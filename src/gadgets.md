[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



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

<a href="gadgets.py#L67-L102"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Log:
   2:     def __init__(i,init=[],also=None):
   3:       i.lo, i.hi, i.also, i._some= None, None, also,Some()
   4:       map(i.__add__,init)
   5:     def __add__(i,x):
   6:       if   i.lo == None : i.lo = i.hi = x # auto-initialize
   7:       elif x > i.hi     : i.hi = x
   8:       elif x < i.lo     : i.lo = x
   9:       if i.also:
  10:         i.also + x
  11:       i._some += x
  12:       return x
  13:     def some(i):
  14:       return i._some.any
  15:     def tiles(i,tiles=None,ordered=False,n=3):
  16:       return r3(ntiles(i.some(),tiles,ordered),n)
  17:     def norm(i,x):
  18:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  19:   
  20:   @setting
  21:   def SOMES(): return o(
  22:       size=256
  23:       )
  24:   
  25:   class Some:
  26:     def __init__(i, max=None): 
  27:       i.n, i.any = 0,[]
  28:       i.max = max or the.SOMES.size
  29:     def __iadd__(i,x):
  30:       i.n += 1
  31:       now = len(i.any)
  32:       if now < i.max:    
  33:         i.any += [x]
  34:       elif r() <= now/i.n:
  35:         i.any[ int(r() * now) ]= x 
  36:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L111-L113"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  37:   def Candidate(decs=[],objs=[]):
  38:     return o(decs=decs,objs=objs,
  39:              aggregate=None)
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="gadgets.py#L119-L158"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  40:   def Schaffer():
  41:     def f1(can):
  42:       x = can.decs[0]
  43:       return x**2
  44:     def f2(can):
  45:       x = can.decs[0]
  46:       return (x-2)**2
  47:     return Candidate(
  48:             decs = [Want("x",   lo = -10**5, hi = 10**5)],
  49:             objs = [Less("f1",  maker=f1),
  50:                     Less("f2", maker=f2)])
  51:   
  52:   def Fonseca(n=3):
  53:     def f1(can):
  54:       z = sum((x - 1/sqrt(n))**2 for x in can.decs)
  55:       return 1 - ee**(-1*z)
  56:     def f2(can):
  57:       z = sum((x + 1/sqrt(n))**2 for x in can.decs)
  58:       return 1 - ee**(-1*z)
  59:     def dec(x):
  60:       return Want(x, lo=-4, hi=4)
  61:     return Candidate(
  62:             decs = [dec(x) for x in range(n)],
  63:             objs = [Less("f1",  maker=f1),
  64:                     Less("f2",  maker=f2)])
  65:   
  66:   def Kursawe(a=1,b=1):
  67:     def f1(can):
  68:       def xy(x,y):
  69:         return -10*ee**(-0.2*sqrt(x*x + y*y))
  70:       a,b,c = can.decs
  71:       return xy(a,b) + xy(b,c)
  72:     def f2(can):
  73:       return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  74:     def dec(x):
  75:       return Want(x, lo=-5, hi=5)            
  76:     return Candidate(
  77:              decs = [dec(x) for x in range(3)],
  78:              objs = [Less("f1",  maker=f1),
  79:                      Less("f2",  maker=f2)])
```

## Candidates have the Same Shape as `Log`s and `Want`s

Candidates can be used as templates by
replace some template candidate with one `what` for each location. 
This is useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

<a href="gadgets.py#L170-L181"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  80:   def none() : return None
  81:   def log()  : return Log
  82:   
  83:   def fill(x, what=none):
  84:     if   isa(x,list): return fillList(x,what)
  85:     elif isa(x,o)   : return fillContainer(x,what)
  86:     else            : return what()
  87:   
  88:   def fillList(lst,what):
  89:     return [ fill(x,what) for x in lst]
  90:   def fillContainer(old,what):
  91:     return o( **{ k : fill(old[k], what) for k in old.__dict__ } )
```

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

<a href="gadgets.py#L205-L228"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  92:   def lt(i,j): return i < j
  93:   def gt(i,j): return i > j
  94:   
  95:   class Want(object):
  96:     def __init__(i, txt, init=None,
  97:                     lo=-10**32, hi=10**32,
  98:                     better=lt,
  99:                     maker=None):
 100:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 101:       i.maker = maker or i.guess
 102:       i.better= better
 103:     def __repr__(i):
 104:       return 'o'+str(i.__dict__)
 105:     def guess(i):
 106:       return i.lo + r()*(i.hi - i.lo)
 107:     def restrain(i,x):
 108:       return max(i.lo, min(i.hi, x))
 109:     def wrap(i,x):
 110:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 111:     def ok(i,x):
 112:       return i.lo <= x <= i.hi
 113:     def fromHell(i,x,log):
 114:       hell = 1 if i.better == lt else 0
 115:       return (hell - log.norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L235-L238"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 116:   Less=Want
 117:   
 118:   def More(txt,*lst,**d):
 119:     return Want(txt,*lst,better=gt,**d)
```

## `Gadgets`: places to store lots of `Want`s

Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

<a href="gadgets.py#L253-L322"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 120:   @setting
 121:   def GADGETS(): return  o(
 122:       baseline=100,
 123:       mutate = 0.3
 124:   )
 125:   
 126:   class Gadgets:
 127:     def __init__(i,
 128:                  abouts):
 129:       i.abouts = abouts
 130:       i.log    = fill(i.abouts, log())
 131:       
 132:     def blank(i):
 133:       "return a new candidate, filled with None"
 134:       return fill(i.abouts, none)
 135:     
 136:     def keepDecs(i)     : return i.decs(True)
 137:     def keepEval(i,can) : return i.eval(can,True)
 138:     def keepAggregate(i,can) : return i.aggregate(can,True)
 139:     def keeps(i,keeps,logs,things)  :
 140:       if keeps:
 141:         for log,thing in zip(logs,things):
 142:           log + thing
 143:         
 144:     def decs(i,keep=False):
 145:       "return a new candidate, with guesses for decisions"
 146:       can = i.blank()
 147:       can.decs = [about.maker() for about in i.abouts.decs]
 148:       i.keeps(keep,i.log.decs,can.decs)
 149:       return can
 150:     
 151:     def eval(i,can,keep=False):
 152:       "expire the old aggregate. make the objective scores."
 153:       can.aggregate = None
 154:       can.objs = [about.maker(can) for about in i.abouts.objs]
 155:       i.keeps(keep,i.log.objs,can.objs)
 156:       return can
 157:   
 158:     def aggregate(i,can,keep=False):
 159:       "Return the aggregate. Side-effect: store it in the can"
 160:       if can.aggregate == None:
 161:          agg = n = 0
 162:          for obj,about,log in zip(can.objs,
 163:                                   i.abouts.objs,
 164:                                   i.log.objs):
 165:            n   += 1
 166:            agg += about.fromHell(obj,log)
 167:          can.aggregate = agg ** 0.5 / n ** 0.5
 168:          if keep:
 169:            i.log.aggregate + can.aggregate
 170:       return can.aggregate
 171:          
 172:     def mutate(i,can,p=None,keep=False):
 173:       "Return a new can with p% mutated"
 174:       if p is None: p = the.GADGETS.mutate
 175:       can1= i.blank()
 176:       for n,(dec,about) in enumerate(zip(can.decs,
 177:                                          i.abouts.decs)):
 178:         can1.decs[n] = about.maker() if p > r() else dec
 179:       i.keeps(keep,i.log.decs,can1.decs)
 180:       return can1
 181:     
 182:     def baseline(i,n=None):
 183:       "Log the results of generating, say, 100 random instances."
 184:       for j in xrange(n or the.GADGETS.baseline):
 185:         can = i.keepEval( i.keepDecs() )
 186:         i.keepAggregate(can)
 187:         
 188:   
 189:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

