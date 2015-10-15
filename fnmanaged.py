import os
from concurrent import futures
from peak.util.proxies import LazyProxy
import decorator

g_executor = LazyProxy(lambda:
                       futures.ThreadPoolExecutor(
                           max_workers=int(
                               os.environ.get("FN_MANAGED_WORKERS", 4))))


"""
A managed functions behaviour can be changed at runtime.
In this case it will be affected by the FN_MANAGED env variable.

It can turn readable sequential code into more performant code.
The runtime decides how to best execute this piece of code.
Look at the tests to see what it can do
"""


@decorator.decorator
def managed(fn, *args, **kwargs):
    pw_async = os.environ.get("FN_MANAGED", "false").lower()
    if pw_async == "lazy":
        retval = LazyProxy(lambda: fn(*args, **kwargs))
    elif pw_async == "async":
        def _thread_exec(*args, **kwargs):
            #TODO? add redirect stdout here
            return fn(*args, **kwargs)
        future = g_executor.submit(_thread_exec, *args, **kwargs)
        retval = LazyProxy(lambda: future.result())
    else:
        retval = fn(*args, **kwargs)
    return retval
