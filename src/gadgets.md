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

<a href="gadgets.py#L112-L157"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Log:
   2:     def __init__(i,init=[],also=None):
   3:       i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
   4:       map(i.__add__,init)
   5:     def adds(i,lst):
   6:       map(i.__add__,lst)
   7:     def __add__(i,x):
   8:       i.n += 1
   9:       if   i.empty() : i.lo = i.hi = x # auto-initialize
  10:       elif x > i.hi     : i.hi = x
  11:       elif x < i.lo     : i.lo = x
  12:       if i.also:
  13:         i.also + x
  14:       i._some += x
  15:       return x
  16:     def some(i):
  17:       return i._some.any
  18:     def tiles(i,tiles=None,ordered=False,n=3):
  19:       return r3(ntiles(i.some(),tiles,ordered),n)
  20:     def empty(i):
  21:       return i.lo == None
  22:     def norm(i,x):
  23:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
  24:     def stats(i,tiles=[0.25,0.5,0.75]):
  25:       return ntiles(sorted(i._some.any),
  26:              ordered=False, 
  27:              tiles=tiles)
  28:       
  29:   
  30:   @setting
  31:   def SOMES(): return o(
  32:       size=256
  33:       )
  34:   
  35:   class Some:
  36:     def __init__(i, max=None): 
  37:       i.n, i.any = 0,[]
  38:       i.max = max or the.SOMES.size
  39:     def __iadd__(i,x):
  40:       i.n += 1
  41:       now = len(i.any)
  42:       if now < i.max:    
  43:         i.any += [x]
  44:       elif r() <= now/i.n:
  45:         i.any[ int(r() * now) ]= x 
  46:       return i
```

## Candidates

`Candidate`s have objectives, decisions and maybe some aggregate value. Note that since
they are just containers, we define `Candidate` using the `o` container class.

<a href="gadgets.py#L166-L193"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  47:   class Candidate(object):
  48:     def __init__(i,decs=[],objs=[]):
  49:       i.decs,i.objs=decs,objs
  50:       i.aggregate=None
  51:       i.abouts = i.about()
  52:     def __getitem__(i,key):
  53:       return i.__dict__[key]
  54:     def ok(i,can): return True
  55:     def about(i): True
  56:     def __repr__(i):
  57:       return printer(i,decs=i.decs,
  58:                      objs=i.objs,
  59:                      aggregated=i.aggregate)
  60:     def clone(i,what = lambda _: None):
  61:       j      = object.__new__(i.__class__)
  62:       j.decs = [what(x) for x in i.decs]
  63:       j.objs = [what(x) for x in i.objs]
  64:       j.aggregate = what(i.aggregate)
  65:       j.abouts = i.abouts
  66:       return j
  67:     def alongWith(i,j=None):
  68:       "convenient iterator."
  69:       if j:
  70:         for one,two in zip(i.decs, j.decs):
  71:           yield one,two
  72:         for one,two in zip(i.objs, j.objs):
  73:           yield one,two
  74:         yield i.aggregate, j.aggregate
```

Example model (note the use of the `want`, `less` and `more` classes... defined below).

