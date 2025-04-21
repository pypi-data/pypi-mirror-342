import blinker
import inspect
import itertools
import weakref
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
    Type,
    Set,
    get_origin,
    get_args,
)
from types import SimpleNamespace
import asyncio

_ReceiverCallable = Callable[..., Any]

MAX_CACHE_SIZE = 1024
_dict_ns_cache = {}
_list_ns_cache = {}


def _memoized_dict_to_ns(obj):
    obj_id = id(obj)
    if obj_id in _dict_ns_cache:
        return _dict_ns_cache[obj_id]
    if not all(isinstance(k, str) for k in obj):
        return obj
    try:
        ns = SimpleNamespace(
            **{k: _CoolSignalBase._recursive_ns_memo(v) for k, v in obj.items()}
        )
    except TypeError:
        ns = obj
    if len(_dict_ns_cache) >= MAX_CACHE_SIZE:
        _dict_ns_cache.clear()
    _dict_ns_cache[obj_id] = ns
    return ns


def _memoized_list_to_ns(obj):
    obj_id = id(obj)
    if obj_id in _list_ns_cache:
        return _list_ns_cache[obj_id]
    ns_list = [_CoolSignalBase._recursive_ns_memo(v) for v in obj]
    if len(_list_ns_cache) >= MAX_CACHE_SIZE:
        _list_ns_cache.clear()
    _list_ns_cache[obj_id] = ns_list
    return ns_list


class _CoolSignalBase(blinker.Signal):
    _send_counter: "itertools.count[int]"
    _receiver_map: "weakref.WeakKeyDictionary[_ReceiverCallable, _ReceiverCallable]"

    def __init__(self, doc: Optional[str] = None) -> None:
        super().__init__(doc)
        self._send_counter = itertools.count()
        self._receiver_map = weakref.WeakKeyDictionary()

    def disconnect(
        self, receiver: _ReceiverCallable, sender: Any = blinker.ANY
    ) -> None:
        wrapped_receiver = self._receiver_map.pop(receiver, None)
        if wrapped_receiver:
            super().disconnect(wrapped_receiver, sender=sender)

    @staticmethod
    def _recursive_ns(value: Any) -> Any:
        return _CoolSignalBase._recursive_ns_memo(value)

    @staticmethod
    def _recursive_ns_memo(value: Any):
        if isinstance(value, dict):
            return _memoized_dict_to_ns(value)
        if isinstance(value, list):
            return _memoized_list_to_ns(value)
        return value

    @staticmethod
    def _build_param_converters(
        sig: inspect.Signature,
    ) -> Dict[str, Callable[[Any], Any]]:
        param_converters: Dict[str, Callable[[Any], Any]] = {}
        builtin_types = {
            str,
            int,
            float,
            bool,
            bytes,
            dict,
            list,
            tuple,
            set,
            type(None),
        }
        for param_name, param_obj in sig.parameters.items():
            ann = param_obj.annotation
            if ann is inspect.Parameter.empty or ann is Any:
                continue
            origin = get_origin(ann)
            args = get_args(ann)
            if origin is list and args:
                elem_type = args[0]
                if (
                    inspect.isclass(elem_type)
                    and elem_type not in builtin_types
                    and elem_type is not Any
                ):

                    def make_list_converter(
                        elem_cls: Type[Any],
                    ) -> Callable[[Any], Any]:
                        def _conv(value_list: Any) -> Any:
                            if isinstance(value_list, list):
                                converted_list = []
                                for item in value_list:
                                    if isinstance(item, elem_cls):
                                        converted_list.append(item)
                                    elif isinstance(item, dict):
                                        try:
                                            converted_list.append(elem_cls(**item))
                                        except Exception:
                                            converted_list.append(
                                                _CoolSignalBase._recursive_ns(item)
                                            )
                                    else:
                                        converted_list.append(item)
                                return converted_list
                            return value_list

                        return _conv

                    param_converters[param_name] = make_list_converter(elem_type)
                    continue
            if inspect.isclass(ann) and ann not in builtin_types and ann is not Any:

                def make_obj_converter(obj_cls: Type[Any]) -> Callable[[Any], Any]:
                    def _conv(value: Any) -> Any:
                        if isinstance(value, obj_cls):
                            return value
                        if isinstance(value, dict):
                            try:
                                return obj_cls(**value)
                            except Exception:
                                return _CoolSignalBase._recursive_ns(value)
                        return value

                    return _conv

                param_converters[param_name] = make_obj_converter(ann)
                continue
            param_converters[param_name] = _CoolSignalBase._recursive_ns
        return param_converters


