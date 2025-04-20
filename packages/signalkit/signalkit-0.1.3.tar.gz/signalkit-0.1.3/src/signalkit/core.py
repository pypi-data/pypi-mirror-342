import uuid
import blinker
from pydantic import BaseModel, Field

class SignalEvent(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class CoolSignal(blinker.Signal):
    @staticmethod
    def _wrap_handler(func):
        def wrapper(sender, *args, **kwargs):
            request_id = None
            event = kwargs.get('event', None)
            if event and hasattr(event, 'request_id'):
                request_id = event.request_id
            if hasattr(func, '__self__') and func.__self__ is not None:
                arg = func(event)
            else:
                arg = func(sender, event)
            return (request_id, arg)
        wrapper._is_wrapped_for_request_id = True
        return wrapper
    def connect(self, receiver, sender=blinker.ANY, weak=False):
        if not getattr(receiver, "_is_wrapped_for_request_id", False):
            receiver = self._wrap_handler(receiver)
        return super().connect(receiver, sender=sender, weak=weak)
    def send(self, sender=None, **kwargs):
        responses = super().send(sender, **kwargs)
        event = kwargs.get('event', None)
        request_id = getattr(event, 'request_id', None) if event else None
        if request_id is not None:
            for _, (rid, value) in responses:
                if rid == request_id and value is not None:
                    return value
            return None
        return responses