<a href="gadgets.py#L199-L277"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  75:   class Schaffer(Candidate):
  76:     def about(i):
  77:       def f1(can):
  78:         x = can.decs[0]
  79:         return x**2
  80:       def f2(can):
  81:         x = can.decs[0]
  82:         return (x-2)**2
  83:       i.decs = [An("x",   lo = -10**5, hi = 10**5)]
  84:       i.objs = [Less("f1",  maker=f1),
  85:                 Less("f2", maker=f2)]
  86:     
  87:   class Fonseca(Candidate):
  88:     n=3
  89:     def about(i):
  90:       def f1(can):
  91:         z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
  92:         return 1 - ee**(-1*z)
  93:       def f2(can):
  94:         z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
  95:         return 1 - ee**(-1*z)
  96:       def dec(x):
  97:         return An(x, lo=-4, hi=4)
  98:       i.decs = [dec(x) for x in range(Fonseca.n)]
  99:       i.objs = [Less("f1",  maker=f1),
 100:                 Less("f2",  maker=f2)]
 101:   
 102:   class Kursawe(Candidate):
 103:     def about(i,a=1,b=1):
 104:       def f1(can):
 105:         def xy(x,y):
 106:           return -10*ee**(-0.2*sqrt(x*x + y*y))
 107:         a,b,c = can.decs
 108:         return xy(a,b) + xy(b,c)
 109:       def f2(can):
 110:         return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
 111:       def dec(x):
 112:         return  An(x, lo=-5, hi=5)           
 113:       i.decs = [dec(x) for x in range(3)]
 114:       i.objs = [Less("f1",  maker=f1),
 115:                 Less("f2",  maker=f2)]
 116:   
 117:   class ZDT1(Candidate):
 118:     n=30
 119:     def about(i):
 120:       def f1(can):
 121:         return can.decs[0]
 122:       def f2(can):
 123:         g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
 124:         return g*abs(1 - sqrt(can.decs[0]*g))
 125:       def dec(x):
 126:         return An(x,lo=0,hi=1)
 127:       i.decs = [dec(x) for x in range(ZDT1.n)]
 128:       i.objs = [Less("f1",maker=f1),
 129:                 Less("f2",maker=f2)]
 130:   
 131:   class Viennet4(Candidate):
 132:     def ok(i,can):
 133:        one,two = can.decs
 134:        g1 = -1*two - 4*one + 4
 135:        g2 = one + 1            
 136:        g3 = two - one + 2
 137:        return g1 >= 0 and g2 >= 0 and g3 >= 0
 138:     def about(i):
 139:       def f1(can):
 140:         one,two = can.decs
 141:         return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
 142:       def f2(can):
 143:         one,two = can.decs
 144:         return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
 145:       def f3(can):
 146:         one,two= can.decs
 147:         return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
 148:       def dec(x):
 149:         return An(x,lo= -4,hi= 4)
 150:       i.decs = [dec(x) for x in range(2)]
 151:       i.objs = [Less("f1",maker=f1),
 152:                 Less("f2",maker=f2),
 153:                 Less("f3",maker=f3)]
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

