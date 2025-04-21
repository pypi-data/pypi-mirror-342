# SignalKit

SignalKit is a lightweight Python signaling library built upon the robust [Blinker](https://github.com/pallets-eco/blinker) library. It provides a simple yet flexible way to dispatch signals and handle responses, automatically adapting to your handler function signatures.

## Installation
`pip install signalkit`

## Usage Example

```python
# define event model
class Event:
    def __init__(self, text: str):
        self.text = text

# define handler
def handle_event(sender, event: Event) -> str:
    return event.text.upper()

# use CoolSignal
from signalkit import CoolSignal

signal = CoolSignal()
signal.connect(handle_event)

event = Event("hello world")
response = signal.send(sender=None, event=event)
print(response) # 'HELLO WORLD'
```

```python
import asyncio
from signalkit import CoolSignalAsync

async def handle_event_async(sender, event: Event) -> str:
    return event.text.upper()

signal = CoolSignalAsync()
signal.connect(handle_event_async)

event = Event("hello async")
async def main():
    response = await signal.send(sender=None, event=event)
    print(response) # 'HELLO ASYNC'

asyncio.run(main())
```
