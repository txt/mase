# Lib: Standard Utilities

Standard imports: used everywhere.

## Code Standards

Narrow code (52 chars, max); use ``i'', not ``self'', set indent to two characters, 

In a repo (or course). Markdown comments (which means we can do tricks like auto-generating this
documentation from comments in the file).

Not Python3, but use Python3 headers.

good reseraoiuces for advance people: Norving's infrenqencly asked questions

David Isaacon's Pything tips, tricks, and Hacks.http://www.siafoo.net/article/52

Environemnt that supports matplotlib, scikitlearn. Easy to get there.

Old school: install linux. New school: install virtualbox. Newer school: work online.

To checn if you ahve a suseful envorunment, try the following (isntall pip, matpolotlib, scikitlearn)

Learn Python.

Learn tdd

Attitude to coding. not code byt"set yourself up to et rapid feedback on some issue"


```
import random, pprint, re, datetime, time,traceback
from contextlib import contextmanager
import pprint,sys
```

Unit test engine, inspired by Kent Beck.

```
def ok(*lst):
  for one in lst: unittest(one)
  return one

class unittest:
  tries = fails = 0  #  tracks the record so far
  @staticmethod
  def score():
    t = unittest.tries
    f = unittest.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print(traceback.format_exc())
    print(unittest.score(),':',test.__name__, e)
```

Simple container class (offers simple initialization).

```
class o:
  def __init__(i,**d)    : i + d
  def __add__(i,d)       : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return str(i.items())
  def items(i,x=None)    :
    x = x or i
    if isinstance(x,o):
      return [(k,i.items(v)) for
              k,v in x.__dict__.values()
              if not k[0] == "_" ]
    else: return x
```

The settings system.

```
the = o()

def setting(f):
  name = f.__name__
  def wrapper(**d):
    tmp = f()
    tmp + d
    the[name] = tmp
    return tmp
  wrapper()
  return wrapper


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
r    = random.random
any  = random.choice
seed = random.seed
isa  = isinstance

def lt(x,y): return x < y
def gt(x,y): return x > y
def first(lst): return lst[0]
def last(lst): return lst[-1]
                          
def shuffle(lst):
  random.shuffle(lst)
  return lst

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9],
                norm=False, f=3):
  if norm:
    lo,hi = lst[0], lst[-1]
    lst= g([(x - lo)/(hi-lo+0.0001) for x in lst],f)
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
```
