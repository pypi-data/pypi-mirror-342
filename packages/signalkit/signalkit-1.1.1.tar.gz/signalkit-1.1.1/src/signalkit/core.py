import blinker
import inspect
import itertools
import weakref
from typing import Any, Callable, Dict, Optional, Tuple, Type, Set

_ReceiverCallable = Callable[..., Any]

class CoolSignal(blinker.Signal):
    _send_counter: 'itertools.count[int]'
    _receiver_map: 'weakref.WeakKeyDictionary[_ReceiverCallable, _ReceiverCallable]'

    def __init__(self, doc: Optional[str] = None) -> None:
        super().__init__(doc)
        self._send_counter = itertools.count()
        self._receiver_map = weakref.WeakKeyDictionary()

    @staticmethod
    def _wrap_handler(func: _ReceiverCallable) -> _ReceiverCallable:
        sig = inspect.signature(func)
        func_params: Set[str] = set(sig.parameters.keys())
        func_accepts_kwargs: bool = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )

        def wrapper(sender: Any, **kwargs: Any) -> Tuple[Optional[int], Any]:
            request_id: Optional[int] = kwargs.pop("_request_id", None)
            call_args: Tuple[Any, ...] = kwargs.pop("_args", ())
            is_bound: bool = hasattr(func, "__self__") and func.__self__ is not None

            final_kwargs: Dict[str, Any] = {}
            original_kwargs_snapshot = kwargs.copy()

            if func_accepts_kwargs:
                final_kwargs = kwargs
            else:
                valid_params = func_params
                if not is_bound and 'sender' in valid_params:
                    valid_params = valid_params - {'sender'}
                final_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}

            try:
                if is_bound:
                    arg: Any = func(*call_args, **final_kwargs)
                else:
                    arg: Any = func(sender, *call_args, **final_kwargs)
            except TypeError as e:
                err_msg = (
                    f"Error calling handler '{getattr(func, '__name__', repr(func))}': {e}. "
                    f"Handler Signature: {sig}. "
                    f"Provided positional args (_args): {call_args}. Provided keyword args (original): {original_kwargs_snapshot}. "
                    f"Processed/Filtered keyword args passed: {final_kwargs}. "
                    f"Is bound: {is_bound}."
                )
                raise TypeError(err_msg) from e

            return (request_id, arg)

        wrapper._is_coolsignal_wrapped = True
        return wrapper

    def connect(self, receiver: _ReceiverCallable, sender: Any = blinker.ANY, weak: bool = False) -> None:
        if receiver in self._receiver_map:
            return

        if not getattr(receiver, "_is_coolsignal_wrapped", False):
            wrapped_receiver = self._wrap_handler(receiver)
            self._receiver_map[receiver] = wrapped_receiver
        else:
            wrapped_receiver = receiver

        super().connect(wrapped_receiver, sender=sender, weak=weak)

    def disconnect(self, receiver: _ReceiverCallable, sender: Any = blinker.ANY) -> None:
        wrapped_receiver = self._receiver_map.pop(receiver, None)

        if wrapped_receiver:
            super().disconnect(wrapped_receiver, sender=sender)
        else:
            pass

    def send(self, sender: Optional[Any] = None, *args: Any, **kwargs: Any) -> Optional[Any]:
        request_id: int = next(self._send_counter)

        payload: Dict[str, Any] = kwargs.copy()
        payload["_request_id"] = request_id
        payload["_args"] = args

        responses: list[tuple[_ReceiverCallable, tuple[Optional[int], Any]]] = super().send(sender, **payload)

        for _receiver_func, (rid, value) in responses:
            if rid is not None and rid == request_id and value is not None:
                return value
        return None
