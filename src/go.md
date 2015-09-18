[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



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
<a href="go.py#L41-L53"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   import random
   2:   r   = random.random
   3:   isa = isinstance
   4:   _ = None
   5:   
   6:   def seed(x=None):
   7:     random.seed(x or the.run.seed)
   8:   
   9:   class o:
  10:     def __init__(i,**d)    : i.__dict__.update(d)
  11:     def __setitem__(i,k,v) : i.__dict__[k] = v
  12:     def __getitem__(i,k)   : return i.__dict__[k]
  13:     def __repr__(i)        : return 'o'+str(i.__dict__)
```

## Log

This class is the simplest of all.  It just remembers the range of values
seen so far.

<a href="go.py#L62-L71"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  14:   class Log:
  15:     def __init__(i):
  16:       i.lo, i.hi = None, None
  17:     def norm(i,x):
  18:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  19:     def __iadd__(i,x):
  20:       if   i.lo == None : i.lo = i.hi = x # auto-initialize
  21:       elif x > i.hi     : i.hi = x
  22:       else x < i.lo     : i.lo = x
  23:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="go.py#L80-L82"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  24:   def Candidate(decs=[],objs=[]):
  25:     return o(dec=dec,objs=objs,
  26:              aggregate=None)
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="go.py#L88-L98"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  27:   def Schaffer():
  28:     def f1(can):
  29:       x = can.decs[0]
  30:       return x**2
  31:     def f2(can):
  32:       x = can.decs[0]
  33:       return (x-2)**2
  34:     return Candidate(
  35:             decs = [Want("x",   lo = -4, hi = 4)],
  36:             objs = [Less("f1",  maker=f1),
  37:                     Less("f12", maker=f2)])
```

### Filling in the Candidates

+ Replace some template candidate with one `what` for each location. Useful for:
   + Generating logs (replace each slot with one `Log`)
   + Generating a new blank candidate (replace each slot with `None`)

<a href="go.py#L108-L122"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  38:   def none(): return None
  39:   def log():  return Log()
  40:   
  41:   def fill(x, what=none):
  42:     if isinstance(x,list):
  43:       return fillList(x,what)
  44:     elif isinstance(x,o):
  45:       return o( fillDictionary(o.__dict__, what) )
  46:     else:
  47:       return slot()
  48:   
  49:   def fillList(lst,what):
  50:     return [ what() for _ in lst]
  51:   def fillDictionary(d,what):
  52:     return { k:fill(v,what) for k,v in d.items() }
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

  53:   class Want(object):
  54:     def __init__(i, txt, init=None,
  55:                     lo=-10**32, hi=10**32,
  56:                     maker=None):
  57:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
  58:       i.maker = maker or i.guess
  59:     def __repr__(i):
  60:       return 'o'+str(i.__dict__)
  61:       def guess(i):
  62:       return i.lo + r()*(i.hi - i.lo)
  63:     def restrain(i,x):
  64:       return max(i.lo, min(i.hi, x))
  65:     def wrap(i,x):
  66:       return i.lo + (x - i.lo) % (i.hi - i.lo)
  67:     def ok(i,x):
  68:       return i.lo <= x <= i.hi
```

### Want Objectives?

Subclasses of `Want` store information about objectives 
including:

+ How to compute the distance `fromHell`.
+ When does one objective have a `better` value than another;


Here are out `better` predicates:

<a href="go.py#L176-L177"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  69:   def lt(i,j): return i < j
  70:   def gt(i,j): return i > j
```

And these control our objectives as follows:

<a href="go.py#L183-L196"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  71:   class Obj(Want):
  72:     def fromHelll(i,x,log):
  73:       hell = 1 if i.better == lt else 0
  74:       return (hell - log.norm(x)) ** 2
  75:     
  76:   class Less(Obj):
  77:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  78:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  79:       i.better = lt
  80:       
  81:   class More(Obj):
  82:     def __init__(i,txt,init,lo=-10**32,hi=10**32,maker=None):
  83:       super(less, i).__init__(txt,init,lo=lo,hi=hi,maker=maker)
  84:       i.better = gt
```

## Wants: places to store lots of `Want`s

<a href="go.py#L202-L256"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  85:   class Wants:
  86:     def __init__(i, wants,also = None):
  87:       i.wants  = wants
  88:       i.log    = fill(i.wants, log)
  89:       i.also   = also
  90:       
  91:     def decs(i):
  92:       can = i.blank()
  93:       can.decs = [want.maker() for want in i.wants.decs]
  94:       return can
  95:     
  96:     def seen(i,whats,loggers):
  97:       for what in whats:
  98:         for logs in loggers:
  99:           for got,log in zip(can[what],logs[what]):
 100:             log += got
 101:             
 102:     def evaluate(i,c):
 103:       can.aggregate = None:
 104:       can.objs = [want.maker(can) for want in i.wants.objs]
 105:       return can
 106:     
 107:     def aggregate(i,can):
 108:       if can.aggregate == None:
 109:         agg = n = 0
 110:         for obj,want,log in zip(c.objs,i.wants.objs.i.log.objs):
 111:           n   += 1
 112:           agg += want.fromHell(obj,log)
 113:         can.aggregate = agg ** 0.5 / n ** 0.5
 114:       return can.aggregate
 115:     
 116:     def blank(i):
 117:       return fill(i.wants, none)
 118:     
 119:     def mutate(i,can,p):
 120:       can1= i.blank()
 121:       for n,(dec,want) in enumerate(zip(can.decs,i.want.decs)):
 122:         can1[n] = want.maker() if p > r() else dec
 123:       return can1
 124:     
 125:     def baseline(i,n=100):
 126:       for _ in xrange(n):
 127:         can = i.evaluate( i.decs() )
 128:         i.log.aggregate  += i.aggregate(can)
 129:         i.also.aggregate += i.aggregate(can)
 130:         i.seen(can, ["decs","objs"],
 131:                     [i.log,i.also])
 132:         
 133:   
 134:   
 135:   def sa(m,
 136:          p=0.3, cooling=1,kmax=1000,e[silon=10.1,era=100,lives=5): # e.g. sa(Schafer())
 137:          k, life, e = 1,lives,1e32):
 138:   
 139:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

