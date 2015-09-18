[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



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
<a href="gadgets.py#L54-L65"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   import random
   2:   r   = random.random
   3:   isa = isinstance
   4:   
   5:   def seed(x=1):
   6:     random.seed(x)
   7:   
   8:   class o:
   9:     def __init__(i,**d)    : i.__dict__.update(d)
  10:     def __setitem__(i,k,v) : i.__dict__[k] = v
  11:     def __getitem__(i,k)   : return i.__dict__[k]
  12:     def __repr__(i)        : return 'o'+str(i.__dict__)
```

## Log

This class is the simplest of all.  It just remembers the range of values
seen so far.

<a href="gadgets.py#L74-L85"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  13:   class Log:
  14:     def __init__(i,also=None):
  15:       i.lo, i.hi, i.also = None, None, also
  16:     def __add__(i,x):
  17:       if   i.lo == None : i.lo = i.hi = x # auto-initialize
  18:       elif x > i.hi     : i.hi = x
  19:       else x < i.lo     : i.lo = x
  20:       if i.also:
  21:         i.also + x
  22:       return x
  23:     def norm(i,x):
  24:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
```

Note one small detail. Sometimes we are logging information
about one run as well as all runs. So `Log` has an `also` pointer
which, if non-nil, is another place to repeat the same information.

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L98-L100"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  25:   def Candidate(decs=[],objs=[]):
  26:     return o(dec=dec,objs=objs,
  27:              aggregate=None)
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="gadgets.py#L106-L116"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  28:   def Schaffer():
  29:     def f1(can):
  30:       x = can.decs[0]
  31:       return x**2
  32:     def f2(can):
  33:       x = can.decs[0]
  34:       return (x-2)**2
  35:     return Candidate(
  36:             decs = [Want("x",   lo = -4, hi = 4)],
  37:             objs = [Less("f1",  maker=f1),
  38:                     Less("f2", maker=f2)])
```

### Filling in the Candidates

+ Replace some template candidate with one `what` for each location. Useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

<a href="gadgets.py#L126-L137"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  39:   def none()        : return None
  40:   def log(also=None): return lambda: Log(also)
  41:   
  42:   def fill(x, what=none):
  43:     if   isa(x,list): return fillList(x,what)
  44:     elif isa(x,o)   : return fillContainer(x,what)
  45:     else            : return what()
  46:   
  47:   def fillList(lst,what):
  48:     return [ fill(x,what) for x in lst]
  49:   def fillContainer(old,what):
  50:     return o( **{ k : fill(d[k], what) for k in old } )
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

<a href="gadgets.py#L160-L175"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  51:   class Want(object):
  52:     def __init__(i, txt, init=None,
  53:                     lo=-10**32, hi=10**32,
  54:                     maker=None):
  55:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
  56:       i.maker = maker or i.guess
  57:     def __repr__(i):
  58:       return 'o'+str(i.__dict__)
  59:       def guess(i):
  60:       return i.lo + r()*(i.hi - i.lo)
  61:     def restrain(i,x):
  62:       return max(i.lo, min(i.hi, x))
  63:     def wrap(i,x):
  64:       return i.lo + (x - i.lo) % (i.hi - i.lo)
  65:     def ok(i,x):
  66:       return i.lo <= x <= i.hi
```

### Want Objectives?

Subclasses of `Want` store information about objectives 
including:

+ How to compute the distance `fromHell`.
+ When does one objective have a `better` value than another;

Here are out `better` predicates:

<a href="gadgets.py#L189-L190"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  67:   def lt(i,j): return i < j
  68:   def gt(i,j): return i > j
```

And these control our objectives as follows:

<a href="gadgets.py#L196-L209"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  69:   class Obj(Want):
  70:     def fromHelll(i,x,log):
  71:       hell = 1 if i.better == lt else 0
  72:       return (hell - log.norm(x)) ** 2
  73:     
  74:   class Less(Obj):
  75:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  76:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  77:       i.better = lt
  78:       
  79:   class More(Obj):
  80:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  81:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  82:       i.better = gt
```

## `Gadgets`: places to store lots of `Want`s

Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

<a href="gadgets.py#L224-L288"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  83:   class Gadgets:
  84:     def __init__(i,
  85:                  abouts, # e.g. Schaffer()
  86:                  also = None):
  87:       i.abouts = abouts
  88:       i.log    = fill(i.abouts, log(also))
  89:       
  90:     def blank(i):
  91:       "return a new candidate, filled with None"
  92:       return fill(i.abouts, none)
  93:     
  94:     def keepDecs(i)     : return i.decs(True)
  95:     def keepEval(i,can) : return i.eval(i,can,True)
  96:     def keepAggregate(i,can) : return i.aggregate(i,can,True)
  97:   
  98:     def decs(i,keep=False):
  99:       "return a new candidate, with guesses for decisions"
 100:       can = i.blank()
 101:       can.decs = [about.maker() for about in i.abouts.decs]
 102:       if keep:
 103:         [log + dec for log,dec in zip(i.log.decs,can.decs)]
 104:       return can
 105:     
 106:     def eval(i,c,keep=False):
 107:       "expire the old aggregate. make the objective scores."
 108:       can.aggregate = None:
 109:       can.objs = [about.maker(can) for about in i.abouts.objs]
 110:       if keep:
 111:         [log + obj for log,obj in zip(i.log.objs, can.objs]
 112:       return can
 113:   
 114:     def aggregate(i,can,keep=False):
 115:       "Return the aggregate. Side-effect: store it in the can"
 116:       if can.aggregate == None:
 117:          agg = n = 0
 118:          for obj,about,log in zip(c.objs,
 119:                                   i.abouts.objs,
 120:                                   i.log.objs):
 121:            n   += 1
 122:            agg += about.fromHell(obj,log)
 123:          can.aggregate = agg ** 0.5 / n ** 0.5
 124:          if keep:
 125:            i.abouts.aggregate += can.aggregate
 126:       return can.aggregate
 127:          
 128:     def mutate(i,can,p):
 129:       "Return a new can with p% mutated"
 130:       can1= i.blank()
 131:       for n,(dec,about) in enumerate(zip(can.decs,i.about.decs)):
 132:         can1.decs[n] = about.maker() if p > r() else dec
 133:       return can1
 134:     
 135:     def baseline(i,n=100):
 136:       "Log the results of generating, say, 100 random instances."
 137:       for _ in xrange(n):
 138:         can = i.keepEval( i.keepDecs() )
 139:         i.keepAggregate(can)
 140:         return can
 141:   
 142:   
 143:   def sa(m,
 144:          p=0.3, cooling=1,kmax=1000,e[silon=10.1,era=100,lives=5): # e.g. sa(Schafer())
 145:          k, life, e = 1,lives,1e32):
 146:   
 147:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