class CoolSignal(_CoolSignalBase):
    @staticmethod
    def _wrap_handler(func: _ReceiverCallable) -> _ReceiverCallable:
        sig = inspect.signature(func)
        func_params: Set[str] = set(sig.parameters.keys())
        func_accepts_kwargs: bool = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )
        param_converters = _CoolSignalBase._build_param_converters(sig)
        has_sender_param = "sender" in sig.parameters
        is_bound_method = hasattr(func, "__self__") and func.__self__ is not None

        def wrapper(sender: Any, **kwargs: Any) -> Tuple[Optional[int], Any]:
            request_id: Optional[int] = kwargs.pop("_request_id", None)
            original_kwargs_snapshot = kwargs.copy()
            converted_kwargs: Dict[str, Any] = {}
            for key, val in kwargs.items():
                if key in param_converters:
                    try:
                        converted_kwargs[key] = param_converters[key](val)
                    except Exception as conv_exc:
                        converted_kwargs[key] = val
                else:
                    converted_kwargs[key] = _CoolSignalBase._recursive_ns(val)

            if func_accepts_kwargs:
                final_kwargs = converted_kwargs
            else:
                valid_params = func_params

                if has_sender_param and not is_bound_method:
                    valid_params = valid_params - {"sender"}

                if is_bound_method and "self" in valid_params:
                    valid_params = valid_params - {"self"}

                final_kwargs = {
                    k: v for k, v in converted_kwargs.items() if k in valid_params
                }

            try:

                if has_sender_param:
                    arg: Any = func(sender, **final_kwargs)
                else:
                    arg: Any = func(**final_kwargs)

            except TypeError as e:
                call_pattern = (
                    "func(sender, **final_kwargs)"
                    if has_sender_param
                    else "func(**final_kwargs)"
                )
                err_msg = (
                    f"Error calling handler '{getattr(func, '__name__', repr(func))}': {e}. "
                    f"Handler Signature: {sig}. Is bound: {is_bound_method}. Expects sender: {has_sender_param}. "
                    f"Call pattern used: {call_pattern}. "
                    f"Provided keyword args (original): {original_kwargs_snapshot}. "
                    f"Processed/Filtered keyword args passed: {final_kwargs}. "
                )
                raise TypeError(err_msg) from e
            return (request_id, arg)

        setattr(wrapper, "_is_coolsignal_wrapped", True)
        return wrapper

    def connect(
        self, receiver: _ReceiverCallable, sender: Any = blinker.ANY, weak: bool = False
    ) -> None:
        if receiver in self._receiver_map:
            return
        is_already_wrapped = getattr(receiver, "_is_coolsignal_wrapped", False)
        if not is_already_wrapped:
            wrapped_receiver = CoolSignal._wrap_handler(receiver)
            self._receiver_map[receiver] = wrapped_receiver
        else:
            wrapped_receiver = receiver
        super().connect(wrapped_receiver, sender=sender, weak=weak)

    def send(
        self, sender: Optional[Any] = None, **kwargs: Any
    ) -> Optional[Any]:
        request_id: int = next(self._send_counter)
        payload: Dict[str, Any] = kwargs.copy()
        payload["_request_id"] = request_id
        responses: list[tuple[_ReceiverCallable, tuple[Optional[int], Any]]] = (
            super().send(sender, **payload)
        )
        for _receiver_func, (rid, value) in responses:
            if rid is not None and rid == request_id and value is not None:
                return value
        return None

    def emit(self, payload: Any, *, sender: Optional[Any] = None) -> Optional[Any]:
        return self.send(sender=sender, payload=payload)


