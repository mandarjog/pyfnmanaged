# pyfnmanaged
*managed python functions*
```python
# This decorator shows how to inject management into a system.
# It is done by decorating a function with the @managed decorator
# It uses python concurrent.futures api

def add(a, b):
  time.sleep(1)
  return a + b

def sub(a, b):
  time.sleep(2)
  return a - b
  
def mul(a, b):
  time.sleep(3)
  return a * b

# we would like to perform the following
# computation
# (10 + 20) * (50 - 10) == 1200  [ans]

# This is an example of how one would write
# performant code
def do_imperative():
  c = executor.submit(add, 10, 20)
  d = executor.submit(sub, 50, 10)
  e = executor.submit(mul, c.result(), d.result())
  
  return e.result()
  
# This is how the same code looks if
# functions are decorated
def do_declarative():
  c = add(10, 20)
  d = sub(50, 10)
  ans = mul(c, d)
  return ans

# do_declaritive is much more readable
# you concentrate on the business logic.
# This is a good way to inject async behaviour
# The 'managed' decorator can decide on the fly if a function should 
# be executed synchronously, on a different thread
# or in a distributed way using celery
```
