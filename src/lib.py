from __future__ import print_function,division
import random, pprint, re, datetime, time
from contextlib import contextmanager
import pprint,sys
from boot import *

@setting
def LIB(): return o(
    seed =  1,
    has  = o(decs = 3,
             skip="_",
             wicked=True),
    show = o(indent=2,
             width=80)
)
#-------------------------------------------------
def lt(x,y): return x < y
def gt(x,y): return x > y

isa   = isinstance
fun   = lambda x:x.__class__.__name__ == 'function'
r     = random.random
any   = random.choice
seed = random.seed

def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
  at = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]

def say(*lst):
  sys.stdout.write(', '.join(map(str,lst)))
  sys.stdout.flush()

#-------------------------------------------------
def show(x, indent=None, width=None):  
  print(pprint.pformat(has(x),
            indent= indent or the.LIB.show.indent,
            width = width  or the.LIB.show.width))

def has(x,  decs=None, wicked=None, skip=None) :
  if decs   is None:
    decs = the.LIB.has.decs
  if wicked is None:
    wicked = the.LIB.has.wicked
  if skip   is None:
    skip = the.LIB.has.skip
  if   isa(x, o):
    return has({x.__class__.__name__: x.d()})
  elif isa(x,list):
    return map(has,x)
  elif isa(x,float):
    return round(x,decs)
  elif fun(x):
    return x.__name__+'()'
  elif wicked and hasattr(x,"__dict__"):
      return has({x.__class__.__name__ : x.__dict__})
  elif isa(x, dict):
    return {k:has(v)
            for k,v in x.items()
            if skip != str(k)[0]}
  else:
    return x

def cache(f):
  name = f.__name__
  def wrapper(i):
    i.cache = i._cache or {}
    key = (name, i.id)
    if key in i._cache:
      x = i._cache[key]
    else:
      x = f(i) # sigh, gonna have to call it
    i._cache[key] =  x # ensure ache holds 'c'
    return x
  return wrapper

@contextmanager
def duration():
  t1 = time.time()
  yield
  t2 = time.time()
  print("\n" + "-" * 72)
  print("# Runtime: %.3f secs" % (t2-t1))

def use(x,**y): return (x,y)

@contextmanager
def settings(*usings):
  for (using, override) in usings:
    using(**override)
  yield
  for (using,_) in usings:
    using()
    
@contextmanager
def study(what,*usings):
  print("\n#" + "-" * 50,
        "\n#", what, "\n#",
        datetime.datetime.now().strftime(
          "%Y-%m-%d %H:%M:%S"))    
  for (using, override) in usings:
    using(**override)              
  seed(the.LIB.seed)            
  show(the)                   
  with duration():
    yield
  for (using,_) in usings:
    using()               
