from __future__ import print_function, division
#########################################################
# This is free and unencumbered software released into
# the public domain.
#                    __                  __              
#                   /\ \                /\ \__           
#    __      __     \_\ \     __      __\ \ ,_\   ____   
#  /'_ `\  /'__`\   /'_` \  /'_ `\  /'__`\ \ \/  /',__\  
# /\ \L\ \/\ \L\.\_/\ \L\ \/\ \L\ \/\  __/\ \ \_/\__, `\ 
# \ \____ \ \__/.\_\ \___,_\ \____ \ \____\\ \__\/\____/ 
#  \/___L\ \/__/\/_/\/__,_ /\/___L\ \/____/ \/__/\/___/  
#    /\____/                  /\____/                    
#    \_/__/                   \_/__/ 
#   		    
# (c) 2015 Tim Menzies, http://menzies.us
#
# Anyone is free to copy, modify, publish, use,
# compile, sell, or distribute this software, either
# in source code form or as a compiled binary, for any
# purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the
# author or authors of this software dedicate any and
# all copyright interest in the software to the public
# domain. We make this dedication for the benefit of
# the public at large and to the detriment of our
# heirs and successors. We intend this dedication to
# be an overt act of relinquishment in perpetuity of
# all present and future rights to this software under
# copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information, please refer to
# http://unlicense.org
#########################################################

import sys
sys.dont_write_bytecode = True
from gadgets0 import *

"""



# GADGETS: Timm's Generic Optimizer Gadgets (and Goodies)

<img width=400 align=right src="../img/gogo.jpg">


`Gadgets` are a library of utilities for working with
optimization models. 

With `Gadgets`, it is possible to encode something
that looks a little like....

```python
for model in [Schaffer,Fonseca,...]:
  for optimizer in [sa,mws...]:
    for _ in xrange(20):
      optimizer(model())
```

Note that:

+ For samples of how to use this code, see [gadgetsok.py](gadgetsok.py).
+ In the following, anything in `this font` is some method or class in the code.

## What are `Gadgets`?

`Gadgets` are a _Factory_ and a _Facade_:

+ In class-based programming, the _factory_ method
  pattern is a _creational pattern_ which uses factory
  methods to deal with the problem of creating
  objects without specifying the exact class of
  object that will be created. This is done by
  creating objects via (e.g.)  calling a factory
  method-- either specified in an interface and
  implemented by child classes.
+ A _facade_ is an object that provides a simplified 
  interface to a larger body of code, such as a class library. A facade can:
   + make a software library easier to use,
     understand and test, since the facade has
     convenient methods for common tasks;
   + make the library more readable, for the same
     reason; 
   + reduce dependencies of outside code on
     the inner workings of a library, since most
     code uses the facade, thus allowing more
     flexibility in developing the system;

`Gadgets` are a _facade_ since, every time I code a new optimizer, its always some mix-and-match of
numerous lower-level facilities. 

+ On Sundays and Wednesdays, I think optimizers should inherit from
`Gadgets`.
+ On every other day, I believe that since not every gadget applies to every optimizer,
its just more flexible and easier to place all those lower-level facilities into a box, and just 
call interface methods to that box.

_Factories_ assemble _parts_. In this code, I know of three kinds of parts:

+ Parts to hold the specific values from one set of
  decisions, objectives and (optionally) some aggregation of the objective
  scores. In the following, these will be called
  + `decs`
  + `objs`
  + `aggregate`
+ Parts for the some _logging code_ that keeps track of the observed `decs` and `objs, aggregate` values.
+ Parts that talk `About` legal values for the `decs` and `objs` and, for `objs` if we want to minimize
  or maximize those scores.

## Parts of the `Gadgets`

### `Candidate`s

`Candidate`s objects have  objectives, decisions and maybe some aggregate value. 
Using a factory method,  we will fill in `Candidate`s with either 

+ The specific values from one set `decs` and `objs, aggregate`;
+ Or, `Log`ging objects that remember what specific values were ever assigned to  `decs` and `objs, aggregate`;
+ Or, `About` objects that defined what are legel values from the specific values  
  (and, for `objs` if we want to minimize
  or maximize those scores)

In the following, I sometimes refer to `Candidate` objects as `can`. For example, the `ok` method
received a `can` and returns true if the current contents of `decs` are valid.

"""        
class Candidate(object):
  def __init__(i,decs=[],objs=[]):
    i.decs,i.objs=decs,objs
    i.aggregate=None
    i.abouts = i.about()
    
  def __repr__(i):
    "Present me in a  string"
    return printer(i,decs=i.decs,
                   objs=i.objs,
                   aggregated=i.aggregate)

  def __getitem__(i,key):
    "Simple way to access decs or objs or aggregates."
    return i.__dict__[key]
  
  def ok(i,can):
    "Maybe overwritten by subclass."
    return True
  
  def about(i):
    """Factory method for return a Candidate full of 
       About objects."""
    assert False,'implemented by subclass'
    
  
  def clone(i,what = lambda _: None):
    """A genetic factory that makes a new  thing
       like receiver, filled in with 'what' objects."""
    j      = object.__new__(i.__class__)
    j.decs = [what(x) for x in i.decs]
    j.objs = [what(x) for x in i.objs]
    j.aggregate = what(i.aggregate)
    j.abouts = i.abouts
    return j
  
  def alongWith(i,j=None):
    "Convenient iterator."
    if j:
      for one,two in zip(i.decs, j.decs):
        yield one,two
      for one,two in zip(i.objs, j.objs):
        yield one,two
      yield i.aggregate, j.aggregate
      
