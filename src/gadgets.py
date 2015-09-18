from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# GADGETS: Timm's Generic Optimizer Tricks

<img width=400 align=right src="../img/gogo.jpg">

`Gadgets` is a library of utilities for working with optimization models. With `Gadgets`,
it is possible to encode:

```python
for model in [Schaffer,...]:
  for optimizer in [sa,mws...]:
    optimizer(model())
```

`Gadgets` uses 
a little object system based on Python:

+ Candidates store example instances
+ And our knowledge of candidates is stored in `Want` and `Wants` and `Log`:
    + `Log` stores the range of values seen within the generated candidates
    + `Want` stores our expectations for single values of the candidates;
       + This will be used to (e.g.) generate values from some pre-defined range.
       + And we will run one `Log` object for every `Want` object

`Gadgets` then uses the above to store our expectations for lists of values;
       
+ Many of the services of `Gadgets` are define by recursive calls to `Want`
+ E.g. to initialize a candidate, we ask a list of `Want`s for some values.
    
So Candidate is like "instance" and `Want`  are like "class" and `Gadgets` is like
a factory for building new Candidates, and `Log`s.
 
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

The usual suspects:
"""
import random
r   = random.random
isa = isinstance

def seed(x=1):
  random.seed(x)

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
  def __init__(i,also=None):
    i.lo, i.hi, i.also = None, None, also
  def __add__(i,x):
    if   i.lo == None : i.lo = i.hi = x # auto-initialize
    elif x > i.hi     : i.hi = x
    else x < i.lo     : i.lo = x
    if i.also:
      i.also + x
    return x
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 10**-32)
"""

Note one small detail. Sometimes we are logging information
about one run as well as all runs. So `Log` has an `also` pointer
which, if non-nil, is another place to repeat the same information.

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
                  Less("f2", maker=f2)])
"""

### Filling in the Candidates

+ Replace some template candidate with one `what` for each location. Useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

"""
def none()        : return None
def log(also=None): return lambda: Log(also)

def fill(x, what=none):
  if   isa(x,list): return fillList(x,what)
  elif isa(x,o)   : return fillContainer(x,what)
  else            : return what()

def fillList(lst,what):
  return [ fill(x,what) for x in lst]
def fillContainer(old,what):
  return o( **{ k : fill(d[k], what) for k in old } )
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

## `Gadgets`: places to store lots of `Want`s

Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

"""
class Gadgets:
  def __init__(i,
               abouts, # e.g. Schaffer()
               also = None):
    i.abouts = abouts
    i.log    = fill(i.abouts, log(also))
    
  def blank(i):
    "return a new candidate, filled with None"
    return fill(i.abouts, none)
  
  def keepDecs(i)     : return i.decs(True)
  def keepEval(i,can) : return i.eval(i,can,True)
  def keepAggregate(i,can) : return i.aggregate(i,can,True)
  def keeps(i,logs,things)  :
    for log,thing in zip(logs,things):
      log + thing
      
  def decs(i,keep=False):
    "return a new candidate, with guesses for decisions"
    can = i.blank()
    can.decs = [about.maker() for about in i.abouts.decs]
    if keep:
      i.keeps(i.log.decs,can.decs)
    return can
  
  def eval(i,c,keep=False):
    "expire the old aggregate. make the objective scores."
    can.aggregate = None:
    can.objs = [about.maker(can) for about in i.abouts.objs]
    if keep:
      i.keeps(i.log.objs,can.objs)
    return can

  def aggregate(i,can,keep=False):
    "Return the aggregate. Side-effect: store it in the can"
    if can.aggregate == None:
       agg = n = 0
       for obj,about,log in zip(c.objs,
                                i.abouts.objs,
                                i.log.objs):
         n   += 1
         agg += about.fromHell(obj,log)
       can.aggregate = agg ** 0.5 / n ** 0.5
       if keep:
         i.abouts.aggregate += can.aggregate
    return can.aggregate
       
  def mutate(i,can,p,keep=False):
    "Return a new can with p% mutated"
    can1= i.blank()
    for n,(dec,about) in enumerate(zip(can.decs,i.about.decs)):
      can1.decs[n] = about.maker() if p > r() else dec
    if keep:
      i.keeps(i.log.decs,can1.decs)
    return can1
  
  def baseline(i,n=100):
    "Log the results of generating, say, 100 random instances."
    for _ in xrange(n):
      can = i.keepEval( i.keepDecs() )
      i.keepAggregate(can)
      return can

def sa(m,
       p=0.3, cooling=1,kmax=1000,e[silon=10.1,era=100,lives=5): # e.g. sa(Schafer())
       k, life, e = 1,lives,1e32):


