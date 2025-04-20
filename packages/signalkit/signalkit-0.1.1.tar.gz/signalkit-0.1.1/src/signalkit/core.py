from dataclasses import dataclass, field
import uuid
import blinker

@dataclass
class SignalResponse:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class CoolSignal(blinker.Signal):
    @staticmethod
    def _wrap_handler(func):
        def wrapper(sender, *args, **kwargs):
            request_id = None
            for arg in args:
                if isinstance(arg, SignalResponse):
                    request_id = arg.request_id
                    break
            if request_id is None:
                for arg in kwargs.values():
                    if isinstance(arg, SignalResponse):
                        request_id = arg.request_id
                        break
            arg = func(sender, *args, **kwargs)
            return (request_id, arg)
        wrapper._is_wrapped_for_request_id = True
        return wrapper
    def connect(self, receiver, sender=blinker.ANY, weak=False):
        if not getattr(receiver, "_is_wrapped_for_request_id", False):
            receiver = self._wrap_handler(receiver)
        return super().connect(receiver, sender=sender, weak=weak)
    def send(self, sender=None, **kwargs):
        responses = super().send(sender, **kwargs)
        request_id = None
        for value in kwargs.values():
            if isinstance(value, SignalResponse):
                request_id = value.request_id
                break
        if request_id is not None:
            for _, (rid, value) in responses:
                if rid == request_id and value is not None:
                    return value
            return None
        return responses 