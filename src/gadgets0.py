from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# Standard support utils

## The usual suspects

"""
from contextlib import contextmanager
import pprint,datetime,time
import random,math
from ok import *
"""

## Some one(ish) liners.

"""
pi  = math.pi
ee  = math.e
sin = math.sin
sqrt= math.sqrt
r   = random.random
isa = isinstance

def say(*lst):
  sys.stdout.write(', '.join(map(str,lst)))
  sys.stdout.flush()
  
def r3(lst,n=3):
  return map(lambda x:round(x,n),lst)

def r5(lst): return r3(lst,5)

def seed(x=None):
  random.seed(x or the.MISC.seed)

def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=None,ordered=True):
  tiles = tiles or the.MISC.tiles
  lst   = lst if ordered else sorted(lst)
  at    = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]

def median(lst,ordered=False):
  lst = sorted(lst)
  m = len(lst)
  j = lst[int(m/2)+1]
  if m % 2:
    return j
  else:
    i = lst[int(m/2)]
    return (i+j)/2.1
  
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
            indent= indent or the.MISC.show.indent,
            width = width  or the.MISC.show.width))

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

+ Magic constants do not become 1000 global variables:
  + All such constants are nested inside one global called `the`.
+ It is all stored in one central place (so we
  can print all the current constants);
  + This code stores everything in a magic place called `the`.
+ That place can be updated from all over the code base
  (so the specification of those constants can be
  distributed over to near the code that actually uses them);
  + This code defines a decorator that wraps any function
    that defines a settings.
  + E.g. see `MISC`, below.
+ Using the `study`
  function, defined below, it is possible to:
   + Temporarily override those values;
   + Then reset all those values back to
     some defaults.

The code assumes that settings are set via some method:

```python
def theseSettings(**overrides):
  d1 = theSettings()
  d1.update(overrides)
  the.theseSettings = d1
```

This is a common enough pattern that I auto-create the above
using a decorator around a function that returns
a dictionary.

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
def MISC(): return o(
    seed=1,
    tiles=[0.1,0.3,0.5,0.7,0.9],
    show=o(indent=2,
           width=50))
"""

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

  
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
  print("\n# " + "-" * 50,                 # before
        "\n# ", what, "\n#",               # before
        datetime.datetime.now().strftime(  # before
          "%Y-%m-%d %H:%M:%S"))            # before
  for (using, override) in usings:         # before
    using(**override)                      # before: make new settings
  seed()                                   # before: reset seed
  t1 = time.time()                         # before
  show(the)                                # before
  print("")                                # before
  yield                                      
  t2 = time.time()                         # after
  print("\n# " + "-" * 50)                 # after
  print("# Runtime: %.3f secs\n" % (t2-t1))# after  : print runtime
  for (using,_) in usings:                 # after  : reset settings
    using()                                # after
