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

<a href="gadgets.py#L140-L182"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Candidate(object):
   2:     def __init__(i,decs=[],objs=[]):
   3:       i.decs,i.objs=decs,objs
   4:       i.aggregate=None
   5:       #i.abouts = i.about()
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
  33:       #j.abouts = i.abouts
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

One decision, two objectives, zero  constraints.

<a href="gadgets.py#L193-L203"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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

One decisions, two objectives, zero constraints.

<a href="gadgets.py#L219-L232"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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

Note the use of a list comprehension to create multiple decisions, all with similar properties.
This is handy here and, for more complex models like `ZDT1` with 30 decisions with similar properties,
it is very useful indeed.

#### Kursawe

Three decisions, two objectives,  zero constraints.

<a href="gadgets.py#L244-L257"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
```

#### ZDT1

Thirty decisions, two objectives,  zero constraints.

<a href="gadgets.py#L265-L277"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  83:   class ZDT1(Candidate):
  84:     n=30
  85:     def about(i):
  86:       def f1(can):
  87:         return can.decs[0]
  88:       def f2(can):
  89:         g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
  90:         return g*abs(1 - sqrt(can.decs[0]*g))
  91:       def dec(x):
  92:         return An(x,lo=0,hi=1)
  93:       i.decs = [dec(x) for x in range(ZDT1.n)]
  94:       i.objs = [Less("f1",maker=f1),
  95:                 Less("f2",maker=f2)]
```

Again, note the use of a list comprehension to create multiple decisions, all with similar properties.

#### Viennet4

Two decisions, three objectives,  three constraints (all codes into the `ok` method).

<a href="gadgets.py#L287-L309"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  96:   class Viennet4(Candidate):
  97:     def ok(i,can):
  98:        one,two = can.decs
  99:        g1 = -1*two - 4*one + 4
 100:        g2 = one + 1            
 101:        g3 = two - one + 2
 102:        return g1 >= 0 and g2 >= 0 and g3 >= 0
 103:     def about(i):
 104:       def f1(can):
 105:         one,two = can.decs
 106:         return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
 107:       def f2(can):
 108:         one,two = can.decs
 109:         return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
 110:       def f3(can):
 111:         one,two= can.decs
 112:         return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
 113:       def dec(x):
 114:         return An(x,lo= -4,hi= 4)
 115:       i.decs = [dec(x) for x in range(2)]
 116:       i.objs = [Less("f1",maker=f1),
 117:                 Less("f2",maker=f2),
 118:                 Less("f3",maker=f3)]
```

### `Log`ging Objects 

Another kind of part that is assembled into a `Candidate` by a factory methods are
`Log` objects. These  remembers the range of values
seen so far.

Note one small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 

<a href="gadgets.py#L325-L351"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 119:   class Log:
 120:     def __init__(i,init=[],also=None):
 121:       i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
 122:       map(i.__add__,init)
 123:     def adds(i,lst):
 124:       map(i.__add__,lst)
 125:     def __add__(i,x):
 126:       i.n += 1
 127:       if   i.empty() : i.lo = i.hi = x # auto-initialize
 128:       elif x > i.hi     : i.hi = x
 129:       elif x < i.lo     : i.lo = x
 130:       if i.also:
 131:         i.also + x
 132:       i._some += x     # NOTE1
 133:       return x
 134:     def some(i):
 135:       return i._some.any
 136:     def tiles(i,tiles=None,ordered=False,n=3):
 137:       return r3(ntiles(i.some(),tiles,ordered),n)
 138:     def empty(i):
 139:       return i.lo == None
 140:     def norm(i,x):
 141:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
 142:     def stats(i,tiles=[0.25,0.5,0.75]):
 143:       return ntiles(sorted(i._some.any),
 144:              ordered=False, 
 145:              tiles=tiles)
```
 
_NOTE1_ As a side-effect of logging, we also keep a small sample of
  the logged items This will come in handy... later. The code
for keeping _Some_ values is shown below.
   