class CoolSignalAsync(_CoolSignalBase):
    @staticmethod
    def _wrap_handler(func: _ReceiverCallable) -> _ReceiverCallable:
        if not inspect.iscoroutinefunction(func):
            raise TypeError("CoolSignalAsync only supports async (coroutine) handlers.")
        sig = inspect.signature(func)
        func_params: Set[str] = set(sig.parameters.keys())
        func_accepts_kwargs: bool = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )
        param_converters = _CoolSignalBase._build_param_converters(sig)
        has_sender_param = "sender" in sig.parameters
        is_bound_method = hasattr(func, "__self__") and func.__self__ is not None

        async def wrapper(sender: Any, **kwargs: Any) -> Tuple[Optional[int], Any]:
            request_id: Optional[int] = kwargs.pop("_request_id", None)
            original_kwargs_snapshot = kwargs.copy()
            converted_kwargs: Dict[str, Any] = {}
            for key, val in kwargs.items():
                if key in param_converters:
                    try:
                        converted_kwargs[key] = param_converters[key](val)
                    except Exception as conv_exc:
                        converted_kwargs[key] = val
                else:
                    converted_kwargs[key] = _CoolSignalBase._recursive_ns(val)

            if func_accepts_kwargs:
                final_kwargs = converted_kwargs
            else:
                valid_params = func_params

                if has_sender_param and not is_bound_method:
                    valid_params = valid_params - {"sender"}

                if is_bound_method and "self" in valid_params:
                    valid_params = valid_params - {"self"}

                final_kwargs = {
                    k: v for k, v in converted_kwargs.items() if k in valid_params
                }

            try:

                if has_sender_param:
                    arg: Any = await func(sender, **final_kwargs)
                else:
                    arg: Any = await func(**final_kwargs)

            except TypeError as e:
                call_pattern = (
                    "await func(sender, **final_kwargs)"
                    if has_sender_param
                    else "await func(**final_kwargs)"
                )
                err_msg = (
                    f"Error calling handler '{getattr(func, '__name__', repr(func))}': {e}. "
                    f"Handler Signature: {sig}. Is bound: {is_bound_method}. Expects sender: {has_sender_param}. "
                    f"Call pattern used: {call_pattern}. "
                    f"Provided keyword args (original): {original_kwargs_snapshot}. "
                    f"Processed/Filtered keyword args passed: {final_kwargs}. "
                )
                raise TypeError(err_msg) from e
            return (request_id, arg)

        setattr(wrapper, "_is_coolsignal_wrapped", True)
        return wrapper

    def connect(
        self, receiver: _ReceiverCallable, sender: Any = blinker.ANY, weak: bool = False
    ) -> None:
        if receiver in self._receiver_map:
            return
        is_already_wrapped = getattr(receiver, "_is_coolsignal_wrapped", False)
        if not is_already_wrapped:
            wrapped_receiver = CoolSignalAsync._wrap_handler(receiver)
            self._receiver_map[receiver] = wrapped_receiver
        else:
            wrapped_receiver = receiver
        super().connect(wrapped_receiver, sender=sender, weak=weak)

    async def send(
        self, sender: Optional[Any] = None, **kwargs: Any
    ) -> Optional[Any]:
        request_id: int = next(self._send_counter)
        payload: Dict[str, Any] = kwargs.copy()
        payload["_request_id"] = request_id
        responses = await self._send_all(sender, **payload)
        for _receiver_func, (rid, value) in responses:
            if rid is not None and rid == request_id and value is not None:
                return value
        return None

    async def emit(self, payload: Any, *, sender: Optional[Any] = None) -> Optional[Any]:
        return await self.send(sender=sender, payload=payload)

    async def _send_all(self, sender: Any, **payload: Any):
        coros = []
        for receiver in self.receivers_for(sender):
            coros.append(receiver(sender, **payload))
        results = await asyncio.gather(*coros)
        return zip(self.receivers_for(sender), results)
