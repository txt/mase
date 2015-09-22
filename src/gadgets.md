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

<a href="gadgets.py#L112-L152"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
  22:     def nudge(i,f=1):
  23:       return (i.hi - i.lo)*f
  24:   
  25:   @setting
  26:   def SOMES(): return o(
  27:       size=256
  28:       )
  29:   
  30:   class Some:
  31:     def __init__(i, max=None): 
  32:       i.n, i.any = 0,[]
  33:       i.max = max or the.SOMES.size
  34:     def __iadd__(i,x):
  35:       i.n += 1
  36:       now = len(i.any)
  37:       if now < i.max:    
  38:         i.any += [x]
  39:       elif r() <= now/i.n:
  40:         i.any[ int(r() * now) ]= x 
  41:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L161-L180"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  42:   def Candidate(decs=[],objs=[]):
  43:     return o(decs=decs,objs=objs,
  44:              aggregate=None)
  45:   
  46:   def canCopy(can,
  47:                     what = lambda : None):
  48:     copy= Candidate()
  49:     copy.decs = [what() for _ in can.decs]
  50:     copy.objs = [what() for _ in can.objs]
  51:     copy.aggregate = what()
  52:     return copy
  53:   
  54:   def parts(can1=None,can2=None):
  55:     "convince iterator. used later"
  56:     if can1 and can2:
  57:       for one,two in zip(can1.decs, can2.decs):
  58:         yield one,two
  59:       for one,two in zip(can1.objs, can2.objs):
  60:         yield one,two
  61:       yield can1.aggregate, can2.aggregate
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="gadgets.py#L186-L237"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  62:   def Schaffer():
  63:     def f1(can):
  64:       x = can.decs[0]
  65:       return x**2
  66:     def f2(can):
  67:       x = can.decs[0]
  68:       return (x-2)**2
  69:     return Candidate(
  70:             decs = [Want("x",   lo = -10**5, hi = 10**5)],
  71:             objs = [Less("f1",  maker=f1),
  72:                     Less("f2", maker=f2)])
  73:   
  74:   def Fonseca(n=3):
  75:     def f1(can):
  76:       z = sum((x - 1/sqrt(n))**2 for x in can.decs)
  77:       return 1 - ee**(-1*z)
  78:     def f2(can):
  79:       z = sum((x + 1/sqrt(n))**2 for x in can.decs)
  80:       return 1 - ee**(-1*z)
  81:     def dec(x):
  82:       return Want(x, lo=-4, hi=4)
  83:     return Candidate(
  84:             decs = [dec(x) for x in range(n)],
  85:             objs = [Less("f1",  maker=f1),
  86:                     Less("f2",  maker=f2)])
  87:   
  88:   def Kursawe(a=1,b=1):
  89:     def f1(can):
  90:       def xy(x,y):
  91:         return -10*ee**(-0.2*sqrt(x*x + y*y))
  92:       a,b,c = can.decs
  93:       return xy(a,b) + xy(b,c)
  94:     def f2(can):
  95:       return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  96:     def dec(x):
  97:       return  Want(x, lo=-5, hi=5)           
  98:     return Candidate(
  99:              decs = [dec(x) for x in range(3)],
 100:              objs = [Less("f1",  maker=f1),
 101:                      Less("f2",  maker=f2)])
 102:   
 103:   def ZDT1(n=30):
 104:     def f1(can): return can.decs[0]
 105:     def f2(can):
 106:       g = 1 + 9*sum(x for x in can.decs[1:] )/(n-1)
 107:       return g*abs(1 - sqrt(can.decs[0]*g))
 108:     def dec(x):
 109:       return Want(x,lo=0,hi=1)
 110:     return Candidate(
 111:       decs=[dec(x) for x in range(n)],
 112:       objs=[Less("f1",maker=f1),
 113:             Less("f2",maker=f2)])
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

