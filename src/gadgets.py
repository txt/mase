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
from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from gadgets0 import *

"""

# GADGETS: Timm's Generic Optimizer Gadgets (and Goodies)

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
+ The syntax of the Python class system is sometimes...
  awful. I find I can do cleaner coding if I dodge it.

## Log

This class is the simplest of all.  It just remembers the range of values
seen so far.

Note two small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 
+ As a side-effect of logging, we also keep a small sample of
  the logged items. This will come in handy... later.

"""
class Log:
  def __init__(i,init=[],also=None):
    i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
    map(i.__add__,init)
  def __add__(i,x):
    i.n += 1
    if   i.empty() : i.lo = i.hi = x # auto-initialize
    elif x > i.hi     : i.hi = x
    elif x < i.lo     : i.lo = x
    if i.also:
      i.also + x
    i._some += x
    return x
  def some(i):
    return i._some.any
  def tiles(i,tiles=None,ordered=False,n=3):
    return r3(ntiles(i.some(),tiles,ordered),n)
  def empty(i):
    return i.lo == None
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 10**-32)

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

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

"""        
class Candidate(object):
  def __init__(i,decs=[],objs=[]):
    i.decs,i.objs=decs,objs
    i.aggregate=None
    i.abouts = i.about()
  def __getitem__(i,key):
    return i.__dict__[key]
  def ok(i,can): return True
  def about(i): True
  def __repr__(i):
    return printer(i,decs=i.decs,
                   objs=i.objs,
                   aggregated=i.aggregate)
  def clone(i,what = lambda _: None):
    j      = object.__new__(i.__class__)
    j.decs = [what(x) for x in i.decs]
    j.objs = [what(x) for x in i.objs]
    j.aggregate = what(i.aggregate)
    return j
  def alongWith(i,j=None):
    "convenient iterator."
    if j:
      for one,two in zip(i.decs, j.decs):
        yield one,two
      for one,two in zip(i.objs, j.objs):
        yield one,two
      yield i.aggregate, j.aggregate
"""

Example model (note the use of the `want`, `less` and `more` classes... defined below).

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

class ZDT1(Candidate):
  n=30
  def about(i):
    def f1(can): return can.decs[0]
    def f2(can):
      g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
      return g*abs(1 - sqrt(can.decs[0]*g))
    def dec(x):
      return An(x,lo=0,hi=1)
    i.decs = [dec(x) for x in range(ZDT1.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2)]
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

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

"""
A = An = Less = About

def More(txt,*lst,**d):
  return About(txt,*lst,better=gt,**d)
"""

## `Gadgets`: places to store lots of `Want`s

`Gagets` is really a farcade containing a bunch of services
useful for sa, mws, de, general GAs, etc. It was a toss of a coin
to make it either:

- a superclass of those optimizers or 
- a separate class that associated with the optimizers. 

In the end,
I went with the subclass approach (but I acknowledge that that
decision is somewhat arbitrary).


Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

"""
@setting
def GADGETS(): return  o(
    baseline=50,
    mutate = 0.3,
    epsilon=0.01,
    era=50,
    lives=5,
    verbose=True,
    nudge=1
)

class Gadgets:
  def __init__(i,model):
    i.my  = model
    
  def blank(i):
    "return a new candidate, filled with None"
    return i.my.clone(lambda _: None)
  def logs(i,also=None):
    "Return a new log, also linked to another log"
    new = i.my.clone(lambda _ : Log())
    for new1,also1 in new.alongWith(also):
        new1.also = also1
    return new
  def log1(i,can,log):
     [log1 + x for log1,x in log.alongWith(can)]
  def logNews(i,log, news):
    for can in news:
      for x,log1 in zip(can.decs,log.decs):
        log1 + x
      for x,log1 in zip(can.objs,log.objs):
        log1 + x
      log.aggregate + i.aggregate(can,log)
  def decs(i):
    "return a new candidate, with guesses for decisions"
    can = i.blank()
    can.decs = [dec.maker() for dec in i.my.decs]
    return can
  
  def eval(i,can):
    "expire the old aggregate. make the objective scores."
    can.aggregate = None
    can.objs = [obj.maker(can) for obj in i.my.objs]
    return can

  def aggregate(i,can,logs):
    "Return the aggregate. Side-effect: store it in the can"
    if can.aggregate == None:
       agg = n = 0
       for obj,about,log in zip(can.objs,
                                i.my.objs,
                                logs.objs):
         n   += 1
         agg += about.fromHell(obj,log)
       can.aggregate = agg ** 0.5 / n ** 0.5
    return can.aggregate
       
  def mutate(i,can,logs,p=None,f=None):
    "Return a new can with p% mutated"
    if p is None: p = the.GADGETS.mutate
    if f is None: f = the.GADGETS.nudge
    can1= i.blank()
    for n,(dec,about,log) in enumerate(zip(can.decs,
                                           i.my.decs,
                                           logs.decs)):
      val   = can.decs[n]
      if p > r():
         some  = (log.hi - log.lo)*0.5
         val   = val - some + 2*some*r()
         val   = about.wrap(val)
      can1.decs[n] = val
    return can1
  
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
    better=worse=0
    for now1,last1,about in zip(now.objs,
                                last.objs,
                                i.my.objs):
      nowMed = median(now1.some())
      lastMed= median(last1.some())
      if about.better(nowMed, lastMed):
        better += 1
      elif nowMed != lastMed:
        worse += 1
    return better > 0 and worse < 1
  def fyi(i,x)   : the.GADGETS.verbose and say(x)
  def shout(i,x) : i.fyi("__" + x)
  def bye(i,info,first,now) : i.fyi(info); return first,now

@setting
def SA(): return o(
    p=0.25,
    cooling=1,
    kmax=1000)
  
def sa(m,also=None,baseline=None):
  g = Gadgets(m)
  def p(old,new,t): return ee**((old - new)/t)
  def goodbye(x)  : return g.bye(x,first,now)
  k,eb,life, = 0,1,the.GADGETS.lives
  #===== setting up logs
  also     = also or g.logs()
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
    sn = g.mutate(s, also, the.GADGETS.mutate)
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
      if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
      if life < 1                 : return goodbye("L")
      if k > the.SA.kmax          : return goodbye("K")
      g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
      last, now  = now, g.logs(also) 