<a href="gadgets.py#L301-L327"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 154:   def lt(i,j): return i < j
 155:   def gt(i,j): return i > j
 156:   
 157:   class About(object):
 158:     def __init__(i, txt, init=None,
 159:                     lo=-10**32, hi=10**32,
 160:                     better=lt,
 161:                     maker=None):
 162:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 163:       i.maker = maker or i.guess
 164:       i.better= better
 165:     def __repr__(i):
 166:       return 'o'+str(i.__dict__)
 167:     def guess(i):
 168:       return i.lo + r()*(i.hi - i.lo)
 169:     def restrain(i,x):
 170:       return max(i.lo, min(i.hi, x))
 171:     def wrap(i,x):
 172:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 173:     def norm(i,x):
 174:       return (x - i.lo) / (i.hi - i.lo + 10**-32)
 175:     def ok(i,x):
 176:       return i.lo <= x <= i.hi
 177:     def fromHell(i,x,log,min=None,max=None):
 178:       norm = i.norm if log.lo == None else log.norm
 179:       hell = 1 if i.better == lt else 0
 180:       return (hell - norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L334-L337"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 181:   A = An = Less = About
 182:   
 183:   def More(txt,*lst,**d):
 184:     return About(txt,*lst,better=gt,**d)
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

<a href="gadgets.py#L364-L598"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 185:   @setting
 186:   def GADGETS(): return  o(
 187:       baseline=50,
 188:       era=50,
 189:       mutate = 0.3,
 190:       epsilon=0.01,
 191:       lives=5,
 192:       verbose=True,
 193:       nudge=1,
 194:       patience=64
 195:   )
 196:   
 197:   class Gadgets:
 198:     """Gadgets is a "facade"; i.e. a simplified 
 199:     interface to a body of code."""
 200:     def __init__(i,model):
 201:       i.model  = model
 202:       
 203:     def blank(i):
 204:       "return a new candidate, filled with None"
 205:       return i.model.clone(lambda _: None)
 206:     def logs(i,also=None):
 207:       "Return a new log, also linked to another log"
 208:       new = i.model.clone(lambda _ : Log())
 209:       for new1,also1 in new.alongWith(also):
 210:           new1.also = also1
 211:       return new
 212:     def log1(i,can,log):
 213:        [log1 + x for log1,x in log.alongWith(can)]
 214:     def logNews(i,log, news):
 215:       for can in news:
 216:         for x,log1 in zip(can.decs,log.decs):
 217:           log1 + x
 218:         for x,log1 in zip(can.objs,log.objs):
 219:           log1 + x
 220:         log.aggregate + i.aggregate(can,log)
 221:       return news
 222:         
 223:     def aFewBlanks(i):
 224:       patience = the.GADGETS.patience
 225:       while True:
 226:         yield i.blank()
 227:         patience -= 1
 228:         assert patience > 0, "constraints too hard to satisfy"
 229:   
 230:     def decs(i):
 231:       "return a new candidate, with guesses for decisions"
 232:       for can in i.aFewBlanks():
 233:         can.decs = [dec.maker() for dec in i.model.decs]
 234:         if i.model.ok(can):
 235:           return can
 236:     
 237:     def eval(i,can):
 238:       "expire the old aggregate. make the objective scores."
 239:       can.aggregate = None
 240:       can.objs = [obj.maker(can) for obj in i.model.objs]
 241:       return can
 242:   
 243:     def aggregate(i,can,logs):
 244:       "Return the aggregate. Side-effect: store it in the can"
 245:       if can.aggregate == None:
 246:          agg = n = 0
 247:          for obj,about,log in zip(can.objs,
 248:                                   i.model.objs,
 249:                                   logs.objs):
 250:            n   += 1
 251:            agg += about.fromHell(obj,log)
 252:          can.aggregate = agg ** 0.5 / n ** 0.5
 253:       return can.aggregate
 254:          
 255:     def mutate(i,can,logs,p):
 256:       "Return a new can with p% mutated"
 257:       for sn in i.aFewBlanks():
 258:         for n,(dec,about,log) in enumerate(zip(can.decs,
 259:                                              i.model.decs,
 260:                                              logs.decs)):
 261:           val = can.decs[n]
 262:           if p > r():
 263:             some = (log.hi - log.lo)*0.5
 264:             val  = val - some + 2*some*r()
 265:             val  = about.wrap(val)
 266:           sn.decs[n] = val
 267:         if i.model.ok(sn):
 268:           return sn
 269:         
 270:     def xPlusFyz(i,threeMore,cr,f):
 271:       "Crossovers some decisions, by a factor of 'f'"
 272:       def smear((x1, y1, z1, about)):
 273:         x1 = x1 if cr <= r() else x1 + f*(y1-z1)
 274:         return about.wrap(x1)
 275:       for sn in i.aFewBlanks():
 276:         x,y,z   = threeMore()
 277:         sn.decs = [smear(these)
 278:                    for these in zip(x.decs,
 279:                                     y.decs,
 280:                                     z.decs,
 281:                                     i.model.decs)]
 282:         if i.model.ok(sn):
 283:           return sn
 284:       
 285:     def news(i,n=None):
 286:       "Generating, say, 100 random instances."
 287:       return [i.eval( i.decs())
 288:               for _ in xrange(n or the.GADGETS.baseline)]
 289:   
 290:     def energy(i,can,logs):
 291:       "Returns an energy value to be minimized"
 292:       i.eval(can)
 293:       e = abs(1 - i.aggregate(can,logs))
 294:       if e < 0: e= 0
 295:       if e > 1: e= 1
 296:       return e
 297:     def better1(i,now,last):
 298:       better=worse=0
 299:       for now1,last1,about in zip(now.objs,
 300:                                   last.objs,
 301:                                   i.model.objs):
 302:         nowMed = median(now1.some())
 303:         lastMed= median(last1.some())
 304:         if about.better(nowMed, lastMed):
 305:           better += 1
 306:         elif nowMed != lastMed:
 307:           worse += 1
 308:       return better > 0 and worse < 1
 309:     def fyi(i,x)   : the.GADGETS.verbose and say(x)
 310:     def shout(i,x) : i.fyi("__" + x)
 311:     def bye(i,info,first,now) : i.fyi(info); return first,now
 312:   
 313:       
 314:   @setting
 315:   def SA(): return o(
 316:       p=0.25,
 317:       cooling=1,
 318:       kmax=1000)
 319:     
 320:   def sa(m,baseline=None,also2=None):
 321:     def goodbye(x)  : return g.bye(x,first,now)
 322:     g = Gadgets(m)
 323:     def p(old,new,t): return ee**((old - new)/t)
 324:     k,eb,life = 0,1,the.GADGETS.lives
 325:     #===== setting up logs
 326:     also     = g.logs(also2) # also = log of all eras
 327:     first    = now  = g.logs(also)
 328:     g.logNews(first,baseline or g.news())
 329:     last, now  = now, g.logs(also)
 330:     #===== ok to go
 331:     s = g.decs()
 332:     e = g.energy(s,now)
 333:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 334:     while True:
 335:       info="."
 336:       k += 1
 337:       t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 338:       sn = g.mutate(s, also,the.SA.p)
 339:       en = g.energy(sn,also)
 340:       g.log1(sn,now)
 341:       if en < eb:
 342:         sb,eb = sn,en
 343:         g.shout("!")
 344:       if en < e:
 345:         s,e = sn,en
 346:         info = "+"
 347:       elif p(e,en,t) < r():
 348:         s,e = sn, en
 349:         info="?"
 350:       if k % the.GADGETS.era: 
 351:         g.fyi(info)
 352:       else:
 353:         life = life - 1
 354:         if g.better1(now, last)     : life = the.GADGETS.lives 
 355:         if life < 1                 : return goodbye("L")
 356:         if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 357:         if k > the.SA.kmax          : return goodbye("K")
 358:         g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 359:         last, now  = now, g.logs(also) 
 360:   
 361:   
 362:   @setting
 363:   def DE(): return o(
 364:       cr = 0.4,
 365:       f  = 0.5,
 366:       npExpand = 10,
 367:       kmax=1000)
 368:     
 369:   def de(m,baseline=None,also2=None):
 370:     def goodbye(x)  : return g.bye(x,first,now)
 371:     g  = Gadgets(m)
 372:     np = len(g.model.decs) * the.DE.npExpand
 373:     k,eb,life = 0,1,the.GADGETS.lives
 374:     #===== setting up logs
 375:     also     = g.logs(also2) # also = log of all eras
 376:     first    = now  = g.logs(also)
 377:     frontier = g.logNews(first,baseline or g.news(np))
 378:     last, now  = now, g.logs(also)
 379:     #===== ok to go
 380:     sn = en = None
 381:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 382:     while True:
 383:       for n,parent in enumerate(frontier):
 384:         info="."
 385:         k += 1
 386:         e  = g.aggregate(parent, also)
 387:         sn = g.xPlusFyz(lambda: another3(frontier,parent),
 388:                         the.DE.cr,
 389:                         the.DE.f)
 390:         en = g.energy(sn,also)
 391:         g.log1(sn,now)
 392:         if en < eb:
 393:           sb,eb = sn,en
 394:           g.shout("!")
 395:         if en < e:
 396:           frontier[n] = sn # goodbye parent
 397:           info = "+"
 398:         g.fyi(info)
 399:       life = life - 1
 400:       if g.better1(now, last)     : life = the.GADGETS.lives 
 401:       if life < 1                 : return goodbye("L")
 402:       if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 403:       if k > the.DE.kmax          : return goodbye("K")
 404:       g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 405:       last, now  = now, g.logs(also) 
 406:   
 407:   def another3(lst, avoid=None):
 408:     def another1():
 409:       x = avoid
 410:       while id(x) in seen: 
 411:         x = lst[  int(random.uniform(0,len(lst))) ]
 412:       seen.append( id(x) )
 413:       return x
 414:     # -----------------------
 415:     assert len(lst) > 4
 416:     avoid = avoid or lst[0]
 417:     seen  = [ id(avoid) ]
 418:     return another1(), another1(), another1()
 419:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

