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

<a href="gadgets.py#L112-L150"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Log:
   2:     def __init__(i,init=[],also=None):
   3:       i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
   4:       map(i.__add__,init)
   5:     def __add__(i,x):
   6:       i.n += 1
   7:       if   i.empty() : i.lo = i.hi = x # auto-initialize
   8:       elif x > i.hi     : i.hi = x
   9:       elif x < i.lo     : i.lo = x
  10:       if i.also:
  11:         i.also + x
  12:       i._some += x
  13:       return x
  14:     def some(i):
  15:       return i._some.any
  16:     def tiles(i,tiles=None,ordered=False,n=3):
  17:       return r3(ntiles(i.some(),tiles,ordered),n)
  18:     def empty(i):
  19:       return i.lo == None
  20:     def norm(i,x):
  21:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  22:   
  23:   @setting
  24:   def SOMES(): return o(
  25:       size=256
  26:       )
  27:   
  28:   class Some:
  29:     def __init__(i, max=None): 
  30:       i.n, i.any = 0,[]
  31:       i.max = max or the.SOMES.size
  32:     def __iadd__(i,x):
  33:       i.n += 1
  34:       now = len(i.any)
  35:       if now < i.max:    
  36:         i.any += [x]
  37:       elif r() <= now/i.n:
  38:         i.any[ int(r() * now) ]= x 
  39:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L159-L178"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  40:   def Candidate(decs=[],objs=[]):
  41:     return o(decs=decs,objs=objs,
  42:              aggregate=None)
  43:   
  44:   def canCopy(can,
  45:                     what = lambda : None):
  46:     copy= Candidate()
  47:     copy.decs = [what() for _ in can.decs]
  48:     copy.objs = [what() for _ in can.objs]
  49:     copy.aggregate = what()
  50:     return copy
  51:   
  52:   def parts(can1=None,can2=None):
  53:     "convince iterator. used later"
  54:     if can1 and can2:
  55:       for one,two in zip(can1.decs, can2.decs):
  56:         yield one,two
  57:       for one,two in zip(can1.objs, can2.objs):
  58:         yield one,two
  59:       yield can1.aggregate, can2.aggregate
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).
s
<a href="gadgets.py#L184-L224"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  60:   def Schaffer():
  61:     def f1(can):
  62:       x = can.decs[0]
  63:       return x**2
  64:     def f2(can):
  65:       x = can.decs[0]
  66:       return (x-2)**2
  67:     return Candidate(
  68:             decs = [Want("x",   lo = -10**5, hi = 10**5)],
  69:             objs = [Less("f1",  maker=f1),
  70:                     Less("f2", maker=f2)])
  71:   
  72:   def Fonseca(n=3):
  73:     def f1(can):
  74:       z = sum((x - 1/sqrt(n))**2 for x in can.decs)
  75:       return 1 - ee**(-1*z)
  76:     def f2(can):
  77:       z = sum((x + 1/sqrt(n))**2 for x in can.decs)
  78:       return 1 - ee**(-1*z)
  79:     def dec(x):
  80:       return Want(x, lo=-4, hi=4)
  81:     return Candidate(
  82:             decs = [dec(x) for x in range(n)],
  83:             objs = [Less("f1",  maker=f1),
  84:                     Less("f2",  maker=f2)])
  85:   
  86:   def Kursawe(a=1,b=1):
  87:     def f1(can):
  88:       def xy(x,y):
  89:         return -10*ee**(-0.2*sqrt(x*x + y*y))
  90:       a,b,c = can.decs
  91:       return xy(a,b) + xy(b,c)
  92:     def f2(can):
  93:       return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  94:     def dec(x):
  95:       return  Want(x, lo=-5, hi=5)           
  96:     return Candidate(
  97:              decs = [dec(x) for x in range(3)],
  98:              objs = [Less("f1",  maker=f1),
  99:                      Less("f2",  maker=f2)])
 100:   
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