"""

Using the above, we can build a _factory_ method
called `about` that returns what we know `About`
each candidate.

#### Schaffer

One decision, two objectives, zero  constraints.

"""
class Schaffer(Candidate):
  def about(i):
    def f1(can):
      x = can.decs[0]
      return x**2
    def f2(can):
      x = can.decs[0]
      return (x-2)**2
    i.decs = [An("x",   lo = -10**5, hi = 10**5)]
    i.objs = [Less("f1",  maker=f1),
              Less("f2", maker=f2)]
"""

In the above, `An` and `Less` are really `About` objects that define legal ranges for values 
 (and, for `objs` if we want to minimize
  or maximize those scores).

Note also that `f1` and `f2` are nested methods that accepted a `Candidate` object (which,
you will recall, I call `can`s).


#### Fonseca

One decisions, two objectives, zero constraints.

"""  
class Fonseca(Candidate):
  n=3
  def about(i):
    def f1(can):
      z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
      return 1 - ee**(-1*z)
    def f2(can):
      z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
      return 1 - ee**(-1*z)
    def dec(x):
      return An(x, lo=-4, hi=4)
    i.decs = [dec(x) for x in range(Fonseca.n)]
    i.objs = [Less("f1",  maker=f1),
              Less("f2",  maker=f2)]
"""

Note the use of a list comprehension to create multiple decisions, all with similar properties.
This is handy here and, for more complex models like `ZDT1` with 30 decisions with similar properties,
it is very useful indeed.

#### Kursawe

Three decisions, two objectives,  zero constraints.

"""
class Kursawe(Candidate):
  def about(i,a=1,b=1):
    def f1(can):
      def xy(x,y):
        return -10*ee**(-0.2*sqrt(x*x + y*y))
      a,b,c = can.decs
      return xy(a,b) + xy(b,c)
    def f2(can):
      return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
    def dec(x):
      return  An(x, lo=-5, hi=5)           
    i.decs = [dec(x) for x in range(3)]
    i.objs = [Less("f1",  maker=f1),
              Less("f2",  maker=f2)]
"""

#### ZDT1

Thirty decisions, two objectives,  zero constraints.

"""
class ZDT1(Candidate):
  n=30
  def about(i):
    def f1(can):
      return can.decs[0]
    def f2(can):
      g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
      return g*abs(1 - sqrt(can.decs[0]*g))
    def dec(x):
      return An(x,lo=0,hi=1)
    i.decs = [dec(x) for x in range(ZDT1.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2)]
