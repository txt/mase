from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from ok import *

"""# Domain-Specific Languages (in Python)

This files shows an example of a small object-based DSL (domain-specific language) in Python.
In the language, all the tedious stuff is implemented in superclasses, letting
users express their knowledge in simple succinct subclasses.

The example here will be compartmental modeling and is
 adapted from some  excellent code from
[Abraham Flaxman](https://gist.github.com/aflaxman/4121076#file-sdm_diaper_delivery-ipynb).

## Theory

Does your language pass the _elbow test_? Do your business users elbow you of the way
in their haste to fix what is obviously wrong with your code?

No?  Then you obviously:

+ You are not speaking their language. 
+ You've lost that an
entire community that might have been able to audit,
verify, and evolve your code.

Enter domain-specific languages (DSLs). DSLs have also been called:

+ [little languages](http://staff.um.edu.mt/afra1/seminar/little-languages.pdf);
+ micro-languages,
+ application languages,
+ very high level languages.

Example DSLs:

+ SQL
+ AWK (unix text reporting language)

DSLs are useful since
different representations of the same concepts can make certain inferences easier. Here's Douglas
Hofstadter from his book _Godel, Esher, Bach:_

+  When you confront a (system) that you know nothing of,... your problem is how to assign interpretations to its symbols in a meaningful way...:

     + You may make several tentative stabs in the dark before finding a good set of words to associate with the symbols.
     + It is very similar to attempts to crack a code, or to decipher inscriptions in an unknown language...
     + When you hit a right choice... all of a sudden things just feel right, and work speeds up enormously.
     + Pretty soon everything falls into place."

Here's James Martin from his book _Design of Real-time Computer Systems_:

+ We must develop languages that the scientist, the architect, the teacher, and the layman can use without being computer experts.
   + The language for each user must be as natural as possible to him.
   + The statistician must talk to his terminal in the language of statistics.
   + The civil engineer must use the language of civil engineering.
   + When a man (sic) learns his profession he must learn the problem-oriented languages to go with that profession.

A DSL is a very high-level language that a user can learn and use in less than a day. Such productivity can only be achieved by tailoring the language to the special needs and skills of a particular class of users in a particular domain.
So one way to find DSL is listen to experts in some field commenting on their processing. Often that processing
has repeated domain-specific idioms:

+ Idioms= Methods imposed by programmers to handle common forms, procedures.
+ E.g. Ensure data is saved before the window is closed.
+ E.g. Before conducting expensive tests, perform cheap tests that can rule out need for expensive tests.

In a DSL-based software development process, the analyst:

+ Identifies the users and their tasks;
+ Identifies the common idioms used by those users;
+ Invents a little language to handle those idioms;
+ Generates sample sentences in that language;
+ Shows those sentences to the user and trains them how to write their own.

That is, instead of the analyst writing the application, the analysts writes tools that let a user community write and maintain their own knowledge.


The benefits of DSL (productivity, explanatory, ownership by the users) can be out-weighed by the cost of building the DSL.  Most expensive way of building  a DSL:

+ Full-blown YACC/LEX parser

Simpler:

+ Code the idioms in general superclasses;
+ Leave the domain-specific stuff for subclasses/

For example....

## SAF: Stock and Flow (Compartmental Modeling in Python)

From Wikipedia:

+ Economics, business, accounting, and related
  fields often distinguish between quantities that are
_stocks_ and those that are _flows_. These differ in
their units of measurement. 
   + A stock variable is
measured at one specific time, and represents a
quantity existing at that point in time (say,
December 31, 2004), which may have accumulated in
the past. 
   + A flow variable is measured over an
interval of time. Therefore a flow would be measured
per unit of time (say a year). Flow is roughly
analogous to rate or speed in this sense.
+ Examples:
    + A person or country might have stocks of money, financial assets, liabilities, wealth, real means of production, capital, inventories, and human capital (or labor power). 
    + Flow magnitudes include income, spending, saving, debt repayment, fixed investment, inventory investment, and labor utilization.These differ in their units of measurement.
+ Formally:
    + A stock (or "level variable") in this broader sense is some entity that is accumulated over time by inflows and/or depleted by outflows. Stocks can only be changed via flows. Mathematically a stock can be seen as an accumulation or integration of flows over time – with outflows subtracting from the stock. Stocks typically have a certain value at each moment of time – e.g. the number of population at a certain moment.
    +  flow (or "rate") changes a stock over time. Usually we can clearly distinguish inflows (adding to the stock) and outflows (subtracting from the stock). Flows typically are measured over a certain interval of time – e.g., the number of births over a day or month.

For practical purposes, it may be necessary to add _auxillary variables_ to handle some intermediaries (so, in the following,
we can see _nominal productivity_).

![Brooks](img/brookslaw.png)

So, in the following code, look for

```python
F,A,S = Flow, Aux, Stock
```

## Example: Diapers


```
 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 

C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers
```

"""
import random
r   = random.random
isa = isinstance

