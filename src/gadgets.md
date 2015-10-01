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
for model in [Schaffer,Fonseca,...]:
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
  method-- either specified in an interface and
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

### `Candidate`s

`Candidate`s objects have  objectives, decisions and maybe some aggregate value. 
Using a factory method,  we will fill in `Candidate`s with either 

+ The specific values from one set `decs` and `objs, aggregate`;
+ Or, `Log`ging objects that remember what specific values were ever assigned to  `decs` and `objs, aggregate`;
+ Or, `About` objects that defined what are legel values from the specific values  
  (and, for `objs` if we want to minimize
  or maximize those scores)

In the following, I sometimes refer to `Candidate` objects as `can`. For example, the `ok` method
received a `can` and returns true if the current contents of `decs` are valid.

<a href="gadgets.py#L141-L185"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Candidate(object):
   2:     def __init__(i,decs=[],objs=[]):
   3:       i.decs,i.objs=decs,objs
   4:       i.aggregate=None
   5:       i.abouts = i.about()
   6:       
   7:     def __repr__(i):
   8:       "Present me in a  string"
   9:       return printer(i,decs=i.decs,
  10:                      objs=i.objs,
  11:                      aggregated=i.aggregate)
  12:   
  13:     def __getitem__(i,key):
  14:       "Simple way to access decs or objs or aggregates."
  15:       return i.__dict__[key]
  16:     
  17:     def ok(i,can):
  18:       "Maybe overwritten by subclass."
  19:       return True
  20:     
  21:     def about(i):
  22:       """Factory method for return a Candidate full of 
  23:          About objects."""
  24:       assert False,'implemented by subclass'
  25:       
  26:     
  27:     def clone(i,what = lambda _: None):
  28:       """A genetic factory that makes a new  thing
  29:          like receiver, filled in with 'what' objects."""
  30:       j      = object.__new__(i.__class__)
  31:       j.decs = [what(x) for x in i.decs]
  32:       j.objs = [what(x) for x in i.objs]
  33:       j.aggregate = what(i.aggregate)
  34:       j.abouts = i.abouts
  35:       return j
  36:     
  37:     def alongWith(i,j=None):
  38:       "Convenient iterator."
  39:       if j:
  40:         for one,two in zip(i.decs, j.decs):
  41:           yield one,two
  42:         for one,two in zip(i.objs, j.objs):
  43:           yield one,two
  44:         yield i.aggregate, j.aggregate
  45:         
```

Using the above, we can build a _factory_ method
called `about` that returns what we know `About`
each candidate.

#### Schaffer

One decision, two objectives, zero  constraints.

<a href="gadgets.py#L197-L207"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  46:   class Schaffer(Candidate):
  47:     def about(i):
  48:       def f1(can):
  49:         x = can.decs[0]
  50:         return x**2
  51:       def f2(can):
  52:         x = can.decs[0]
  53:         return (x-2)**2
  54:       i.decs = [An("x",   lo = -10**5, hi = 10**5)]
  55:       i.objs = [Less("f1",  maker=f1),
  56:                 Less("f2", maker=f2)]
```

In the above, `An` and `Less` are really `About` objects that define legal ranges for values 
 (and, for `objs` if we want to minimize
  or maximize those scores).

Note also that `f1` and `f2` are nested methods that accepted a `Candidate` object (which,
you will recall, I call `can`s).


#### Fonseca

One decisions, two objectives, zero constraints.

<a href="gadgets.py#L223-L236"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  57:   class Fonseca(Candidate):
  58:     n=3
  59:     def about(i):
  60:       def f1(can):
  61:         z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
  62:         return 1 - ee**(-1*z)
  63:       def f2(can):
  64:         z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
  65:         return 1 - ee**(-1*z)
  66:       def dec(x):
  67:         return An(x, lo=-4, hi=4)
  68:       i.decs = [dec(x) for x in range(Fonseca.n)]
  69:       i.objs = [Less("f1",  maker=f1),
  70:                 Less("f2",  maker=f2)]