<a href="gadgets.py#L359-L375"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 146:   @setting
 147:   def SOMES(): return o(
 148:       size=256
 149:       )
 150:   
 151:   class Some:
 152:     def __init__(i, max=None): 
 153:       i.n, i.any = 0,[]
 154:       i.max = max or the.SOMES.size
 155:     def __iadd__(i,x):
 156:       i.n += 1
 157:       now = len(i.any)
 158:       if now < i.max:    
 159:         i.any += [x]
 160:       elif r() <= now/i.n:
 161:         i.any[ int(r() * now) ]= x 
 162:       return i
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

<a href="gadgets.py#L399-L425"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 163:   def lt(i,j): return i < j
 164:   def gt(i,j): return i > j
 165:   
 166:   class About(object):
 167:     def __init__(i, txt, init=None,
 168:                     lo=-10**32, hi=10**32,
 169:                     better=lt,
 170:                     maker=None):
 171:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 172:       i.maker = maker or i.guess
 173:       i.better= better
 174:     def __repr__(i):
 175:       return 'o'+str(i.__dict__)
 176:     def guess(i):
 177:       return i.lo + r()*(i.hi - i.lo)
 178:     def restrain(i,x):
 179:       return max(i.lo, min(i.hi, x))
 180:     def wrap(i,x):
 181:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 182:     def norm(i,x):
 183:       return (x - i.lo) / (i.hi - i.lo + 10**-32)
 184:     def ok(i,x):
 185:       return i.lo <= x <= i.hi
 186:     def fromHell(i,x,log,min=None,max=None):
 187:       norm = i.norm if log.lo == None else log.norm
 188:       hell = 1 if i.better == lt else 0
 189:       return (hell - norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L432-L435"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 190:   A = An = Less = About
 191:   
 192:   def More(txt,*lst,**d):
 193:     return About(txt,*lst,better=gt,**d)
```

## The `Gadgets` Facade

Note that `Gadgets` stores most of the generic processing
of my optimizers. Hence the control params of `Gadgets`
is really the control params of most of the optimization.

<a href="gadgets.py#L445-L455"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 194:   @setting
 195:   def GADGETS(): return  o(
 196:       baseline=50,
 197:       era=50,
 198:       mutate = 0.3,
 199:       epsilon=0.01,
 200:       lives=5,
 201:       verbose=True,
 202:       nudge=1,
 203:       patience=64
 204:   )
```

Gadgets are created from a `model` (which is one of the  subclasses of `Candidate`). For exmaple

```
m = Gadgets(Schaffer())
```

Note the brackets after the model name-- this creates a new instance of that model.

<a href="gadgets.py#L467-L600"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 205:   class Gadgets:
 206:     def __init__(i,model):
 207:       i.model  = model
 208:       
 209:     def blank(i):
 210:       "Factory for candidate objects containing Nones"
 211:       return i.model.clone(lambda _: None)
 212:     
 213:     def logs(i,also=None):
 214:       "Factory for candidate objects containing Logs"
 215:       new = i.model.clone(lambda _ : Log())
 216:       for new1,also1 in new.alongWith(also):
 217:           new1.also = also1
 218:       return new
 219:     
 220:     def log1(i,can,log):
 221:       "Stores values from 'can' into 'log'."
 222:       [log1 + x for log1,x in log.alongWith(can)]
 223:       
 224:     def logNews(i,log, news):
 225:       """Stores values from a list of cans, called 'news'
 226:          into a log."""
 227:       for can in news:
 228:         for x,log1 in zip(can.decs,log.decs):
 229:           log1 + x
 230:         for x,log1 in zip(can.objs,log.objs):
 231:           log1 + x
 232:         log.aggregate + i.aggregate(can,log)
 233:       return news
 234:         
 235:     def aFewBlanks(i):
 236:       """ Handles instantiation with constraints.
 237:           If can't  make  newinstance after some repeats, crash."""
 238:       patience = the.GADGETS.patience
 239:       while True:
 240:         yield i.blank()
 241:         patience -= 1
 242:         assert patience > 0, "constraints too hard to satisfy"
 243:   
 244:     def decs(i):
 245:       "return a new candidate, with guesses for decisions"
 246:       for can in i.aFewBlanks():
 247:         can.decs = [dec.maker() for dec in i.model.decs]
 248:         if i.model.ok(can):
 249:           return can
 250:     
 251:     def eval(i,can):
 252:       "expire the old aggregate. make the objective scores."
 253:       can.aggregate = None
 254:       can.objs = [obj.maker(can) for obj in i.model.objs]
 255:       return can
 256:   
 257:     def aggregate(i,can,logs):
 258:       "Return the aggregate. Side-effect: store it in the can"
 259:       if can.aggregate == None:
 260:          agg = n = 0
 261:          for obj,about,log in zip(can.objs,
 262:                                   i.model.objs,
 263:                                   logs.objs):
 264:            n   += 1
 265:            agg += about.fromHell(obj,log)
 266:          can.aggregate = agg ** 0.5 / n ** 0.5
 267:       return can.aggregate
 268:          
 269:     def mutate(i,can,logs,p):
 270:       "Return a new can with p% mutated"
 271:       for sn in i.aFewBlanks():
 272:         for n,(dec,about,log) in enumerate(zip(can.decs,
 273:                                              i.model.decs,
 274:                                              logs.decs)):
 275:           val = can.decs[n]
 276:           if p > r():
 277:             some = (log.hi - log.lo)*0.5
 278:             val  = val - some + 2*some*r()
 279:             val  = about.wrap(val)
 280:           sn.decs[n] = val
 281:         if i.model.ok(sn):
 282:           return sn
 283:         
 284:     def xPlusFyz(i,threeMore,cr,f):
 285:       "Crossovers some decisions, by a factor of 'f'"
 286:       def smear((x1, y1, z1, about)):
 287:         x1 = x1 if cr <= r() else x1 + f*(y1-z1)
 288:         return about.wrap(x1)
 289:       for sn in i.aFewBlanks():
 290:         x,y,z   = threeMore()
 291:         sn.decs = [smear(these)
 292:                    for these in zip(x.decs,
 293:                                     y.decs,
 294:                                     z.decs,
 295:                                     i.model.decs)]
 296:         if i.model.ok(sn):
 297:           return sn
 298:       
 299:     def news(i,n=None):
 300:       "Generating, say, 100 random instances."
 301:       return [i.eval( i.decs())
 302:               for _ in xrange(n or the.GADGETS.baseline)]
 303:   
 304:     def energy(i,can,logs):
 305:       "Returns an energy value to be minimized"
 306:       i.eval(can)
 307:       e = abs(1 - i.aggregate(can,logs))
 308:       if e < 0: e= 0
 309:       if e > 1: e= 1
 310:       return e
 311:     
 312:     def better1(i,now,last):
 313:       "Is one era better than another?"
 314:       better=worse=0
 315:       for now1,last1,about in zip(now.objs,
 316:                                   last.objs,
 317:                                   i.model.objs):
 318:         nowMed = median(now1.some())
 319:         lastMed= median(last1.some())
 320:         if about.better(nowMed, lastMed):
 321:           better += 1
 322:         elif nowMed != lastMed:
 323:           worse += 1
 324:       return better > 0 and worse < 1
 325:     
 326:     def fyi(i,x)   :
 327:       "Maybe, mention something"
 328:       the.GADGETS.verbose and say(x)
 329:       
 330:     def shout(i,x) :
 331:       "Add an emphasis to an output."
 332:       i.fyi("__" + x)
 333:       
 334:     def bye(i,info,first,now) :
 335:       """Optimizers return the distribution of values seen in
 336:          first and final era"""
 337:       i.fyi(info)
 338:       return first,now
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

<a href="gadgets.py#L618-L663"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 339:   @setting
 340:   def SA(): return o(
 341:       p=0.25,
 342:       cooling=1,
 343:       kmax=1000)
 344:     
 345:   def sa(m,baseline=None,also2=None):
 346:     def goodbye(x)  : return g.bye(x,first,now)
 347:     g = Gadgets(m)
 348:     def p(old,new,t): return ee**((old - new)/t)
 349:     k,eb,life = 0,1,the.GADGETS.lives
 350:     #===== setting up logs
 351:     also     = g.logs(also2) # also = log of all eras
 352:     first    = now  = g.logs(also)
 353:     g.logNews(first,baseline or g.news())
 354:     last, now  = now, g.logs(also)
 355:     #===== ok to go
 356:     s = g.decs()
 357:     e = g.energy(s,now)
 358:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 359:     while True:
 360:       info="."
 361:       k += 1
 362:       t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 363:       sn = g.mutate(s, also,the.SA.p)
 364:       en = g.energy(sn,also)
 365:       g.log1(sn,now)
 366:       if en < eb:
 367:         sb,eb = sn,en
 368:         g.shout("!")
 369:       if en < e:
 370:         s,e = sn,en
 371:         info = "+"
 372:       elif p(e,en,t) < r():
 373:         s,e = sn, en
 374:         info="?"
 375:       if k % the.GADGETS.era: 
 376:         g.fyi(info)
 377:       else:
 378:         life = life - 1
 379:         if g.better1(now, last)     : life = the.GADGETS.lives 
 380:         if life < 1                 : return goodbye("L")
 381:         if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 382:         if k > the.SA.kmax          : return goodbye("K")
 383:         g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 384:         last, now  = now, g.logs(also) 
```

### Differential Evolution

<a href="gadgets.py#L669-L712"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 385:   @setting
 386:   def DE(): return o(
 387:       cr = 0.4,
 388:       f  = 0.5,
 389:       npExpand = 10,
 390:       kmax=1000)
 391:     
 392:   def de(m,baseline=None,also2=None):
 393:     def goodbye(x)  : return g.bye(x,first,now)
 394:     g  = Gadgets(m)
 395:     np = len(g.model.decs) * the.DE.npExpand
 396:     k,eb,life = 0,1,the.GADGETS.lives
 397:     #===== setting up logs
 398:     also     = g.logs(also2) # also = log of all eras
 399:     first    = now  = g.logs(also)
 400:     frontier = g.logNews(first,baseline or g.news(np))
 401:     last, now  = now, g.logs(also)
 402:     #===== ok to go
 403:     sn = en = None
 404:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 405:     while True:
 406:       for n,parent in enumerate(frontier):
 407:         info="."
 408:         k += 1
 409:         e  = g.aggregate(parent, also)
 410:         sn = g.xPlusFyz(lambda: another3(frontier,parent),
 411:                         the.DE.cr,
 412:                         the.DE.f)
 413:         en = g.energy(sn,also)
 414:         g.log1(sn,now)
 415:         if en < eb:
 416:           sb,eb = sn,en
 417:           g.shout("!")
 418:         if en < e:
 419:           frontier[n] = sn # goodbye parent
 420:           info = "+"
 421:         g.fyi(info)
 422:       life = life - 1
 423:       if g.better1(now, last)     : life = the.GADGETS.lives 
 424:       if life < 1                 : return goodbye("L")
 425:       if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 426:       if k > the.DE.kmax          : return goodbye("K")
 427:       g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 428:       last, now  = now, g.logs(also) 
```

DE trick for finding three unique things in a list that are not `avoid`.

<a href="gadgets.py#L718-L730"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 429:   def another3(lst, avoid=None):
 430:     def another1():
 431:       x = avoid
 432:       while id(x) in seen: 
 433:         x = lst[  int(random.uniform(0,len(lst))) ]
 434:       seen.append( id(x) )
 435:       return x
 436:     # -----------------------
 437:     assert len(lst) > 4
 438:     avoid = avoid or lst[0]
 439:     seen  = [ id(avoid) ]
 440:     return another1(), another1(), another1()
 441:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

