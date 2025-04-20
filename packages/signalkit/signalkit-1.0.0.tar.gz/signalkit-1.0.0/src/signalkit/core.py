import blinker
import inspect
import itertools
import weakref


class CoolSignal(blinker.Signal):
    def __init__(self, doc=None):
        super().__init__(doc)
        self._send_counter = itertools.count()
        self._receiver_map = weakref.WeakKeyDictionary()

    @staticmethod
    def _wrap_handler(func):
        sig = inspect.signature(func)
        func_params = set(sig.parameters.keys())
        func_accepts_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )

        def wrapper(sender, **kwargs):

            request_id = kwargs.pop("_request_id", None)
            call_args = kwargs.pop("_args", ())
            is_bound = hasattr(func, "__self__") and func.__self__ is not None

            final_kwargs = {}
            if func_accepts_kwargs:
                final_kwargs = kwargs
            else:
                final_kwargs = {k: v for k, v in kwargs.items() if k in func_params}

            try:
                if is_bound:
                    arg = func(*call_args, **final_kwargs)
                else:

                    arg = func(sender, *call_args, **final_kwargs)
            except TypeError as e:

                err_msg = (
                    f"Error calling handler '{func.__name__}': {e}. "
                    f"Handler Signature: {sig}. "
                    f"Provided positional args: {call_args}. Provided keyword args: {kwargs}. "
                    f"Is bound: {is_bound}."
                )
                raise TypeError(err_msg) from e

            return (request_id, arg)

        wrapper._is_coolsignal_wrapped = True
        return wrapper

    def connect(self, receiver, sender=blinker.ANY, weak=False):
        if receiver in self._receiver_map:
            return

        if not getattr(receiver, "_is_coolsignal_wrapped", False):
            wrapped_receiver = self._wrap_handler(receiver)
            self._receiver_map[receiver] = wrapped_receiver
        else:
            wrapped_receiver = receiver

        super().connect(wrapped_receiver, sender=sender, weak=weak)

    def disconnect(self, receiver, sender=blinker.ANY):
        wrapped_receiver = self._receiver_map.pop(receiver, None)

        if wrapped_receiver:
            super().disconnect(wrapped_receiver, sender=sender)
        else:
            pass

    def send(self, sender=None, *args, **kwargs):
        request_id = next(self._send_counter)

        payload = kwargs.copy()
        payload["_request_id"] = request_id
        payload["_args"] = args

        responses = super().send(sender, **payload)

        for _, (rid, value) in responses:
            if rid is not None and rid == request_id and value is not None:
                return value
        return None
