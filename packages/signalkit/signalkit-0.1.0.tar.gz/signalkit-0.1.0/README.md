# SignalKit

SignalKit is a lightweight utility library that builds on Blinker to provide structured, UUID-based signal-response orchestration.

## Features

- Typed signal events using dataclasses (or any object with a request_id)
- Safe response correlation via request IDs
- Decorators to simplify consistent handler behavior
- High performance, minimal dependencies

## Install

```bash
pip install -e .

```

## Usage Example

```python
from dataclasses import dataclass, field
import uuid
from src.core import CoolSignal

@dataclass
class SignalEvent:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

signal = CoolSignal()

def handler(sender, event: SignalEvent):
    if event.request_id == "abc":
        return "matched!"

signal.connect(handler)
event = SignalEvent(request_id="abc")
result = signal.send(signal, event=event)
print(result)  # "matched!"
```

## Note

SignalKit works with any event object that has a `request_id` attribute. For high-performance or low-latency systems, you can use a `dataclass` as shown above. For more complex validation, you can use your own custom class.