```

Note the use of a list comprehension to create multiple decisions, all with similar properties.
This is handy here and, for more complex models like `ZDT1` with 30 decisions with similar properties,
it is very useful indeed.

#### Kursawe

Three decisions, two objectives,  zero constraints.

<a href="gadgets.py#L248-L261"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  71:   class Kursawe(Candidate):
  72:     def about(i,a=1,b=1):
  73:       def f1(can):
  74:         def xy(x,y):
  75:           return -10*ee**(-0.2*sqrt(x*x + y*y))
  76:         a,b,c = can.decs
  77:         return xy(a,b) + xy(b,c)
  78:       def f2(can):
  79:         return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  80:       def dec(x):
  81:         return  An(x, lo=-5, hi=5)           
  82:       i.decs = [dec(x) for x in range(3)]
  83:       i.objs = [Less("f1",  maker=f1),
  84:                 Less("f2",  maker=f2)]
```

#### ZDT1

Thirty decisions, two objectives,  zero constraints.

<a href="gadgets.py#L269-L281"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  85:   class ZDT1(Candidate):
  86:     n=30
  87:     def about(i):
  88:       def f1(can):
  89:         return can.decs[0]
  90:       def f2(can):
  91:         g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
  92:         return g*abs(1 - sqrt(can.decs[0]*g))
  93:       def dec(x):
  94:         return An(x,lo=0,hi=1)
  95:       i.decs = [dec(x) for x in range(ZDT1.n)]
  96:       i.objs = [Less("f1",maker=f1),
  97:                 Less("f2",maker=f2)]
```

Again, note the use of a list comprehension to create multiple decisions, all with similar properties.

#### Viennet4

Two decisions, three objectives,  three constraints (all codes into the `ok` method).

<a href="gadgets.py#L291-L313"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

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

### `Log`ging Objects 

Another kind of part that is assembled into a `Candidate` by a factory methods are
`Log` objects. These  remembers the range of values
seen so far.

Note one small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 

<a href="gadgets.py#L329-L355"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
 134:       i._some += x     # NOTE1
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
```
 
_NOTE1_ As a side-effect of logging, we also keep a small sample of
  the logged items This will come in handy... later. The code
for keeping _Some_ values is shown below.
   
<a href="gadgets.py#L363-L379"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 148:   @setting
 149:   def SOMES(): return o(
 150:       size=256
 151:       )
 152:   
 153:   class Some:
 154:     def __init__(i, max=None): 
 155:       i.n, i.any = 0,[]
 156:       i.max = max or the.SOMES.size
 157:     def __iadd__(i,x):
 158:       i.n += 1
 159:       now = len(i.any)
 160:       if now < i.max:    
 161:         i.any += [x]
 162:       elif r() <= now/i.n:
 163:         i.any[ int(r() * now) ]= x 
 164:       return i
```

### `About` Objects 

The `About` class (and its variants: `Less` and `More`) define our expectation for 
each `Candidate`
values.

If we need a value for a `Candidate`, we call `.maker()`:

+ For decisions,
  this just pulls a value from the known `hi` and `lo` ranges;
+ For objectives,
  call some `maker` function passed over an initialization time.

Note that `About` is a handy place to implement some useful services:

+ Checking if a value is `ok` (in bounds `lo..hi`);
+ `restrain`ing out of bound values back to `lo..hi`;
+ `wrap`ing out of bounds value via modulo;
+ How to compute the distance `fromHell`.

<a href="gadgets.py#L403-L429"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 165:   def lt(i,j): return i < j
 166:   def gt(i,j): return i > j
 167:   
 168:   class About(object):
 169:     def __init__(i, txt, init=None,
 170:                     lo=-10**32, hi=10**32,
 171:                     better=lt,
 172:                     maker=None):
 173:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 174:       i.maker = maker or i.guess
 175:       i.better= better
 176:     def __repr__(i):
 177:       return 'o'+str(i.__dict__)
 178:     def guess(i):
 179:       return i.lo + r()*(i.hi - i.lo)
 180:     def restrain(i,x):
 181:       return max(i.lo, min(i.hi, x))
 182:     def wrap(i,x):
 183:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 184:     def norm(i,x):
 185:       return (x - i.lo) / (i.hi - i.lo + 10**-32)
 186:     def ok(i,x):
 187:       return i.lo <= x <= i.hi
 188:     def fromHell(i,x,log,min=None,max=None):
 189:       norm = i.norm if log.lo == None else log.norm
 190:       hell = 1 if i.better == lt else 0
 191:       return (hell - norm(x)) ** 2
```

