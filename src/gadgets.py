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
def Candidate(decs=[],objs=[]):
  return o(decs=decs,objs=objs,
           aggregate=None)

def canCopy(can,
                  what = lambda : None):
  copy= Candidate()
  copy.decs = [what() for _ in can.decs]
  copy.objs = [what() for _ in can.objs]
  copy.aggregate = what()
  return copy

def parts(can1=None,can2=None):
  "convince iterator. used later"
  if can1 and can2:
    for one,two in zip(can1.decs, can2.decs):
      yield one,two
    for one,two in zip(can1.objs, can2.objs):
      yield one,two
    yield can1.aggregate, can2.aggregate
"""

Example model (note the use of the `want`, `less` and `more` classes... defined below).
s
"""
def Schaffer():
  def f1(can):
    x = can.decs[0]
    return x**2
  def f2(can):
    x = can.decs[0]
    return (x-2)**2
  return Candidate(
          decs = [Want("x",   lo = -10**5, hi = 10**5)],
          objs = [Less("f1",  maker=f1),
                  Less("f2", maker=f2)])

def Fonseca(n=3):
  def f1(can):
    z = sum((x - 1/sqrt(n))**2 for x in can.decs)
    return 1 - ee**(-1*z)
  def f2(can):
    z = sum((x + 1/sqrt(n))**2 for x in can.decs)
    return 1 - ee**(-1*z)
  def dec(x):
    return Want(x, lo=-4, hi=4)
  return Candidate(
          decs = [dec(x) for x in range(n)],
          objs = [Less("f1",  maker=f1),
                  Less("f2",  maker=f2)])

def Kursawe(a=1,b=1):
  def f1(can):
    def xy(x,y):
      return -10*ee**(-0.2*sqrt(x*x + y*y))
    a,b,c = can.decs
    return xy(a,b) + xy(b,c)
  def f2(can):
    return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  def dec(x):
    return  Want(x, lo=-5, hi=5)           
  return Candidate(
           decs = [dec(x) for x in range(3)],
           objs = [Less("f1",  maker=f1),
                   Less("f2",  maker=f2)])

def ZDT1(n=30):
  def f1(can): return can.decs[0]
  def f2(can):
    g = 1 + 9*sum(x for x in can.decs[1:] )/(n-1)
    return g*abs(1 - sqrt(can.decs[0]*g))
  def dec(x):
    return Want(x,lo=0,hi=1)
  return Candidate(
    decs=[dec(x) for x in range(n)],
    objs=[Less("f1",maker=f1),
          Less("f2",maker=f2)])
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

class Want(object):
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
  def ok(i,x):
    return i.lo <= x <= i.hi
  def fromHell(i,x,log):
    hell = 1 if i.better == lt else 0
    return (hell - log.norm(x)) ** 2
"""

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

"""
Less=Want

def More(txt,*lst,**d):
  return Want(txt,*lst,better=gt,**d)
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
@setting
def GADGETS(): return  o(
    baseline=100,
    mutate = 0.3
)

class Gadgets:
  def __init__(i,
               abouts):
    i.abouts = abouts
    
  def blank(i):
    "return a new candidate, filled with None"
    return canCopy(i.abouts, lambda: None)
  def logs(i,also=None):
    "Return a new log, also linked to another log"
    new = canCopy(i.abouts, lambda: Log())
    for new1,also1 in parts(new,also):
        new1.also = also1
    return new
  def decs(i):
    "return a new candidate, with guesses for decisions"
    can = i.blank()
    can.decs = [about.maker() for about in i.abouts.decs]
    return can
  
  def eval(i,can):
    "expire the old aggregate. make the objective scores."
    can.aggregate = None
    can.objs = [about.maker(can) for about in i.abouts.objs]
    return can

  def aggregate(i,can,logs):
    "Return the aggregate. Side-effect: store it in the can"
    if can.aggregate == None:
       agg = n = 0
       for obj,about,log in zip(can.objs,
                                i.abouts.objs,
                                logs.objs):
         n   += 1
         if not log.empty():
           agg += about.fromHell(obj,log)
       can.aggregate = agg ** 0.5 / n ** 0.5
    return can.aggregate
       
  def mutate(i,can,p=None):
    "Return a new can with p% mutated"
    if p is None: p = the.GADGETS.mutate
    can1= i.blank()
    for n,(dec,about) in enumerate(zip(can.decs,
                                       i.abouts.decs)):
      can1.decs[n] = about.maker() if p > r() else dec
    return can1
  
  def baseline(i,logs,n=None):
    "Log the results of generating, say, 100 random instances."
    frontier = []
    for j in xrange(n or the.GADGETS.baseline):
      can = i.eval( i.decs() )
      i.aggregate(can,logs)
      [log + x for log,x in parts(logs,can)]
      frontier += [can]
    return frontier
  def energy(i,can,logs):
    "Returns an energy value to be minimized"
    i.eval(can)
    return 1 - i.aggregate(can,logs)
  def better1(i,now,last):
    better=worse=0
    for now1,last1,about in zip(now.objs,
                                last.objs,
                                i.abouts.objs):
      nowMed = median(now1.some())
      lastMed= median(last1.some())
      if about.better(nowMed, lastMed):
        better += 1
      elif nowMed != lastMed:
        worse += 1
    return better > 0 and worse < 1

@setting
def SA(): return o(
    p=0.25,
    cooling=1,
    kmax=1000,
    epsilon=0.01,
    era=50,
    lives=5,
    verbose=True)
  
class sa(Gadgets):
  def fyi(i,x)        : the.SA.verbose and say(x)  
  def bye(i,info,first,now) : i.fyi(info); return first,now
  def p(i,old,new,t)  : return ee**((old - new)/t)
  def run(i):
    k,eb,life, = 0,1,the.SA.lives
    also = i.logs()
    first = now  = i.logs(also)
    i.baseline(now, the.SA.era)
    last, now = now, i.logs(also)
    s    = i.decs()
    e    = i.energy(s,now)
    i.fyi("%4s [%2s] %3s "% (k,life,"     "))
    while True:
      info="."
      k += 1
      t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
      sn = i.mutate(s, the.SA.p)
      en = i.energy(sn,also)
      [log + x for log,x in parts(now,sn)]
      if en < eb:
        sb,eb = sn,en
        i.fyi("\033[7m!\033[m")
      if en < e:
        s,e = sn,en
        info = "+"
      elif i.p(e,en,t) < r():
         s,e = sn, en
         info="?"
      if k % the.SA.era: 
        i.fyi(info)
      else:
        life = life - 1
        if i.better1(now, last): 
          life = the.SA.lives 
        if eb < the.SA.epsilon :
          return i.bye("E %.5f" %eb,first,now)
        if life < 1 :
          return i.bye("L", first,now)
        if k > the.SA.kmax :
          return i.bye("K", first,now)
        i.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
        last, now  = now, i.logs(also) 

