from src.core import CoolSignal, SignalResponse


def test_send_returns_all_responses_when_no_request_id():
    # arrange
    signal = CoolSignal()

    def handler(sender, **kwargs):
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
    response = SignalResponse(request_id="not-matching")

    def handler(sender, response: SignalResponse):
        if response.request_id == "some-other-id":
            return "should not match"

    # act
    signal.connect(handler)
    response = signal.send(signal, response=response)

    # assert
    assert response is None


def test_send_returns_value_for_matching_request_id_among_multiple_handlers():
    # arrange
    signal = CoolSignal()
    response1 = SignalResponse()
    response2 = SignalResponse()
    response3 = SignalResponse()

    def handler1(sender, response: SignalResponse):
        if response.request_id == response1.request_id:
            return "handler1"

    def handler2(sender, response: SignalResponse):
        if response.request_id == response2.request_id:
            return "handler2"

    def handler3(sender, response: SignalResponse):
        if response.request_id == response3.request_id:
            return "handler3"

    # act
    signal.connect(handler1)
    signal.connect(handler2)
    signal.connect(handler3)

    # assert
    assert signal.send(signal, response=response1) == "handler1"
    assert signal.send(signal, response=response2) == "handler2"
    assert signal.send(signal, response=response3) == "handler3"
