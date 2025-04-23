from utils.Trace import Trace


def test_trace_singleton():
    t1 = Trace()
    t2 = Trace()
    assert t1 is t2

    t1.setup()
    t2.setup()

    assert t1.trace is t2.trace