"""

Again, note the use of a list comprehension to create multiple decisions, all with similar properties.

#### Viennet4

Two decisions, three objectives,  three constraints (all codes into the `ok` method).

"""    
class Viennet4(Candidate):
  def ok(i,can):
     one,two = can.decs
     g1 = -1*two - 4*one + 4
     g2 = one + 1            
     g3 = two - one + 2
     return g1 >= 0 and g2 >= 0 and g3 >= 0
  def about(i):
    def f1(can):
      one,two = can.decs
      return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
    def f2(can):
      one,two = can.decs
      return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
    def f3(can):
      one,two= can.decs
      return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
    def dec(x):
      return An(x,lo= -4,hi= 4)
    i.decs = [dec(x) for x in range(2)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2),
              Less("f3",maker=f3)]
"""

### `Log`ging Objects 

Another kind of part that is assembled into a `Candidate` by a factory methods are
`Log` objects. These  remembers the range of values
seen so far.

Note one small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 

"""
class Log:
  def __init__(i,init=[],also=None):
    i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
    map(i.__add__,init)
  def adds(i,lst):
    map(i.__add__,lst)
  def __add__(i,x):
    i.n += 1
    if   i.empty() : i.lo = i.hi = x # auto-initialize
    elif x > i.hi     : i.hi = x
    elif x < i.lo     : i.lo = x
    if i.also:
      i.also + x
    i._some += x     # NOTE1
    return x
  def some(i):
    return i._some.any
  def tiles(i,tiles=None,ordered=False,n=3):
    return r3(ntiles(i.some(),tiles,ordered),n)
  def empty(i):
    return i.lo == None
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 10**-32)
  def stats(i,tiles=[0.25,0.5,0.75]):
    return ntiles(sorted(i._some.any),
           ordered=False, 
           tiles=tiles)
"""
 
_NOTE1_ As a side-effect of logging, we also keep a small sample of
  the logged items This will come in handy... later. The code
for keeping _Some_ values is shown below.
   
"""
@setting
def SOMES(): return o(
    size=256
    )

class Some:
  def __init__(i, max=None): 
    i.n, i.any = 0,[]
    i.max = max or the.SOMES.size
  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:    
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x 
    return i
"""

### `About` Objects 

The `About` class (and its variants: `Less` and `More`) define our expectation for 
each `Candidate`
values.

If we need a value for a `Candidate`, we call `.maker()`:

+ For decisions,
  this just pulls a value from the known `hi` and `lo` ranges;
+ For objectives,
  call some `maker` function passed over an initialization time.

Note that `About` is a handy place to implement some useful services:

+ Checking if a value is `ok` (in bounds `lo..hi`);
+ `restrain`ing out of bound values back to `lo..hi`;
+ `wrap`ing out of bounds value via modulo;
+ How to compute the distance `fromHell`.

"""
def lt(i,j): return i < j
def gt(i,j): return i > j

class About(object):
  def __init__(i, txt, init=None,
                  lo=-10**32, hi=10**32,
                  better=lt,
                  maker=None):
    i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
    i.maker = maker or i.guess
    i.better= better
  def __repr__(i):
    return 'o'+str(i.__dict__)
  def guess(i):
    return i.lo + r()*(i.hi - i.lo)
  def restrain(i,x):
    return max(i.lo, min(i.hi, x))
  def wrap(i,x):
    return i.lo + (x - i.lo) % (i.hi - i.lo)
  def norm(i,x):
    return (x - i.lo) / (i.hi - i.lo + 10**-32)
  def ok(i,x):
    return i.lo <= x <= i.hi
  def fromHell(i,x,log,min=None,max=None):
    norm = i.norm if log.lo == None else log.norm
    hell = 1 if i.better == lt else 0
    return (hell - norm(x)) ** 2
"""

Note that many of the above will be called many times as we (e.g.) fill in the decisions
of a `can` (e.g. `guess`, `wrap`, `norm`) or its objectives (e.g. `fromHell`).
 
Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

"""
A = An = Less = About

def More(txt,*lst,**d):
  return About(txt,*lst,better=gt,**d)
