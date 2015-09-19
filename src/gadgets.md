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


## Log

This class is the simplest of all.  It just remembers the range of values
seen so far.

Note two small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 
+ As a side-effect of logging, we also keep a small sample of
  the logged items. This will come in handy... later.

<a href="gadgets.py#L66-L98"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Log:
   2:     def __init__(i,also=None):
   3:       i.lo, i.hi, i.also, i._some= None, None, also,Some()
   4:     def __add__(i,x):
   5:       if   i.lo == None : i.lo = i.hi = x # auto-initialize
   6:       elif x > i.hi     : i.hi = x
   7:       elif x < i.lo     : i.lo = x
   8:       if i.also:
   9:         i.also + x
  10:       i._some += x
  11:       return x
  12:     def some(i):
  13:       return i._some.any
  14:     def norm(i,x):
  15:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  16:   
  17:   @setting
  18:   def somes(): return o(
  19:       size=256
  20:       )
  21:   
  22:   class Some:
  23:     def __init__(i, max=None): 
  24:       i.n, i.any = 0,[]
  25:       i.max = max or the.somes.size
  26:     def __iadd__(i,x):
  27:       i.n += 1
  28:       now = len(i.any)
  29:       if now < i.max:    
  30:         i.any += [x]
  31:       elif r() <= now/i.n:
  32:         i.any[ int(r() * now) ]= x 
  33:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L107-L109"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  34:   def Candidate(decs=[],objs=[]):
  35:     return o(decs=decs,objs=objs,
  36:              aggregate=None)
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="gadgets.py#L115-L125"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  37:   def Schaffer():
  38:     def f1(can):
  39:       x = can.decs[0]
  40:       return x**2
  41:     def f2(can):
  42:       x = can.decs[0]
  43:       return (x-2)**2
  44:     return Candidate(
  45:             decs = [Want("x",   lo = -4, hi = 4)],
  46:             objs = [Less("f1",  maker=f1),
  47:                     Less("f2", maker=f2)])
```

## Candidates have the Same Shape as `Log`s and `Want`s

Candidates can be used as templates by
replace some template candidate with one `what` for each location. 
This is useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

<a href="gadgets.py#L137-L148"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  48:   def none()        : return None
  49:   def log(also=None): return lambda: Log(also)
  50:   
  51:   def fill(x, what=none):
  52:     if   isa(x,list): return fillList(x,what)
  53:     elif isa(x,o)   : return fillContainer(x,what)
  54:     else            : return what()
  55:   
  56:   def fillList(lst,what):
  57:     return [ fill(x,what) for x in lst]
  58:   def fillContainer(old,what):
  59:     return o( **{ k : fill(old[k], what) for k in old.__dict__ } )
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

<a href="gadgets.py#L172-L195"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  60:   def lt(i,j): return i < j
  61:   def gt(i,j): return i > j
  62:   
  63:   class Want(object):
  64:     def __init__(i, txt, init=None,
  65:                     lo=-10**32, hi=10**32,
  66:                     better=lt,
  67:                     maker=None):
  68:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
  69:       i.maker = maker or i.guess
  70:       i.better= better
  71:     def __repr__(i):
  72:       return 'o'+str(i.__dict__)
  73:     def guess(i):
  74:       return i.lo + r()*(i.hi - i.lo)
  75:     def restrain(i,x):
  76:       return max(i.lo, min(i.hi, x))
  77:     def wrap(i,x):
  78:       return i.lo + (x - i.lo) % (i.hi - i.lo)
  79:     def ok(i,x):
  80:       return i.lo <= x <= i.hi
  81:     def fromHelll(i,x,log):
  82:       hell = 1 if i.better == lt else 0
  83:       return (hell - log.norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L202-L205"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  84:   Less=Want
  85:   
  86:   def More(txt,*lst,**d):
  87:     return Want(txt,*lst,better=gt,**d)
```

## `Gadgets`: places to store lots of `Want`s

Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

<a href="gadgets.py#L220-L287"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  88:   @setting
  89:   def gadgets(): return  o(
  90:       baseline=100)
  91:   
  92:   
  93:   class Gadgets:
  94:     def __init__(i,
  95:                  abouts, # e.g. Schaffer()
  96:                  also = None):
  97:       i.abouts = abouts
  98:       i.log    = fill(i.abouts, log(also))
  99:       
 100:     def blank(i):
 101:       "return a new candidate, filled with None"
 102:       return fill(i.abouts, none)
 103:     
 104:     def keepDecs(i)     : return i.decs(True)
 105:     def keepEval(i,can) : return i.eval(i,can,True)
 106:     def keepAggregate(i,can) : return i.aggregate(i,can,True)
 107:     def keeps(i,keep,logs,things)  :
 108:       if keep:
 109:         for log,thing in zip(logs,things):
 110:           log + thing
 111:         
 112:     def decs(i,keep=False):
 113:       "return a new candidate, with guesses for decisions"
 114:       can = i.blank()
 115:       can.decs = [about.maker() for about in i.abouts.decs]
 116:       i.keeps(keep,i.log.decs,can.decs)
 117:       return can
 118:     
 119:     def eval(i,c,keep=False):
 120:       "expire the old aggregate. make the objective scores."
 121:       can.aggregate = None
 122:       can.objs = [about.maker(can) for about in i.abouts.objs]
 123:       i.keeps(keep,i.log.objs,can.objs)
 124:       return can
 125:   
 126:     def aggregate(i,can,keep=False):
 127:       "Return the aggregate. Side-effect: store it in the can"
 128:       if can.aggregate == None:
 129:          agg = n = 0
 130:          for obj,about,log in zip(c.objs,
 131:                                   i.abouts.objs,
 132:                                   i.log.objs):
 133:            n   += 1
 134:            agg += about.fromHell(obj,log)
 135:          can.aggregate = agg ** 0.5 / n ** 0.5
 136:          if keep:
 137:            i.abouts.aggregate += can.aggregate
 138:       return can.aggregate
 139:          
 140:     def mutate(i,can,p,keep=False):
 141:       "Return a new can with p% mutated"
 142:       can1= i.blank()
 143:       for n,(dec,about) in enumerate(zip(can.decs,i.about.decs)):
 144:         can1.decs[n] = about.maker() if p > r() else dec
 145:       i.keeps(keep,i.log.decs,can1.decs)
 146:       return can1
 147:     
 148:     def baseline(i,n=None):
 149:       "Log the results of generating, say, 100 random instances."
 150:       for _ in xrange(n or the.gadgets.baseline):
 151:         can = i.keepEval( i.keepDecs() )
 152:         i.keepAggregate(can)
 153:         return can
 154:   
 155:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