<a href="gadgets.py#L261-L284"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 114:   def lt(i,j): return i < j
 115:   def gt(i,j): return i > j
 116:   
 117:   class Want(object):
 118:     def __init__(i, txt, init=None,
 119:                     lo=-10**32, hi=10**32,
 120:                     better=lt,
 121:                     maker=None):
 122:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 123:       i.maker = maker or i.guess
 124:       i.better= better
 125:     def __repr__(i):
 126:       return 'o'+str(i.__dict__)
 127:     def guess(i):
 128:       return i.lo + r()*(i.hi - i.lo)
 129:     def restrain(i,x):
 130:       return max(i.lo, min(i.hi, x))
 131:     def wrap(i,x):
 132:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 133:     def ok(i,x):
 134:       return i.lo <= x <= i.hi
 135:     def fromHell(i,x,log):
 136:       hell = 1 if i.better == lt else 0
 137:       return (hell - log.norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L291-L294"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 138:   Less=Want
 139:   
 140:   def More(txt,*lst,**d):
 141:     return Want(txt,*lst,better=gt,**d)
```

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

<a href="gadgets.py#L321-L470"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 142:   @setting
 143:   def GADGETS(): return  o(
 144:       baseline=100,
 145:       mutate = 0.3,
 146:       epsilon=0.01,
 147:       era=50,
 148:       lives=5,
 149:       verbose=True,
 150:       nudge=1
 151:   )
 152:   
 153:   class Gadgets:
 154:     def __init__(i,
 155:                  abouts):
 156:       i.abouts = abouts
 157:       
 158:     def blank(i):
 159:       "return a new candidate, filled with None"
 160:       return canCopy(i.abouts, lambda: None)
 161:     def logs(i,also=None):
 162:       "Return a new log, also linked to another log"
 163:       new = canCopy(i.abouts, lambda: Log())
 164:       for new1,also1 in parts(new,also):
 165:           new1.also = also1
 166:       return new
 167:     def decs(i):
 168:       "return a new candidate, with guesses for decisions"
 169:       can = i.blank()
 170:       can.decs = [about.maker() for about in i.abouts.decs]
 171:       return can
 172:     
 173:     def eval(i,can):
 174:       "expire the old aggregate. make the objective scores."
 175:       can.aggregate = None
 176:       can.objs = [about.maker(can) for about in i.abouts.objs]
 177:       return can
 178:   
 179:     def aggregate(i,can,logs):
 180:       "Return the aggregate. Side-effect: store it in the can"
 181:       if can.aggregate == None:
 182:          agg = n = 0
 183:          for obj,about,log in zip(can.objs,
 184:                                   i.abouts.objs,
 185:                                   logs.objs):
 186:            n   += 1
 187:            if not log.empty():
 188:              agg += about.fromHell(obj,log)
 189:          can.aggregate = agg ** 0.5 / n ** 0.5
 190:       return can.aggregate
 191:          
 192:     def mutate(i,can,logs,p=None,f=None):
 193:       "Return a new can with p% mutated"
 194:       if p is None: p = the.GADGETS.mutate
 195:       if f is None: f = the.GADGETS.nudge
 196:       can1= i.blank()
 197:       for n,(dec,about,log) in enumerate(zip(can.decs,
 198:                                              i.abouts.decs,
 199:                                              logs.decs)):
 200:         val   = can.decs[n]
 201:         if p > r():
 202:         #  above = log.hi - val
 203:          # below = log.lo - val
 204:          # if above < below:
 205:          #   lo,hi = log.hi - above*2,log.hi
 206:          # else:
 207:          #   lo,hi = log.lo, log.lo + below*2
 208:          # val = about.wrap(lo + r()*(hi - lo))
 209:           
 210:           nudge = log.nudge(the.GADGETS.nudge)*r()
 211:           val  = about.wrap(val + nudge)
 212:         can1.decs[n] = val
 213:       return can1
 214:     
 215:     def baseline(i,logs,n=None):
 216:       "Log the results of generating, say, 100 random instances."
 217:       frontier = []
 218:       for j in xrange(n or the.GADGETS.baseline):
 219:         can = i.eval( i.decs() )
 220:         i.aggregate(can,logs)
 221:         [log + x for log,x in parts(logs,can)]
 222:         frontier += [can]
 223:       return frontier
 224:     def energy(i,can,logs):
 225:       "Returns an energy value to be minimized"
 226:       i.eval(can)
 227:       e = abs(1 - i.aggregate(can,logs))
 228:       if e < 0: e= 0
 229:       if e > 1: e= 1
 230:       return e
 231:     def better1(i,now,last):
 232:       better=worse=0
 233:       for now1,last1,about in zip(now.objs,
 234:                                   last.objs,
 235:                                   i.abouts.objs):
 236:         nowMed = median(now1.some())
 237:         lastMed= median(last1.some())
 238:         if about.better(nowMed, lastMed):
 239:           better += 1
 240:         elif nowMed != lastMed:
 241:           worse += 1
 242:       return better > 0 and worse < 1
 243:     def fyi(i,x)   : the.GADGETS.verbose and say(x)
 244:     def shout(i,x) : i.fyi("\033[7m"+str(x)+"\033[m")
 245:     def bye(i,info,first,now) : i.fyi(info); return first,now
 246:   
 247:   @setting
 248:   def SA(): return o(
 249:       p=0.25,
 250:       cooling=1,
 251:       kmax=1000)
 252:     
 253:   class sa(Gadgets):
 254:     def run(i):
 255:       def p(old,new,t): return ee**((old - new)/t)
 256:       def goodbye(x)  : return i.bye(x,first,now)
 257:       k,eb,life, = 0,1,the.GADGETS.lives
 258:       also = i.logs()
 259:       first = now  = i.logs(also)
 260:       i.baseline(now, the.GADGETS.era)
 261:       last, now = now, i.logs(also)
 262:       s    = i.decs()
 263:       e    = i.energy(s,now)
 264:       i.fyi("%4s [%2s] %3s "% (k,life,"     "))
 265:       while True:
 266:         info="."
 267:         k += 1
 268:         t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 269:         sn = i.mutate(s, also, the.GADGETS.mutate)
 270:         en = i.energy(sn,also)
 271:         [log + x for log,x in parts(now,sn)]
 272:         if en < eb:
 273:           sb,eb = sn,en
 274:           i.shout("!")
 275:         if en < e:
 276:           s,e = sn,en
 277:           info = "+"
 278:         elif p(e,en,t) < r():
 279:            s,e = sn, en
 280:            info="?"
 281:         if k % the.GADGETS.era: 
 282:           i.fyi(info)
 283:         else:
 284:           life = life - 1
 285:           if i.better1(now, last)     : life = the.GADGETS.lives 
 286:           if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 287:           if life < 1                 : return goodbye("L")
 288:           if k > the.SA.kmax          : return goodbye("K")
 289:           i.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 290:           last, now  = now, i.logs(also) 
 291:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

