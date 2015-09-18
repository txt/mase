[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# GO: Timm's Generic Optimizer Gadgets

<img width=400 align=right src="../img/gogo.jpg">


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

The usual suspects:
<a href="go.py#L42-L53"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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

<a href="go.py#L62-L71"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  13:   class Log:
  14:     def __init__(i):
  15:       i.lo, i.hi = None, None
  16:     def norm(i,x):
  17:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  18:     def __iadd__(i,x):
  19:       if   i.lo == None : i.lo = i.hi = x # auto-initialize
  20:       elif x > i.hi     : i.hi = x
  21:       else x < i.lo     : i.lo = x
  22:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="go.py#L80-L82"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  23:   def Candidate(decs=[],objs=[]):
  24:     return o(dec=dec,objs=objs,
  25:              aggregate=None)
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="go.py#L88-L98"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  26:   def Schaffer():
  27:     def f1(can):
  28:       x = can.decs[0]
  29:       return x**2
  30:     def f2(can):
  31:       x = can.decs[0]
  32:       return (x-2)**2
  33:     return Candidate(
  34:             decs = [Want("x",   lo = -4, hi = 4)],
  35:             objs = [Less("f1",  maker=f1),
  36:                     Less("f12", maker=f2)])
```

### Filling in the Candidates

+ Replace some template candidate with one `what` for each location. Useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

<a href="go.py#L108-L122"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  37:   def none(): return None
  38:   def log():  return Log()
  39:   
  40:   def fill(x, what=none):
  41:     if isinstance(x,list):
  42:       return fillList(x,what)
  43:     elif isinstance(x,o):
  44:       return o( fillDictionary(o.__dict__, what) )
  45:     else:
  46:       return slot()
  47:   
  48:   def fillList(lst,what):
  49:     return [ what() for _ in lst]
  50:   def fillDictionary(d,what):
  51:     return { k:fill(v,what) for k,v in d.items() }
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


<a href="go.py#L146-L161"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  52:   class Want(object):
  53:     def __init__(i, txt, init=None,
  54:                     lo=-10**32, hi=10**32,
  55:                     maker=None):
  56:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
  57:       i.maker = maker or i.guess
  58:     def __repr__(i):
  59:       return 'o'+str(i.__dict__)
  60:       def guess(i):
  61:       return i.lo + r()*(i.hi - i.lo)
  62:     def restrain(i,x):
  63:       return max(i.lo, min(i.hi, x))
  64:     def wrap(i,x):
  65:       return i.lo + (x - i.lo) % (i.hi - i.lo)
  66:     def ok(i,x):
  67:       return i.lo <= x <= i.hi
```

### Want Objectives?

Subclasses of `Want` store information about objectives 
including:

+ How to compute the distance `fromHell`.
+ When does one objective have a `better` value than another;


Here are out `better` predicates:

<a href="go.py#L176-L177"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  68:   def lt(i,j): return i < j
  69:   def gt(i,j): return i > j
```

And these control our objectives as follows:

<a href="go.py#L183-L196"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  70:   class Obj(Want):
  71:     def fromHelll(i,x,log):
  72:       hell = 1 if i.better == lt else 0
  73:       return (hell - log.norm(x)) ** 2
  74:     
  75:   class Less(Obj):
  76:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  77:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  78:       i.better = lt
  79:       
  80:   class More(Obj):
  81:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  82:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  83:       i.better = gt
```

## Wants: places to store lots of `Want`s

<a href="go.py#L202-L256"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  84:   class Wants:
  85:     def __init__(i, wants,also = None):
  86:       i.wants  = wants
  87:       i.log    = fill(i.wants, log)
  88:       i.also   = also
  89:       
  90:     def decs(i):
  91:       can = i.blank()
  92:       can.decs = [want.maker() for want in i.wants.decs]
  93:       return can
  94:     
  95:     def seen(i,whats,loggers):
  96:       for what in whats:
  97:         for logs in loggers:
  98:           for got,log in zip(can[what],logs[what]):
  99:             log += got
 100:             
 101:     def evaluate(i,c):
 102:       can.aggregate = None:
 103:       can.objs = [want.maker(can) for want in i.wants.objs]
 104:       return can
 105:     
 106:     def aggregate(i,can):
 107:       if can.aggregate == None:
 108:         agg = n = 0
 109:         for obj,want,log in zip(c.objs,i.wants.objs.i.log.objs):
 110:           n   += 1
 111:           agg += want.fromHell(obj,log)
 112:         can.aggregate = agg ** 0.5 / n ** 0.5
 113:       return can.aggregate
 114:     
 115:     def blank(i):
 116:       return fill(i.wants, none)
 117:     
 118:     def mutate(i,can,p):
 119:       can1= i.blank()
 120:       for n,(dec,want) in enumerate(zip(can.decs,i.want.decs)):
 121:         can1[n] = want.maker() if p > r() else dec
 122:       return can1
 123:     
 124:     def baseline(i,n=100):
 125:       for _ in xrange(n):
 126:         can = i.evaluate( i.decs() )
 127:         i.log.aggregate  += i.aggregate(can)
 128:         i.also.aggregate += i.aggregate(can)
 129:         i.seen(can, ["decs","objs"],
 130:                     [i.log,i.also])
 131:         
 132:   
 133:   
 134:   def sa(m,
 135:          p=0.3, cooling=1,kmax=1000,e[silon=10.1,era=100,lives=5): # e.g. sa(Schafer())
 136:          k, life, e = 1,lives,1e32):
 137:   
 138:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

