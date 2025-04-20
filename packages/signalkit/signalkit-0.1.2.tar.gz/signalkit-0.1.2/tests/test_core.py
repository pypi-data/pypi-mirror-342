from src.signalkit.core import CoolSignal, SignalEvent


def test_send_returns_all_responses_when_no_request_id():
    # arrange
    signal = CoolSignal()

    def handler(sender, event=None):
        return "ok"

    # act
    signal.connect(handler)
    response = signal.send(signal)

    # assert
    assert isinstance(response, list)
    assert response[0][1] == (None, "ok")


def test_send_returns_none_for_non_matching_request_id():
    # arrange
    signal = CoolSignal()
    event = SignalEvent(request_id="not-matching")

    def handler(sender, event: SignalEvent):
        if event.request_id == "some-other-id":
            return "should not match"

    # act
    signal.connect(handler)
    response = signal.send(signal, event=event)

    # assert
    assert response is None


def test_send_returns_value_for_matching_request_id_among_multiple_handlers():
    # arrange
    signal = CoolSignal()
    event1 = SignalEvent()
    event2 = SignalEvent()
    event3 = SignalEvent()

    def handler1(sender, event: SignalEvent):
        if event.request_id == event1.request_id:
            return "handler1"

    def handler2(sender, event: SignalEvent):
        if event.request_id == event2.request_id:
            return "handler2"

    def handler3(sender, event: SignalEvent):
        if event.request_id == event3.request_id:
            return "handler3"

    # act
    signal.connect(handler1)
    signal.connect(handler2)
    signal.connect(handler3)

    # assert
    assert signal.send(signal, event=event1) == "handler1"
    assert signal.send(signal, event=event2) == "handler2"
    assert signal.send(signal, event=event3) == "handler3"
