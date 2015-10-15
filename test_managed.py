import os
import time
import fnmanaged


@fnmanaged.managed
def add(a, b):
    time.sleep(1)
    return a + b


@fnmanaged.managed
def sub(a, b):
    time.sleep(2)
    return a - b


@fnmanaged.managed
def mul(a, b):
    time.sleep(3)
    return a * b


def _test(env=None, expected_time=6):
    begin = time.time()
    if env:
        oldval = os.environ.get("FN_MANAGED")
        os.environ["FN_MANAGED"] = env

    # (10 + 20) * (50 - 10) == 1200  [ans]
    c = add(10, 20)
    d = sub(50, 10)
    ans = mul(c, d)

    if env:
        if oldval is not None:
            os.environ["FN_MANAGED"] = oldval

    assert (ans == 1200)
    end = time.time()

    # check if execution took expected amount of time
    assert(abs((end - begin) - expected_time) < 0.2)


def test_sync():
    _test()


def test_lazy():
    _test("lazy")


def test_async():
    # Total time taken should be
    # that of the slowest function ~ 3s
    _test("async", expected_time=3)