class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def has(i)             : return i.__dict__
  def keys(i)            : return i.has().keys()
  def items(i)           : return i.has().items()
  def __init__(i,**d)    : i.has().update(d)
  def __setitem__(i,k,v) : i.has()[k] = v
  def __getitem__(i,k)   : return i.has()[k]
  def __repr__(i)        : return 'o'+str(i.has())
  def copy(i): 
      j = o()
      for k in i.has(): j[k] = i[k]
      return j
  def asList(i,keys=[]):
    keys = keys or i.keys()
    return [i[k] for k in keys]
      
class Has:
  def __init__(i,init,lo=0,hi=100):
    i.init,i.lo,i.hi = init,lo,hi
  def restrain(i,x):
    return max(i.lo, 
               min(i.hi, x))
  def rank(i):
    if isa(i,Flow) : return 3
    if isa(i,Stock): return 1
    if isa(i,Aux)  : return 2
  def __repr__(i):
    return str(dict(what=i.__class__.__name__,
                name= i.name,init= i.init,
                 lo  = i.lo,  hi  = i.hi))
                 
class Flow(Has) : pass
class Stock(Has): pass
class Aux(Has)  : pass

S,A,F = Stock,Aux,Flow

class Model:
  def about(i):
    tmp=i.have()
    for k,v in tmp.has().items():
      v.name = k
    return tmp 
  def run(i,dt=1,tmax=30): 
    r()
    t,b4, keep  = 0, o(), []
    about = i.about()
    keys  = sorted(about.keys(), 
                   key=lambda z: about[z].rank())
    for k,a in about.items(): 
      b4[k] = a.init
    keep = [["t"] +  keys,
            [0] + b4.asList(keys)]
    while t < tmax:
      now = b4.copy()
      i.step(dt,t,b4,now)
      for k in about.keys(): 
        now[k] = about[k].restrain(now[k])
      keep += [[t] + now.asList(keys)]
      t += dt
      b4 = now
    return keep

def printm(matrix,less=True):
   """Print a list of list, only showing changes
   in each column (if less is True)."""
   def ditto(m,mark="."):
     def worker(lst):
       out = []
       for i,now in enumerate(lst):
         before = old.get(i,None) # get old it if exists
         out += [mark if before == now else now]
         old[i] = now # next time, 'now' is the 'old' value
       return out # the lst with ditto marks inserted
     old = {}
     return [worker(row) for row in m]
   matrix = ditto(matrix) if less else matrix
   s = [[str(e) for e in row] for row in matrix]
   lens = [max(map(len, col)) for col in zip(*s)]
   fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
   for row in [fmt.format(*row) for row in s]:
      print(row)

class Diapers(Model):
  def have(i):
    return o(C = S(100), D = S(0),
             q = F(0),  r = F(8), s = F(0))
  def step(i,dt,t,u,v):
    def saturday(x): return int(x) % 7 == 6
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70  if saturday(t) else 0 
    v.s  =  u.D if saturday(t) else 0
    if t == 27: # special case (the day i forget)
      v.s = 0

@ok
def _diapers1():
  printm(Diapers().run())