"""

## The `Gadgets` Facade

Note that `Gadgets` stores most of the generic processing
of my optimizers. Hence the control params of `Gadgets`
is really the control params of most of the optimization.

"""
@setting
def GADGETS(): return  o(
    baseline=50,
    era=50,
    mutate = 0.3,
    epsilon=0.01,
    lives=5,
    verbose=True,
    nudge=1,
    patience=64
)
"""

Gadgets are created from a `model` (which is one of the  subclasses of `Candidate`). For exmaple

```
m = Gadgets(Schaffer())
```

Note the brackets after the model name-- this creates a new instance of that model.

"""
class Gadgets:
  def __init__(i,model):
    i.model  = model
    
  def blank(i):
    "Factory for candidate objects containing Nones"
    return i.model.clone(lambda _: None)
  
  def logs(i,also=None):
    "Factory for candidate objects containing Logs"
    new = i.model.clone(lambda _ : Log())
    for new1,also1 in new.alongWith(also):
        new1.also = also1
    return new
  
  def log1(i,can,log):
    "Stores values from 'can' into 'log'."
    [log1 + x for log1,x in log.alongWith(can)]
    
  def logNews(i,log, news):
    """Stores values from a list of cans, called 'news'
       into a log."""
    for can in news:
      for x,log1 in zip(can.decs,log.decs):
        log1 + x
      for x,log1 in zip(can.objs,log.objs):
        log1 + x
      log.aggregate + i.aggregate(can,log)
    return news
      
  def aFewBlanks(i):
    """ Handles instantiation with constraints.
        If can't  make  newinstance after some repeats, crash."""
    patience = the.GADGETS.patience
    while True:
      yield i.blank()
      patience -= 1
      assert patience > 0, "constraints too hard to satisfy"

  def decs(i):
    "return a new candidate, with guesses for decisions"
    for can in i.aFewBlanks():
      can.decs = [dec.maker() for dec in i.model.decs]
      if i.model.ok(can):
        return can
  
  def eval(i,can):
    "expire the old aggregate. make the objective scores."
    can.aggregate = None
    can.objs = [obj.maker(can) for obj in i.model.objs]
    return can

  def aggregate(i,can,logs):
    "Return the aggregate. Side-effect: store it in the can"
    if can.aggregate == None:
       agg = n = 0
       for obj,about,log in zip(can.objs,
                                i.model.objs,
                                logs.objs):
         n   += 1
         agg += about.fromHell(obj,log)
       can.aggregate = agg ** 0.5 / n ** 0.5
    return can.aggregate
       
  def mutate(i,can,logs,p):
    "Return a new can with p% mutated"
    for sn in i.aFewBlanks():
      for n,(dec,about,log) in enumerate(zip(can.decs,
                                           i.model.decs,
                                           logs.decs)):
        val = can.decs[n]
        if p > r():
          some = (log.hi - log.lo)*0.5
          val  = val - some + 2*some*r()
          val  = about.wrap(val)
        sn.decs[n] = val
      if i.model.ok(sn):
        return sn
      
  def xPlusFyz(i,threeMore,cr,f):
    "Crossovers some decisions, by a factor of 'f'"
    def smear((x1, y1, z1, about)):
      x1 = x1 if cr <= r() else x1 + f*(y1-z1)
      return about.wrap(x1)
    for sn in i.aFewBlanks():
      x,y,z   = threeMore()
      sn.decs = [smear(these)
                 for these in zip(x.decs,
                                  y.decs,
                                  z.decs,
                                  i.model.decs)]
      if i.model.ok(sn):
        return sn
    
  def news(i,n=None):
    "Generating, say, 100 random instances."
    return [i.eval( i.decs())
            for _ in xrange(n or the.GADGETS.baseline)]

  def energy(i,can,logs):
    "Returns an energy value to be minimized"
    i.eval(can)
    e = abs(1 - i.aggregate(can,logs))
    if e < 0: e= 0
    if e > 1: e= 1
    return e
  
  def better1(i,now,last):
    "Is one era better than another?"
    better=worse=0
    for now1,last1,about in zip(now.objs,
                                last.objs,
                                i.model.objs):
      nowMed = median(now1.some())
      lastMed= median(last1.some())
      if about.better(nowMed, lastMed):
        better += 1
      elif nowMed != lastMed:
        worse += 1
    return better > 0 and worse < 1
  
  def fyi(i,x)   :
    "Maybe, mention something"
    the.GADGETS.verbose and say(x)
    
  def shout(i,x) :
    "Add an emphasis to an output."
    i.fyi("__" + x)
    
  def bye(i,info,first,now) :
    """Optimizers return the distribution of values seen in
       first and final era"""
    i.fyi(info)
    return first,now
