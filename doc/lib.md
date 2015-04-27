[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)
[Contents](https://github.com/txt/mase/blob/master/TOC.md) | [About](https://github.com/txt/mase/blob/master/ABOUT.md) | [Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) | [Code](https://github.com/txt/mase/tree/master/src) | [Contact](http://menzies.us)</em>



# Lib: Standard library routines

````python

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

def first(lst): return lst[0]
def last(lst): return lst[-1]
                          
def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9],norm=False,f=3):
  if norm:
    lo,hi = lst[0], lst[-1]
    lst = g([(x - lo)/(hi-lo+0.000001) for x in lst],f)
  at = lambda x: lst[ int(len(lst)*x) ]
  lst = [ at(tile) for tile in tiles ]
  
  return lst

def say(*lst):
  sys.stdout.write(', '.join(map(str,lst)))
  sys.stdout.flush()

def g(lst,f=3):
  return map(lambda x: round(x,f),lst)
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
    i._cache = i._cache or {}
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
````



<img align=left src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">
Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

