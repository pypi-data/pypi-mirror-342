# SignalKit

SignalKit is a lightweight utility library that builds on Blinker to provide structured, UUID-based signal-response orchestration.

## Features

- Typed signal events using [Pydantic](https://docs.pydantic.dev/)
- Safe response correlation via request IDs
- Decorators to simplify consistent handler behavior
- High performance, minimal dependencies

## Install

```bash
pip install -e .
```

## Usage Example

```python
from pydantic import BaseModel, Field
import uuid
from signalkit.core import CoolSignal, SignalEvent

class MyEvent(SignalEvent):
    value: str

signal = CoolSignal()

def handler(sender, event: MyEvent):
    if event.value == "hello":
        return "matched!"

signal.connect(handler)
event = MyEvent(value="hello")
result = signal.send(signal, event=event)
print(result)  # "matched!"
```

## Note

SignalKit works with any Pydantic model that has a `request_id` field. For more complex validation and parsing, simply extend `SignalEvent` with your own fields.