"""

## Optimizers

Finally, we can build our optimizers. Note that the following:

+ Process a model in `era`s
+ May stop early after a sequence of unpromising `era`s.
+ May stop early if we get too close to zero
+ Either create a baseline era or accepts a baseline `first` era
  passed in as a parameter.
+ When generating logs, if there is an outer log, store values in this
  log as well as the outer.

### Simulated Annealling

"""    
@setting
def SA(): return o(
    p=0.25,
    cooling=1,
    kmax=1000)
  
def sa(m,baseline=None,also2=None):
  def goodbye(x)  : return g.bye(x,first,now)
  g = Gadgets(m)
  def p(old,new,t): return ee**((old - new)/t)
  k,eb,life = 0,1,the.GADGETS.lives
  #===== setting up logs
  also     = g.logs(also2) # log of all eras
  first    = now  = g.logs(also)
  g.logNews(first,baseline or g.news())
  last, now  = now, g.logs(also)
  #===== ok to go
  s = g.decs()
  e = g.energy(s,now)
  g.fyi("%4s [%2s] %3s "% (k,life,"     "))
  while True:
    info="."
    k += 1
    t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
    sn = g.mutate(s, also,the.SA.p)
    en = g.energy(sn,also)
    g.log1(sn,now)
    if en < eb:
      sb,eb = sn,en
      g.shout("!")
    if en < e:
      s,e = sn,en
      info = "+"
    elif p(e,en,t) < r():
      s,e = sn, en
      info="?"
    if k % the.GADGETS.era: 
      g.fyi(info)
    else:
      life = life - 1
      if g.better1(now, last)     : life = the.GADGETS.lives 
      if life < 1                 : return goodbye("L")
      if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
      if k > the.SA.kmax          : return goodbye("K")
      g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
      last, now  = now, g.logs(also) 
"""

### Differential Evolution

"""
@setting
def DE(): return o(
    cr = 0.4,
    f  = 0.5,
    npExpand = 10,
    kmax=1000)
  
def de(m,baseline=None,also2=None):
  def goodbye(x)  : return g.bye(x,first,now)
  g  = Gadgets(m)
  np = len(g.model.decs) * the.DE.npExpand
  k,eb,life = 0,1,the.GADGETS.lives
  #===== setting up logs
  also     = g.logs(also2) # also = log of all eras
  first    = now  = g.logs(also)
  frontier = g.logNews(first,baseline or g.news(np))
  last, now  = now, g.logs(also)
  #===== ok to go
  sn = en = None
  g.fyi("%4s [%2s] %3s "% (k,life,"     "))
  while True:
    for n,parent in enumerate(frontier):
      info="."
      k += 1
      e  = g.aggregate(parent, also)
      sn = g.xPlusFyz(lambda: another3(frontier,parent),
                      the.DE.cr,
                      the.DE.f)
      en = g.energy(sn,also)
      g.log1(sn,now)
      if en < eb:
        sb,eb = sn,en
        g.shout("!")
      if en < e:
        frontier[n] = sn # goodbye parent
        info = "+"
      g.fyi(info)
    life = life - 1
    if g.better1(now, last)     : life = the.GADGETS.lives 
    if life < 1                 : return goodbye("L")
    if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
    if k > the.DE.kmax          : return goodbye("K")
    g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
    last, now  = now, g.logs(also) 
"""

DE trick for finding three unique things in a list that are not `avoid`.

"""
def another3(lst, avoid=None):
  def another1():
    x = avoid
    while id(x) in seen: 
      x = lst[  int(random.uniform(0,len(lst))) ]
    seen.append( id(x) )
    return x
  # -----------------------
  assert len(lst) > 4
  avoid = avoid or lst[0]
  seen  = [ id(avoid) ]
  return another1(), another1(), another1()

