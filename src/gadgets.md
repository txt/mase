[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 





# GADGETS: Timm's Generic Optimizer Gadgets (and Goodies)

<img width=400 align=right src="../img/gogo.jpg">


`Gadgets` are a library of utilities for working with
optimization models. 

With `Gadgets`, it is possible to encode something
that looks a little like....

```python
for model in [Schaffer,...]:
  for optimizer in [sa,mws...]:
    for _ in xrange(20):
      optimizer(model())
```

Note that:

+ For samples of how to use this code, see [gadgetsok.py](gadgetsok.py).
+ In the following, anything in `this font` is some method or class in the code.

## What are `Gadgets`?

`Gadgets` are a _Factory_ and a _Facade_:

+ In class-based programming, the _factory_ method
  pattern is a _creational pattern_ which uses factory
  methods to deal with the problem of creating
  objects without specifying the exact class of
  object that will be created. This is done by
  creating objects via (e.g.)  calling a factory
  method—- either specified in an interface and
  implemented by child classes.
+ A _facade_ is an object that provides a simplified 
  interface to a larger body of code, such as a class library. A facade can:
   + make a software library easier to use,
     understand and test, since the facade has
     convenient methods for common tasks;
   + make the library more readable, for the same
     reason; 
   + reduce dependencies of outside code on
     the inner workings of a library, since most
     code uses the facade, thus allowing more
     flexibility in developing the system;

`Gadgets` are a _facade_ since, every time I code a new optimizer, its always some mix-and-match of
numerous lower-level facilities. 

+ On Sundays and Wednesdays, I think optimizers should inherit from
`Gadgets`.
+ On every other day, I believe that since not every gadget applies to every optimizer,
its just more flexible and easier to place all those lower-level facilities into a box, and just 
call interface methods to that box.

_Factories_ assemble _parts_. In this code, I know of three kinds of parts:

+ Parts to hold the specific values from one set of
  decisions, objectives and (optionally) some aggregation of the objective
  scores. In the following, these will be called
  + `decs`
  + `objs`
  + `aggregate`
+ Parts for the some _logging code_ that keeps track of the observed `decs` and `objs, aggregate` values.
+ Parts that talk `About` legal values for the `decs` and `objs` and, for `objs` if we want to minimize
  or maximize those scores.

## Parts of the `Gadgets`

### Candidates

`Candidate`s objects have  objectives, decisions and maybe some aggregate value. 
Using a factory method,  we will fill in `Candidate`s with either 

+ The specific values from one set `decs` and `objs, aggregate`;
+ Or, `Log`ging objects that remember what specific values were ever assigned to  `decs` and `objs, aggregate`;
+ Or, `About` objects that defined what are legel values from the specific values  
  (and, for `objs` if we want to minimize
  or maximize those scores)

In the following, I sometimes refer to `Candidate` objects as `can`. For example, the `ok` method
received a `can` and returns true if the current contents of `decs` are valid.

<a href="gadgets.py#L140-L182"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Candidate(object):
   2:     def __init__(i,decs=[],objs=[]):
   3:       i.decs,i.objs=decs,objs
   4:       i.aggregate=None
   5:       i.abouts = i.about()
   6:       
   7:     def __getitem__(i,key):
   8:       "Simple way to access decs or objs or aggregates."
   9:       return i.__dict__[key]
  10:     
  11:     def ok(i,can):
  12:       "Maybe overwritten by subclass."
  13:       return True
  14:     
  15:     def about(i):
  16:       """Factory method for return a Candidate full of 
  17:          About objects."""
  18:       assert False,'implemented by subclass'
  19:       
  20:     def __repr__(i):
  21:       "Present me in a  string"
  22:       return printer(i,decs=i.decs,
  23:                      objs=i.objs,
  24:                      aggregated=i.aggregate)
  25:     
  26:     def clone(i,what = lambda _: None):
  27:       """A genetic factory that makes a new  thing
  28:          like receiver, filled in with 'what' objects."""
  29:       j      = object.__new__(i.__class__)
  30:       j.decs = [what(x) for x in i.decs]
  31:       j.objs = [what(x) for x in i.objs]
  32:       j.aggregate = what(i.aggregate)
  33:       j.abouts = i.abouts
  34:       return j
  35:     
  36:     def alongWith(i,j=None):
  37:       "Convenient iterator."
  38:       if j:
  39:         for one,two in zip(i.decs, j.decs):
  40:           yield one,two
  41:         for one,two in zip(i.objs, j.objs):
  42:           yield one,two
  43:         yield i.aggregate, j.aggregate
```

Using the above, we can build a _factory_ method called `about` that returns what we know `About`
each candidate.

#### Schaffer

<a href="gadgets.py#L191-L201"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  44:   class Schaffer(Candidate):
  45:     def about(i):
  46:       def f1(can):
  47:         x = can.decs[0]
  48:         return x**2
  49:       def f2(can):
  50:         x = can.decs[0]
  51:         return (x-2)**2
  52:       i.decs = [An("x",   lo = -10**5, hi = 10**5)]
  53:       i.objs = [Less("f1",  maker=f1),
  54:                 Less("f2", maker=f2)]
```

In the above, `An` and `Less` are really `About` objects that define legal ranges for values 
 (and, for `objs` if we want to minimize
  or maximize those scores).

Note also that `f1` and `f2` are nested methods that accepted a `Candidate` object (which,
you will recall, I call `can`s).


#### Fonseca

<a href="gadgets.py#L215-L228"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  55:   class Fonseca(Candidate):
  56:     n=3
  57:     def about(i):
  58:       def f1(can):
  59:         z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
  60:         return 1 - ee**(-1*z)
  61:       def f2(can):
  62:         z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
  63:         return 1 - ee**(-1*z)
  64:       def dec(x):
  65:         return An(x, lo=-4, hi=4)
  66:       i.decs = [dec(x) for x in range(Fonseca.n)]
  67:       i.objs = [Less("f1",  maker=f1),
  68:                 Less("f2",  maker=f2)]
```


Note the use of a list comprehension to create

### Kursawe

<a href="gadgets.py#L237-L288"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  69:   class Kursawe(Candidate):
  70:     def about(i,a=1,b=1):
  71:       def f1(can):
  72:         def xy(x,y):
  73:           return -10*ee**(-0.2*sqrt(x*x + y*y))
  74:         a,b,c = can.decs
  75:         return xy(a,b) + xy(b,c)
  76:       def f2(can):
  77:         return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  78:       def dec(x):
  79:         return  An(x, lo=-5, hi=5)           
  80:       i.decs = [dec(x) for x in range(3)]
  81:       i.objs = [Less("f1",  maker=f1),
  82:                 Less("f2",  maker=f2)]
  83:   
  84:   class ZDT1(Candidate):
  85:     n=30
  86:     def about(i):
  87:       def f1(can):
  88:         return can.decs[0]
  89:       def f2(can):
  90:         g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
  91:         return g*abs(1 - sqrt(can.decs[0]*g))
  92:       def dec(x):
  93:         return An(x,lo=0,hi=1)
  94:       i.decs = [dec(x) for x in range(ZDT1.n)]
  95:       i.objs = [Less("f1",maker=f1),
  96:                 Less("f2",maker=f2)]
  97:   
  98:   class Viennet4(Candidate):
  99:     def ok(i,can):
 100:        one,two = can.decs
 101:        g1 = -1*two - 4*one + 4
 102:        g2 = one + 1            
 103:        g3 = two - one + 2
 104:        return g1 >= 0 and g2 >= 0 and g3 >= 0
 105:     def about(i):
 106:       def f1(can):
 107:         one,two = can.decs
 108:         return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
 109:       def f2(can):
 110:         one,two = can.decs
 111:         return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
 112:       def f3(can):
 113:         one,two= can.decs
 114:         return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
 115:       def dec(x):
 116:         return An(x,lo= -4,hi= 4)
 117:       i.decs = [dec(x) for x in range(2)]
 118:       i.objs = [Less("f1",maker=f1),
 119:                 Less("f2",maker=f2),
 120:                 Less("f3",maker=f3)]
```


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

<a href="gadgets.py#L337-L382"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 121:   class Log:
 122:     def __init__(i,init=[],also=None):
 123:       i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
 124:       map(i.__add__,init)
 125:     def adds(i,lst):
 126:       map(i.__add__,lst)
 127:     def __add__(i,x):
 128:       i.n += 1
 129:       if   i.empty() : i.lo = i.hi = x # auto-initialize
 130:       elif x > i.hi     : i.hi = x
 131:       elif x < i.lo     : i.lo = x
 132:       if i.also:
 133:         i.also + x
 134:       i._some += x
 135:       return x
 136:     def some(i):
 137:       return i._some.any
 138:     def tiles(i,tiles=None,ordered=False,n=3):
 139:       return r3(ntiles(i.some(),tiles,ordered),n)
 140:     def empty(i):
 141:       return i.lo == None
 142:     def norm(i,x):
 143:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
 144:     def stats(i,tiles=[0.25,0.5,0.75]):
 145:       return ntiles(sorted(i._some.any),
 146:              ordered=False, 
 147:              tiles=tiles)
 148:       
 149:   
 150:   @setting
 151:   def SOMES(): return o(
 152:       size=256
 153:       )
 154:   
 155:   class Some:
 156:     def __init__(i, max=None): 
 157:       i.n, i.any = 0,[]
 158:       i.max = max or the.SOMES.size
 159:     def __iadd__(i,x):
 160:       i.n += 1
 161:       now = len(i.any)
 162:       if now < i.max:    
 163:         i.any += [x]
 164:       elif r() <= now/i.n:
 165:         i.any[ int(r() * now) ]= x 
 166:       return i
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

<a href="gadgets.py#L407-L433"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 167:   def lt(i,j): return i < j
 168:   def gt(i,j): return i > j
 169:   
 170:   class About(object):
 171:     def __init__(i, txt, init=None,
 172:                     lo=-10**32, hi=10**32,
 173:                     better=lt,
 174:                     maker=None):
 175:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 176:       i.maker = maker or i.guess
 177:       i.better= better
 178:     def __repr__(i):
 179:       return 'o'+str(i.__dict__)
 180:     def guess(i):
 181:       return i.lo + r()*(i.hi - i.lo)
 182:     def restrain(i,x):
 183:       return max(i.lo, min(i.hi, x))
 184:     def wrap(i,x):
 185:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 186:     def norm(i,x):
 187:       return (x - i.lo) / (i.hi - i.lo + 10**-32)
 188:     def ok(i,x):
 189:       return i.lo <= x <= i.hi
 190:     def fromHell(i,x,log,min=None,max=None):
 191:       norm = i.norm if log.lo == None else log.norm
 192:       hell = 1 if i.better == lt else 0
 193:       return (hell - norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L440-L443"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 194:   A = An = Less = About
 195:   
 196:   def More(txt,*lst,**d):
 197:     return About(txt,*lst,better=gt,**d)
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

<a href="gadgets.py#L470-L704"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 198:   @setting
 199:   def GADGETS(): return  o(
 200:       baseline=50,
 201:       era=50,
 202:       mutate = 0.3,
 203:       epsilon=0.01,
 204:       lives=5,
 205:       verbose=True,
 206:       nudge=1,
 207:       patience=64
 208:   )
 209:   
 210:   class Gadgets:
 211:     """Gadgets is a "facade"; i.e. a simplified 
 212:     interface to a body of code."""
 213:     def __init__(i,model):
 214:       i.model  = model
 215:       
 216:     def blank(i):
 217:       "return a new candidate, filled with None"
 218:       return i.model.clone(lambda _: None)
 219:     def logs(i,also=None):
 220:       "Return a new log, also linked to another log"
 221:       new = i.model.clone(lambda _ : Log())
 222:       for new1,also1 in new.alongWith(also):
 223:           new1.also = also1
 224:       return new
 225:     def log1(i,can,log):
 226:        [log1 + x for log1,x in log.alongWith(can)]
 227:     def logNews(i,log, news):
 228:       for can in news:
 229:         for x,log1 in zip(can.decs,log.decs):
 230:           log1 + x
 231:         for x,log1 in zip(can.objs,log.objs):
 232:           log1 + x
 233:         log.aggregate + i.aggregate(can,log)
 234:       return news
 235:         
 236:     def aFewBlanks(i):
 237:       patience = the.GADGETS.patience
 238:       while True:
 239:         yield i.blank()
 240:         patience -= 1
 241:         assert patience > 0, "constraints too hard to satisfy"
 242:   
 243:     def decs(i):
 244:       "return a new candidate, with guesses for decisions"
 245:       for can in i.aFewBlanks():
 246:         can.decs = [dec.maker() for dec in i.model.decs]
 247:         if i.model.ok(can):
 248:           return can
 249:     
 250:     def eval(i,can):
 251:       "expire the old aggregate. make the objective scores."
 252:       can.aggregate = None
 253:       can.objs = [obj.maker(can) for obj in i.model.objs]
 254:       return can
 255:   
 256:     def aggregate(i,can,logs):
 257:       "Return the aggregate. Side-effect: store it in the can"
 258:       if can.aggregate == None:
 259:          agg = n = 0
 260:          for obj,about,log in zip(can.objs,
 261:                                   i.model.objs,
 262:                                   logs.objs):
 263:            n   += 1
 264:            agg += about.fromHell(obj,log)
 265:          can.aggregate = agg ** 0.5 / n ** 0.5
 266:       return can.aggregate
 267:          
 268:     def mutate(i,can,logs,p):
 269:       "Return a new can with p% mutated"
 270:       for sn in i.aFewBlanks():
 271:         for n,(dec,about,log) in enumerate(zip(can.decs,
 272:                                              i.model.decs,
 273:                                              logs.decs)):
 274:           val = can.decs[n]
 275:           if p > r():
 276:             some = (log.hi - log.lo)*0.5
 277:             val  = val - some + 2*some*r()
 278:             val  = about.wrap(val)
 279:           sn.decs[n] = val
 280:         if i.model.ok(sn):
 281:           return sn
 282:         
 283:     def xPlusFyz(i,threeMore,cr,f):
 284:       "Crossovers some decisions, by a factor of 'f'"
 285:       def smear((x1, y1, z1, about)):
 286:         x1 = x1 if cr <= r() else x1 + f*(y1-z1)
 287:         return about.wrap(x1)
 288:       for sn in i.aFewBlanks():
 289:         x,y,z   = threeMore()
 290:         sn.decs = [smear(these)
 291:                    for these in zip(x.decs,
 292:                                     y.decs,
 293:                                     z.decs,
 294:                                     i.model.decs)]
 295:         if i.model.ok(sn):
 296:           return sn
 297:       
 298:     def news(i,n=None):
 299:       "Generating, say, 100 random instances."
 300:       return [i.eval( i.decs())
 301:               for _ in xrange(n or the.GADGETS.baseline)]
 302:   
 303:     def energy(i,can,logs):
 304:       "Returns an energy value to be minimized"
 305:       i.eval(can)
 306:       e = abs(1 - i.aggregate(can,logs))
 307:       if e < 0: e= 0
 308:       if e > 1: e= 1
 309:       return e
 310:     def better1(i,now,last):
 311:       better=worse=0
 312:       for now1,last1,about in zip(now.objs,
 313:                                   last.objs,
 314:                                   i.model.objs):
 315:         nowMed = median(now1.some())
 316:         lastMed= median(last1.some())
 317:         if about.better(nowMed, lastMed):
 318:           better += 1
 319:         elif nowMed != lastMed:
 320:           worse += 1
 321:       return better > 0 and worse < 1
 322:     def fyi(i,x)   : the.GADGETS.verbose and say(x)
 323:     def shout(i,x) : i.fyi("__" + x)
 324:     def bye(i,info,first,now) : i.fyi(info); return first,now
 325:   
 326:       
 327:   @setting
 328:   def SA(): return o(
 329:       p=0.25,
 330:       cooling=1,
 331:       kmax=1000)
 332:     
 333:   def sa(m,baseline=None,also2=None):
 334:     def goodbye(x)  : return g.bye(x,first,now)
 335:     g = Gadgets(m)
 336:     def p(old,new,t): return ee**((old - new)/t)
 337:     k,eb,life = 0,1,the.GADGETS.lives
 338:     #===== setting up logs
 339:     also     = g.logs(also2) # also = log of all eras
 340:     first    = now  = g.logs(also)
 341:     g.logNews(first,baseline or g.news())
 342:     last, now  = now, g.logs(also)
 343:     #===== ok to go
 344:     s = g.decs()
 345:     e = g.energy(s,now)
 346:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 347:     while True:
 348:       info="."
 349:       k += 1
 350:       t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 351:       sn = g.mutate(s, also,the.SA.p)
 352:       en = g.energy(sn,also)
 353:       g.log1(sn,now)
 354:       if en < eb:
 355:         sb,eb = sn,en
 356:         g.shout("!")
 357:       if en < e:
 358:         s,e = sn,en
 359:         info = "+"
 360:       elif p(e,en,t) < r():
 361:         s,e = sn, en
 362:         info="?"
 363:       if k % the.GADGETS.era: 
 364:         g.fyi(info)
 365:       else:
 366:         life = life - 1
 367:         if g.better1(now, last)     : life = the.GADGETS.lives 
 368:         if life < 1                 : return goodbye("L")
 369:         if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 370:         if k > the.SA.kmax          : return goodbye("K")
 371:         g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 372:         last, now  = now, g.logs(also) 
 373:   
 374:   
 375:   @setting
 376:   def DE(): return o(
 377:       cr = 0.4,
 378:       f  = 0.5,
 379:       npExpand = 10,
 380:       kmax=1000)
 381:     
 382:   def de(m,baseline=None,also2=None):
 383:     def goodbye(x)  : return g.bye(x,first,now)
 384:     g  = Gadgets(m)
 385:     np = len(g.model.decs) * the.DE.npExpand
 386:     k,eb,life = 0,1,the.GADGETS.lives
 387:     #===== setting up logs
 388:     also     = g.logs(also2) # also = log of all eras
 389:     first    = now  = g.logs(also)
 390:     frontier = g.logNews(first,baseline or g.news(np))
 391:     last, now  = now, g.logs(also)
 392:     #===== ok to go
 393:     sn = en = None
 394:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 395:     while True:
 396:       for n,parent in enumerate(frontier):
 397:         info="."
 398:         k += 1
 399:         e  = g.aggregate(parent, also)
 400:         sn = g.xPlusFyz(lambda: another3(frontier,parent),
 401:                         the.DE.cr,
 402:                         the.DE.f)
 403:         en = g.energy(sn,also)
 404:         g.log1(sn,now)
 405:         if en < eb:
 406:           sb,eb = sn,en
 407:           g.shout("!")
 408:         if en < e:
 409:           frontier[n] = sn # goodbye parent
 410:           info = "+"
 411:         g.fyi(info)
 412:       life = life - 1
 413:       if g.better1(now, last)     : life = the.GADGETS.lives 
 414:       if life < 1                 : return goodbye("L")
 415:       if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 416:       if k > the.DE.kmax          : return goodbye("K")
 417:       g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 418:       last, now  = now, g.logs(also) 
 419:   
 420:   def another3(lst, avoid=None):
 421:     def another1():
 422:       x = avoid
 423:       while id(x) in seen: 
 424:         x = lst[  int(random.uniform(0,len(lst))) ]
 425:       seen.append( id(x) )
 426:       return x
 427:     # -----------------------
 428:     assert len(lst) > 4
 429:     avoid = avoid or lst[0]
 430:     seen  = [ id(avoid) ]
 431:     return another1(), another1(), another1()
 432:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