Note that many of the above will be called many times as we (e.g.) fill in the decisions
of a `can` (e.g. `guess`, `wrap`, `norm`) or its objectives (e.g. `fromHell`).
 
Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L439-L442"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 192:   A = An = Less = About
 193:   
 194:   def More(txt,*lst,**d):
 195:     return About(txt,*lst,better=gt,**d)
```

## The `Gadgets` Facade

Note that `Gadgets` stores most of the generic processing
of my optimizers. Hence the control params of `Gadgets`
is really the control params of most of the optimization.

<a href="gadgets.py#L452-L462"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 196:   @setting
 197:   def GADGETS(): return  o(
 198:       baseline=50,
 199:       era=50,
 200:       mutate = 0.3,
 201:       epsilon=0.01,
 202:       lives=5,
 203:       verbose=True,
 204:       nudge=1,
 205:       patience=64
 206:   )
```

```
g = Gadgets(Schaffer())
```

(Note the brackets-- this creates a new instance.)

Here is the `Gadgets` facade. Note that it offers a wide range of services
including:

+ Factory methods for generating empty `can`s, or `can`s filled with `Log`s.
+ 

<a href="gadgets.py#L478-L628"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 207:   class Gadgets:
 208:     def __init__(i,abouts):
 209:       i.abouts  = abouts
 210:   
 211:     ### Factory methods ###
 212:   
 213:     def blank(i):
 214:       "Factory for candidate objects containing Nones"
 215:       return i.abouts.clone(lambda _: None)
 216:   
 217:     def logs(i,also=None):
 218:       "Factory for candidate objects containing Logs"
 219:       new = i.abouts.clone(lambda _ : Log())
 220:       for new1,also1 in new.alongWith(also):
 221:           new1.also = also1
 222:       return new
 223:   
 224:     ##### Logging methods #####
 225:   
 226:     def log1(i,can,log):
 227:       "Stores values from 'can' into 'log'."
 228:       [log1 + x for log1,x in log.alongWith(can)]
 229:       
 230:     def logNews(i,log, news):
 231:       """Stores values from a list of cans, called 'news'
 232:          into a log. Does not use 'log1' since this
 233:          also calls the 'aggregate' method."""
 234:       for can in news:
 235:         for x,log1 in zip(can.decs,log.decs):
 236:           log1 + x
 237:         for x,log1 in zip(can.objs,log.objs):
 238:           log1 + x
 239:         log.aggregate + i.aggregate(can,log)
 240:       return news
 241:   
 242:     ##### Filling in decisions #####
 243:     
 244:     def aFewBlanks(i):
 245:       """ Handles instantiation with constraints.
 246:           If can't  make  new instance after some repeats, crash."""
 247:       patience = the.GADGETS.patience
 248:       while True:
 249:         yield i.blank()
 250:         patience -= 1
 251:         assert patience > 0, "constraints too hard to satisfy"
 252:   
 253:     def decs(i):
 254:       "return a new candidate, with guesses for decisions"
 255:       for can in i.aFewBlanks():
 256:         can.decs = [dec.maker() for dec in i.abouts.decs]
 257:         if i.abouts.ok(can):
 258:           return can
 259:   
 260:     ##### Filling in objectives #####
 261:     
 262:     def eval(i,can):
 263:       "expire the old aggregate. make the objective scores."
 264:       can.aggregate = None
 265:       can.objs = [obj.maker(can) for obj in i.abouts.objs]
 266:       return can
 267:   
 268:     def aggregate(i,can,logs):
 269:       "Return the aggregate. Side-effect: store it in the can"
 270:       if can.aggregate == None:
 271:          agg = n = 0
 272:          for obj,about,log in zip(can.objs,
 273:                                   i.abouts.objs,
 274:                                   logs.objs):
 275:            n   += 1
 276:            agg += about.fromHell(obj,log)
 277:          can.aggregate = agg ** 0.5 / n ** 0.5
 278:       return can.aggregate
 279:   
 280:     ##### Mutation methods #####
 281:          
 282:     def mutate(i,can,logs,p):
 283:       "Return a new can with p% mutated"
 284:       for sn in i.aFewBlanks():
 285:         for n,(dec,about,log) in enumerate(zip(can.decs,
 286:                                              i.abouts.decs,
 287:                                              logs.decs)):
 288:           val = can.decs[n]
 289:           if p > r():
 290:             some = (log.hi - log.lo)*0.5
 291:             val  = val - some + 2*some*r()
 292:             val  = about.wrap(val)
 293:           sn.decs[n] = val
 294:         if i.abouts.ok(sn):
 295:           return sn
 296:         
 297:     def xPlusFyz(i,threeMore,cr,f):
 298:       "Crossovers some decisions, by a factor of 'f'"
 299:       def smear((x1, y1, z1, about)):
 300:         x1 = x1 if cr <= r() else x1 + f*(y1-z1)
 301:         return about.wrap(x1)
 302:       for sn in i.aFewBlanks():
 303:         x,y,z   = threeMore()
 304:         sn.decs = [smear(these)
 305:                    for these in zip(x.decs,
 306:                                     y.decs,
 307:                                     z.decs,
 308:                                     i.abouts.decs)]
 309:         if i.abouts.ok(sn):
 310:           return sn
 311:   
 312:     ##### Fully filling in many candidates #####
 313:     
 314:     def news(i,n=None):
 315:       "Generating, say, 100 random instances."
 316:       return [i.eval( i.decs())
 317:               for _ in xrange(n or the.GADGETS.baseline)]
 318:   
 319:     ##### Evaluation of candidates #####
 320:     
 321:     def energy(i,can,logs):
 322:       "Returns an energy value to be minimized"
 323:       i.eval(can)
 324:       e = abs(1 - i.aggregate(can,logs))
 325:       if e < 0: e= 0
 326:       if e > 1: e= 1
 327:       return e
 328:     
 329:     def better1(i,now,last):
 330:       "Is one era better than another?"
 331:       better=worse=0
 332:       for now1,last1,about in zip(now.objs,
 333:                                   last.objs,
 334:                                   i.abouts.objs):
 335:         nowMed = median(now1.some())
 336:         lastMed= median(last1.some())
 337:         if about.better(nowMed, lastMed):
 338:           better += 1
 339:         elif nowMed != lastMed:
 340:           worse += 1
 341:       return better > 0 and worse < 1
 342:   
 343:     ##### Pretty printing #####
 344:       
 345:     def fyi(i,x)   :
 346:       "Maybe, mention something"
 347:       the.GADGETS.verbose and say(x)
 348:       
 349:     def shout(i,x) :
 350:       "Add an emphasis to an output."
 351:       i.fyi("__" + x)
 352:       
 353:     def bye(i,info,first,now) :
 354:       """Optimizers return the distribution of values seen in
 355:          first and final era"""
 356:       i.fyi(info)
 357:       return first,now
