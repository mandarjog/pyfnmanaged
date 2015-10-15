import os
from concurrent import futures
from peak.util.proxies import LazyProxy
import decorator

g_executor = LazyProxy(lambda: futures.ThreadPoolExecutor(max_workers=4))


"""
A managed functions behaviour can be changed at runtime.
In this case it will be affected by the FN_MANAGED env variable.

It can turn readable sequential code into more performant code.
The runtime decides how to best execute this piece of code.
Look at the test to see what it can do
"""


@decorator.decorator
def managed(fn, *args, **kwargs):
    pw_async = os.environ.get("FN_MANAGED", "false").lower()
    if pw_async == "lazy":
        retval = LazyProxy(lambda: fn(*args, **kwargs))
    elif pw_async == "async":
        future = g_executor.submit(fn, *args, **kwargs)
        retval = LazyProxy(lambda: future.result())
    else:
        retval = fn(*args, **kwargs)
    return retval