<a href="gadgets.py#L248-L271"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 101:   def lt(i,j): return i < j
 102:   def gt(i,j): return i > j
 103:   
 104:   class Want(object):
 105:     def __init__(i, txt, init=None,
 106:                     lo=-10**32, hi=10**32,
 107:                     better=lt,
 108:                     maker=None):
 109:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 110:       i.maker = maker or i.guess
 111:       i.better= better
 112:     def __repr__(i):
 113:       return 'o'+str(i.__dict__)
 114:     def guess(i):
 115:       return i.lo + r()*(i.hi - i.lo)
 116:     def restrain(i,x):
 117:       return max(i.lo, min(i.hi, x))
 118:     def wrap(i,x):
 119:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 120:     def ok(i,x):
 121:       return i.lo <= x <= i.hi
 122:     def fromHell(i,x,log):
 123:       hell = 1 if i.better == lt else 0
 124:       return (hell - log.norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L278-L281"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 125:   Less=Want
 126:   
 127:   def More(txt,*lst,**d):
 128:     return Want(txt,*lst,better=gt,**d)
```

## `Gadgets`: places to store lots of `Want`s

Note that the following gizmos will get mixed and matched
any number of ways by different optimizers. So when extending the 
following, always write

+ Simple primitives
+ Which can be combined together by other functions.
    + For example, the primitive `decs` method (that generates decisions)
      on `keeps` the decision if called by `keepDecs`.

<a href="gadgets.py#L296-L426"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 129:   @setting
 130:   def GADGETS(): return  o(
 131:       baseline=100,
 132:       mutate = 0.3
 133:   )
 134:   
 135:   class Gadgets:
 136:     def __init__(i,
 137:                  abouts):
 138:       i.abouts = abouts
 139:       
 140:     def blank(i):
 141:       "return a new candidate, filled with None"
 142:       return canCopy(i.abouts, lambda: None)
 143:     def logs(i,also=None):
 144:       "Return a new log, also linked to another log"
 145:       new = canCopy(i.abouts, lambda: Log())
 146:       for new1,also1 in parts(new,also):
 147:           new1.also = also1
 148:       return new
 149:     def decs(i):
 150:       "return a new candidate, with guesses for decisions"
 151:       can = i.blank()
 152:       can.decs = [about.maker() for about in i.abouts.decs]
 153:       return can
 154:     
 155:     def eval(i,can):
 156:       "expire the old aggregate. make the objective scores."
 157:       can.aggregate = None
 158:       can.objs = [about.maker(can) for about in i.abouts.objs]
 159:       return can
 160:   
 161:     def aggregate(i,can,logs):
 162:       "Return the aggregate. Side-effect: store it in the can"
 163:       if can.aggregate == None:
 164:          agg = n = 0
 165:          for obj,about,log in zip(can.objs,
 166:                                   i.abouts.objs,
 167:                                   logs.objs):
 168:            n   += 1
 169:            if not log.empty():
 170:              agg += about.fromHell(obj,log)
 171:          can.aggregate = agg ** 0.5 / n ** 0.5
 172:       return can.aggregate
 173:          
 174:     def mutate(i,can,p=None):
 175:       "Return a new can with p% mutated"
 176:       if p is None: p = the.GADGETS.mutate
 177:       can1= i.blank()
 178:       for n,(dec,about) in enumerate(zip(can.decs,
 179:                                          i.abouts.decs)):
 180:         can1.decs[n] = about.maker() if p > r() else dec
 181:       return can1
 182:     
 183:     def baseline(i,logs,n=None):
 184:       "Log the results of generating, say, 100 random instances."
 185:       frontier = []
 186:       for j in xrange(n or the.GADGETS.baseline):
 187:         can = i.eval( i.decs() )
 188:         i.aggregate(can,logs)
 189:         [log + x for log,x in parts(logs,can)]
 190:         frontier += [can]
 191:       return frontier
 192:     def energy(i,can,logs):
 193:       "Returns an energy value to be minimized"
 194:       i.eval(can)
 195:       return 1 - i.aggregate(can,logs)
 196:     def better1(i,now,last):
 197:       better=worse=0
 198:       for now1,last1,about in zip(now.objs,
 199:                                   last.objs,
 200:                                   i.abouts.objs):
 201:         nowMed = median(now1.some())
 202:         lastMed= median(last1.some())
 203:         if about.better(nowMed, lastMed):
 204:           better += 1
 205:         elif nowMed != lastMed:
 206:           worse += 1
 207:       return better > 0 and worse < 1
 208:   
 209:   @setting
 210:   def SA(): return o(
 211:       p=0.25,
 212:       cooling=1,
 213:       kmax=1000,
 214:       epsilon=0.01,
 215:       era=50,
 216:       lives=5,
 217:       verbose=True)
 218:     
 219:   class sa(Gadgets):
 220:     def fyi(i,x)      : the.SA.verbose and say(x)  
 221:     def bye(i,info,now) : i.fyi(info); return now
 222:     def p(i,old,new,t): return ee**((old - new)/t)
 223:     def run(i):
 224:       k,eb,life, = 0,1,the.SA.lives
 225:       also = i.logs()
 226:       now  = i.logs(also)
 227:       i.baseline(now,the.SA.era)
 228:       last, now = now, i.logs(also)
 229:       s    = i.decs()
 230:       e    = i.energy(s,now)
 231:       i.fyi("%4s [%2s] %3s "% (k,life,"     "))
 232:       while True:
 233:         info="."
 234:         k += 1
 235:         t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 236:         sn = i.mutate(s, the.SA.p)
 237:         en = i.energy(sn,also)
 238:         [log + x for log,x in parts(now,sn)]
 239:         if en < eb:
 240:           sb,eb = sn,en
 241:           i.fyi("\033[7m!\033[m")
 242:         if en < e:
 243:           s,e = sn,en
 244:           info = "+"
 245:         elif i.p(e,en,t) < r():
 246:            s,e = sn, en
 247:            info="?"
 248:         if k % the.SA.era: 
 249:           i.fyi(info)
 250:         else:
 251:           life = life - 1
 252:           if i.better1(now, last): 
 253:             life = the.SA.lives 
 254:           if eb < the.SA.epsilon: return i.bye("E %.5f" %eb,now)
 255:           if life < 1           : return i.bye("L", now)
 256:           if k > the.SA.kmax    : return i.bye("K", now)
 257:           i.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 258:           last, now  = now, i.logs(also) 
 259:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

