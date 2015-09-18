from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# GO: Timm's Generic Optimizer Gadgets

<img align=right src="../img/gogo.jpg">

Implementation note: in the following I define a little object system based on Python:

+ Candidates store example instances
+ And our knowledge of candidates is stored in `Want` and `Wants` and `Log`:
    + `Log` stores the range of values seen within the generated candidates
    + `Want` stores our expectations for single values of the candidates;
       + This will be used to (e.g.) generate values from some pre-defined range.
       + And we will run one `Log` object for every `Want` object
    + `Wants` stores our expectations for lists of values;
       + The slots of these `Wants` will be all `Want` instances;
       + So many of the services of `Wants` will be define by recursive calls to `Want`
       + E.g. to initialize a candidate, we ask a list of `Want`s for some values.
    
So Candidate is like "instance" and `Want`, `Wants` is like class. 
It is insightful to ask why I wrote my own mini-class system (rather than, say, standard
Python). The answers are that:

+ Sometimes, these models are generated at runtime
in which case we want a simple programmatic way of
defining new "classes";
+ My classes are special in that each slot value has
a clear set of expectations (the `Want`) and a track
record of all assigned values (the `Log`). While
this can be added to standard Python, it can get a
little messy.

## Standard support utils

The usual 
"""
import random
r   = random.random
isa = isinstance
_ = None

def seed(x=None):
  random.seed(x or the.run.seed)

class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
"""

## Log

This class is the simplest of all.  It just remembers the range of values
seen so far.

"""
class Log:
  def __init__(i):
    i.lo, i.hi = None, None
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 10**-32)
  def __iadd__(i,x):
    if   i.lo == None : i.lo = i.hi = x # auto-initialize
    elif x > i.hi     : i.hi = x
    else x < i.lo     : i.lo = x
    return i
"""

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

"""        
def Candidate(decs=[],objs=[]):
  return o(dec=dec,objs=objs,
           aggregate=None)
"""

Example model (note the use of the `want`, `less` and `more` classes... defined below).

"""
def Schaffer():
  def f1(can):
    x = can.decs[0]
    return x**2
  def f2(can):
    x = can.decs[0]
    return (x-2)**2
  return Candidate(
          decs = [Want("x",   lo = -4, hi = 4)],
          objs = [Less("f1",  maker=f1),
                  Less("f12", maker=f2)])
"""

### Filling in the Candidates

+ Replace some template candidate with one `what` for each location. Useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

"""
def none(): return None
def log():  return Log()

def fill(x, what=none):
  if isinstance(x,list):
    return fillList(x,what)
  elif isinstance(x,o):
    return o( fillDictionary(o.__dict__, what) )
  else:
    return slot()

def fillList(lst,what):
  return [ what() for _ in lst]
def fillDictionary(d,what):
  return { k:fill(v,what) for k,v in d.items() }
"""

## Want

The `Want` class (and its subs: `Less` and `More`) define our expectation for 
each `Candidate`
values.

If we need a value for a `Candidate`, we call `.maker()`:

+ For decisions,
  this just pulls a value from the known `hi` and `lo` ranges;
+ For objectives,
  call some `maker` function passed over an initialization time.

Note that `Want` is a handy place to implement some useful services:

+ Checking if a value is `ok` (in bounds `lo..hi`);
+ `restrain`ing out of bound values back to `lo..hi`;
+ `wrap`ing out of bounds value via modulo;


"""
class Want(object):
  def __init__(i, txt, init=None,
                  lo=-10**32, hi=10**32,
                  maker=None):
    i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
    i.maker = maker or i.guess
  def __repr__(i):
    return 'o'+str(i.__dict__)
    def guess(i):
    return i.lo + r()*(i.hi - i.lo)
  def restrain(i,x):
    return max(i.lo, min(i.hi, x))
  def wrap(i,x):
    return i.lo + (x - i.lo) % (i.hi - i.lo)
  def ok(i,x):
    return i.lo <= x <= i.hi
"""

### Want Objectives?

Subclasses of `Want` store information about objectives 
including:

+ How to compute the distance `fromHell`.
+ When does one objective have a `better` value than another;


Here are out `better` predicates:

"""
def lt(i,j): return i < j
def gt(i,j): return i > j
"""

And these control our objectives as follows:

"""
class Obj(Want):
  def fromHelll(i,x,log):
    hell = 1 if i.better == lt else 0
    return (hell - log.norm(x)) ** 2
  
class Less(Obj):
  def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
    super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
    i.better = lt
    
class More(Obj):
  def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
    super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
    i.better = gt
"""

## Wants: places to store lots of `Want`s

"""
class Wants:
  def __init__(i, wants,also = None):
    i.wants  = wants
    i.log    = fill(i.wants, log)
    i.also   = also
    
  def decs(i):
    can = i.blank()
    can.decs = [want.maker() for want in i.wants.decs]
    return can
  
  def seen(i,whats,loggers):
    for what in whats:
      for logs in loggers:
        for got,log in zip(can[what],logs[what]):
          log += got
          
  def evaluate(i,c):
    can.aggregate = None:
    can.objs = [want.maker(can) for want in i.wants.objs]
    return can
  
  def aggregate(i,can):
    if can.aggregate == None:
      agg = n = 0
      for obj,want,log in zip(c.objs,i.wants.objs.i.log.objs):
        n   += 1
        agg += want.fromHell(obj,log)
      can.aggregate = agg ** 0.5 / n ** 0.5
    return can.aggregate
  
  def blank(i):
    return fill(i.wants, none)
  
  def mutate(i,can,p):
    can1= i.blank()
    for n,(dec,want) in enumerate(zip(can.decs,i.want.decs)):
      can1[n] = want.maker() if p > r() else dec
    return can1
  
  def baseline(i,n=100):
    for _ in xrange(n):
      can = i.evaluate( i.decs() )
      i.log.aggregate  += i.aggregate(can)
      i.also.aggregate += i.aggregate(can)
      i.seen(can, ["decs","objs"],
                  [i.log,i.also])
      


def sa(m,
       p=0.3, cooling=1,kmax=1000,e[silon=10.1,era=100,lives=5): # e.g. sa(Schafer())
       k, life, e = 1,lives,1e32):