```

## Optimizers

Finally, we can build our optimizers. Note that the following:

+ Process a model in `era`s
+ May stop early after a sequence of unpromising `era`s.
+ May stop early if we get too close to zero
+ Either create a baseline era or accepts a baseline `first` era
  passed in as a parameter.
+ When generating logs, if there is an outer log, store values in this
  log as well as the outer.

### Simulated Annealling

<a href="gadgets.py#L646-L691"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 358:   @setting
 359:   def SA(): return o(
 360:       p=0.25,
 361:       cooling=1,
 362:       kmax=1000)
 363:     
 364:   def sa(m,baseline=None,also2=None):
 365:     def goodbye(x)  : return g.bye(x,first,now)
 366:     g = Gadgets(m)
 367:     def p(old,new,t): return ee**((old - new)/t)
 368:     k,eb,life = 0,1,the.GADGETS.lives
 369:     #===== setting up logs
 370:     also     = g.logs(also2) # log of all eras
 371:     first    = now  = g.logs(also)
 372:     g.logNews(first,baseline or g.news())
 373:     last, now  = now, g.logs(also)
 374:     #===== ok to go
 375:     s = g.decs()
 376:     e = g.energy(s,now)
 377:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 378:     while True:
 379:       info="."
 380:       k += 1
 381:       t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 382:       sn = g.mutate(s, also,the.SA.p)
 383:       en = g.energy(sn,also)
 384:       g.log1(sn,now)
 385:       if en < eb:
 386:         sb,eb = sn,en
 387:         g.shout("!")
 388:       if en < e:
 389:         s,e = sn,en
 390:         info = "+"
 391:       elif p(e,en,t) < r():
 392:         s,e = sn, en
 393:         info="?"
 394:       if k % the.GADGETS.era: 
 395:         g.fyi(info)
 396:       else:
 397:         life = life - 1
 398:         if g.better1(now, last)     : life = the.GADGETS.lives 
 399:         if life < 1                 : return goodbye("L")
 400:         if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 401:         if k > the.SA.kmax          : return goodbye("K")
 402:         g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 403:         last, now  = now, g.logs(also) 
```

