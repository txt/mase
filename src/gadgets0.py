from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# Standard support utils

## The usual suspects

"""
from contextlib import contextmanager
import pprint,datetime,time
import random
from ok import *
"""

## Some one liners.

"""
r   = random.random
isa = isinstance

def seed(x=None):
  random.seed(x or the.misc.seed)

def shuffle(lst):
  random.shuffle(lst)
  return lst
"""

## Printing some structure of arbitrary depth:

"""
def show(x, indent=None, width=None):
  def has(x):
    if isa(x,list): return [has(v) for v in x]
    if isa(x,dict): return {k:has(v) for k,v
                            in x.items()
                            if k[0] != "_"}
    if isa(x,o): return has(x.__dict__)
    if isa(x,float): return '%g' % x
    return x
  print(pprint.pformat(has(x),
            indent= indent or the.misc.show.indent,
            width = width  or the.misc.show.width))

"""

## Javascript struct emulation

"""
class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
"""

## Magic constants

A place to store all the magic params, and reset
them after some study.

That place has the following properties:

+ It is all stored in one central place (so we
  can print all the current constants);
  + This code stores everything in a magic place called `the`.
+ That place can be updated from all over the code base
  (so the specification of those constants can be
  distributed over to near the code that actually uses them);
  + This code defines a decorator that wraps any function
    that defines a settings.
  + E.g. see `misc`, below.
+ It is possible to:
   + Temporarily override those values;
   + Then reset all those values back to
     some defaults.

The last two requirements are handled by the `study`
function, shown below.

"""
the = o()

def setting(f):
  "Decorator. Stores output of function in 'the'."
  name = f.__name__
  def wrapper(**d):
    tmp = f()
    tmp.__dict__.update(d) # maybe do some overrides
    the[name] = tmp  # store the settings in `the`
    return tmp
  wrapper()  # so a side effect of loading the function
             # is to call the function
  return wrapper
""" 

### Set some settings

"""    
@setting
def misc(): return o(
    seed=1,
    show=o(indent=2,
           width=50))
"""

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

"""
def use(x,**y):
  """Convenience function: for temporarily 
     overwriting defaults."""
  return (x,y)

@contextmanager
def study(what,*usings):
  """Maybe change settings. Always call 
     seed(). Afterwards, set  settings back 
     to defaults."""
  print("\n# " + "-" * 50,
        "\n# ", what, "\n#",
        datetime.datetime.now().strftime(
          "%Y-%m-%d %H:%M:%S"))
  for (using, override) in usings:
    using(**override)
  seed()
  t1 = time.time()
  yield
  show(the)
  t2 = time.time()
  print("\n# " + "-" * 50)
  print("# Runtime: %.3f secs" % (t2-t1))
  for (using,_) in usings:
    using()