### Differential Evolution

<a href="gadgets.py#L697-L740"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 404:   @setting
 405:   def DE(): return o(
 406:       cr = 0.4,
 407:       f  = 0.5,
 408:       npExpand = 10,
 409:       kmax=1000)
 410:     
 411:   def de(m,baseline=None,also2=None):
 412:     def goodbye(x)  : return g.bye(x,first,now)
 413:     g  = Gadgets(m)
 414:     np = len(g.abouts.decs) * the.DE.npExpand
 415:     k,eb,life = 0,1,the.GADGETS.lives
 416:     #===== setting up logs
 417:     also     = g.logs(also2) # also = log of all eras
 418:     first    = now  = g.logs(also)
 419:     frontier = g.logNews(first,baseline or g.news(np))
 420:     last, now  = now, g.logs(also)
 421:     #===== ok to go
 422:     sn = en = None
 423:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 424:     while True:
 425:       for n,parent in enumerate(frontier):
 426:         info="."
 427:         k += 1
 428:         e  = g.aggregate(parent, also)
 429:         sn = g.xPlusFyz(lambda: another3(frontier,parent),
 430:                         the.DE.cr,
 431:                         the.DE.f)
 432:         en = g.energy(sn,also)
 433:         g.log1(sn,now)
 434:         if en < eb:
 435:           sb,eb = sn,en
 436:           g.shout("!")
 437:         if en < e:
 438:           frontier[n] = sn # goodbye parent
 439:           info = "+"
 440:         g.fyi(info)
 441:       life = life - 1
 442:       if g.better1(now, last)     : life = the.GADGETS.lives 
 443:       if life < 1                 : return goodbye("L")
 444:       if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 445:       if k > the.DE.kmax          : return goodbye("K")
 446:       g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 447:       last, now  = now, g.logs(also) 
```

DE trick for finding three unique things in a list that are not `avoid`.

<a href="gadgets.py#L746-L758"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 448:   def another3(lst, avoid=None):
 449:     def another1():
 450:       x = avoid
 451:       while id(x) in seen: 
 452:         x = lst[  int(random.uniform(0,len(lst))) ]
 453:       seen.append( id(x) )
 454:       return x
 455:     # -----------------------
 456:     assert len(lst) > 4
 457:     avoid = avoid or lst[0]
 458:     seen  = [ id(avoid) ]
 459:     return another1(), another1(), another1()
 460:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

