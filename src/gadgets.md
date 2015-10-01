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

<a href="gadgets.py#L141-L184"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
  44:         
```

Using the above, we can build a _factory_ method
called `about` that returns what we know `About`
each candidate.

#### Schaffer

One decision, two objectives, zero  constraints.

<a href="gadgets.py#L196-L206"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  45:   class Schaffer(Candidate):
  46:     def about(i):
  47:       def f1(can):
  48:         x = can.decs[0]
  49:         return x**2
  50:       def f2(can):
  51:         x = can.decs[0]
  52:         return (x-2)**2
  53:       i.decs = [An("x",   lo = -10**5, hi = 10**5)]
  54:       i.objs = [Less("f1",  maker=f1),
  55:                 Less("f2", maker=f2)]
```

In the above, `An` and `Less` are really `About` objects that define legal ranges for values 
 (and, for `objs` if we want to minimize
  or maximize those scores).

Note also that `f1` and `f2` are nested methods that accepted a `Candidate` object (which,
you will recall, I call `can`s).


#### Fonseca

One decisions, two objectives, zero constraints.

<a href="gadgets.py#L222-L235"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  56:   class Fonseca(Candidate):
  57:     n=3
  58:     def about(i):
  59:       def f1(can):
  60:         z = sum([(x - 1/sqrt(Fonseca.n))**2 for x in can.decs])
  61:         return 1 - ee**(-1*z)
  62:       def f2(can):
  63:         z = sum([(x + 1/sqrt(Fonseca.n))**2 for x in can.decs])
  64:         return 1 - ee**(-1*z)
  65:       def dec(x):
  66:         return An(x, lo=-4, hi=4)
  67:       i.decs = [dec(x) for x in range(Fonseca.n)]
  68:       i.objs = [Less("f1",  maker=f1),
  69:                 Less("f2",  maker=f2)]
```

Note the use of a list comprehension to create multiple decisions, all with similar properties.
This is handy here and, for more complex models like `ZDT1` with 30 decisions with similar properties,
it is very useful indeed.

#### Kursawe

Three decisions, two objectives,  zero constraints.

<a href="gadgets.py#L247-L260"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  70:   class Kursawe(Candidate):
  71:     def about(i,a=1,b=1):
  72:       def f1(can):
  73:         def xy(x,y):
  74:           return -10*ee**(-0.2*sqrt(x*x + y*y))
  75:         a,b,c = can.decs
  76:         return xy(a,b) + xy(b,c)
  77:       def f2(can):
  78:         return sum( (abs(x)**a + 5*sin(x)**b) for x in can.decs )
  79:       def dec(x):
  80:         return  An(x, lo=-5, hi=5)           
  81:       i.decs = [dec(x) for x in range(3)]
  82:       i.objs = [Less("f1",  maker=f1),
  83:                 Less("f2",  maker=f2)]
```

#### ZDT1

Thirty decisions, two objectives,  zero constraints.

<a href="gadgets.py#L268-L280"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

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
```

Again, note the use of a list comprehension to create multiple decisions, all with similar properties.

#### Viennet4

Two decisions, three objectives,  three constraints (all codes into the `ok` method).

<a href="gadgets.py#L290-L312"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  97:   class Viennet4(Candidate):
  98:     def ok(i,can):
  99:        one,two = can.decs
 100:        g1 = -1*two - 4*one + 4
 101:        g2 = one + 1            
 102:        g3 = two - one + 2
 103:        return g1 >= 0 and g2 >= 0 and g3 >= 0
 104:     def about(i):
 105:       def f1(can):
 106:         one,two = can.decs
 107:         return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
 108:       def f2(can):
 109:         one,two = can.decs
 110:         return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
 111:       def f3(can):
 112:         one,two= can.decs
 113:         return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
 114:       def dec(x):
 115:         return An(x,lo= -4,hi= 4)
 116:       i.decs = [dec(x) for x in range(2)]
 117:       i.objs = [Less("f1",maker=f1),
 118:                 Less("f2",maker=f2),
 119:                 Less("f3",maker=f3)]
```

### `Log`ging Objects 

Another kind of part that is assembled into a `Candidate` by a factory methods are
`Log` objects. These  remembers the range of values
seen so far.

Note one small details about these `Log`s:

+ Sometimes we are logging information
  about one run within other runs. So `Log` has an `also` pointer
  which, if non-nil, is another place to repeat the same information. 

<a href="gadgets.py#L328-L354"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 120:   class Log:
 121:     def __init__(i,init=[],also=None):
 122:       i.n,i.lo, i.hi, i.also, i._some= 0,None, None, also,Some()
 123:       map(i.__add__,init)
 124:     def adds(i,lst):
 125:       map(i.__add__,lst)
 126:     def __add__(i,x):
 127:       i.n += 1
 128:       if   i.empty() : i.lo = i.hi = x # auto-initialize
 129:       elif x > i.hi     : i.hi = x
 130:       elif x < i.lo     : i.lo = x
 131:       if i.also:
 132:         i.also + x
 133:       i._some += x     # NOTE1
 134:       return x
 135:     def some(i):
 136:       return i._some.any
 137:     def tiles(i,tiles=None,ordered=False,n=3):
 138:       return r3(ntiles(i.some(),tiles,ordered),n)
 139:     def empty(i):
 140:       return i.lo == None
 141:     def norm(i,x):
 142:       return (x - i.lo)/(i.hi - i.lo + 10**-32)
 143:     def stats(i,tiles=[0.25,0.5,0.75]):
 144:       return ntiles(sorted(i._some.any),
 145:              ordered=False, 
 146:              tiles=tiles)
```
 
_NOTE1_ As a side-effect of logging, we also keep a small sample of
  the logged items This will come in handy... later. The code
for keeping _Some_ values is shown below.
   
<a href="gadgets.py#L362-L378"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 147:   @setting
 148:   def SOMES(): return o(
 149:       size=256
 150:       )
 151:   
 152:   class Some:
 153:     def __init__(i, max=None): 
 154:       i.n, i.any = 0,[]
 155:       i.max = max or the.SOMES.size
 156:     def __iadd__(i,x):
 157:       i.n += 1
 158:       now = len(i.any)
 159:       if now < i.max:    
 160:         i.any += [x]
 161:       elif r() <= now/i.n:
 162:         i.any[ int(r() * now) ]= x 
 163:       return i
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

<a href="gadgets.py#L402-L428"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 164:   def lt(i,j): return i < j
 165:   def gt(i,j): return i > j
 166:   
 167:   class About(object):
 168:     def __init__(i, txt, init=None,
 169:                     lo=-10**32, hi=10**32,
 170:                     better=lt,
 171:                     maker=None):
 172:       i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
 173:       i.maker = maker or i.guess
 174:       i.better= better
 175:     def __repr__(i):
 176:       return 'o'+str(i.__dict__)
 177:     def guess(i):
 178:       return i.lo + r()*(i.hi - i.lo)
 179:     def restrain(i,x):
 180:       return max(i.lo, min(i.hi, x))
 181:     def wrap(i,x):
 182:       return i.lo + (x - i.lo) % (i.hi - i.lo)
 183:     def norm(i,x):
 184:       return (x - i.lo) / (i.hi - i.lo + 10**-32)
 185:     def ok(i,x):
 186:       return i.lo <= x <= i.hi
 187:     def fromHell(i,x,log,min=None,max=None):
 188:       norm = i.norm if log.lo == None else log.norm
 189:       hell = 1 if i.better == lt else 0
 190:       return (hell - norm(x)) ** 2
```

Using the above, we can succinctly specify objectives
that want to minimize or maximize their values.

<a href="gadgets.py#L435-L438"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 191:   A = An = Less = About
 192:   
 193:   def More(txt,*lst,**d):
 194:     return About(txt,*lst,better=gt,**d)
```

## The `Gadgets` Facade

Note that `Gadgets` stores most of the generic processing
of my optimizers. Hence the control params of `Gadgets`
is really the control params of most of the optimization.

<a href="gadgets.py#L448-L458"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 195:   @setting
 196:   def GADGETS(): return  o(
 197:       baseline=50,
 198:       era=50,
 199:       mutate = 0.3,
 200:       epsilon=0.01,
 201:       lives=5,
 202:       verbose=True,
 203:       nudge=1,
 204:       patience=64
 205:   )
```

Gadgets are created from a `model` (which is one of the  subclasses of `Candidate`). For exmaple

```
m = Gadgets(Schaffer())
```

Note the brackets after the model name-- this creates a new instance of that model.

<a href="gadgets.py#L470-L603"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 206:   class Gadgets:
 207:     def __init__(i,model):
 208:       i.model  = model
 209:       
 210:     def blank(i):
 211:       "Factory for candidate objects containing Nones"
 212:       return i.model.clone(lambda _: None)
 213:     
 214:     def logs(i,also=None):
 215:       "Factory for candidate objects containing Logs"
 216:       new = i.model.clone(lambda _ : Log())
 217:       for new1,also1 in new.alongWith(also):
 218:           new1.also = also1
 219:       return new
 220:     
 221:     def log1(i,can,log):
 222:       "Stores values from 'can' into 'log'."
 223:       [log1 + x for log1,x in log.alongWith(can)]
 224:       
 225:     def logNews(i,log, news):
 226:       """Stores values from a list of cans, called 'news'
 227:          into a log."""
 228:       for can in news:
 229:         for x,log1 in zip(can.decs,log.decs):
 230:           log1 + x
 231:         for x,log1 in zip(can.objs,log.objs):
 232:           log1 + x
 233:         log.aggregate + i.aggregate(can,log)
 234:       return news
 235:         
 236:     def aFewBlanks(i):
 237:       """ Handles instantiation with constraints.
 238:           If can't  make  newinstance after some repeats, crash."""
 239:       patience = the.GADGETS.patience
 240:       while True:
 241:         yield i.blank()
 242:         patience -= 1
 243:         assert patience > 0, "constraints too hard to satisfy"
 244:   
 245:     def decs(i):
 246:       "return a new candidate, with guesses for decisions"
 247:       for can in i.aFewBlanks():
 248:         can.decs = [dec.maker() for dec in i.model.decs]
 249:         if i.model.ok(can):
 250:           return can
 251:     
 252:     def eval(i,can):
 253:       "expire the old aggregate. make the objective scores."
 254:       can.aggregate = None
 255:       can.objs = [obj.maker(can) for obj in i.model.objs]
 256:       return can
 257:   
 258:     def aggregate(i,can,logs):
 259:       "Return the aggregate. Side-effect: store it in the can"
 260:       if can.aggregate == None:
 261:          agg = n = 0
 262:          for obj,about,log in zip(can.objs,
 263:                                   i.model.objs,
 264:                                   logs.objs):
 265:            n   += 1
 266:            agg += about.fromHell(obj,log)
 267:          can.aggregate = agg ** 0.5 / n ** 0.5
 268:       return can.aggregate
 269:          
 270:     def mutate(i,can,logs,p):
 271:       "Return a new can with p% mutated"
 272:       for sn in i.aFewBlanks():
 273:         for n,(dec,about,log) in enumerate(zip(can.decs,
 274:                                              i.model.decs,
 275:                                              logs.decs)):
 276:           val = can.decs[n]
 277:           if p > r():
 278:             some = (log.hi - log.lo)*0.5
 279:             val  = val - some + 2*some*r()
 280:             val  = about.wrap(val)
 281:           sn.decs[n] = val
 282:         if i.model.ok(sn):
 283:           return sn
 284:         
 285:     def xPlusFyz(i,threeMore,cr,f):
 286:       "Crossovers some decisions, by a factor of 'f'"
 287:       def smear((x1, y1, z1, about)):
 288:         x1 = x1 if cr <= r() else x1 + f*(y1-z1)
 289:         return about.wrap(x1)
 290:       for sn in i.aFewBlanks():
 291:         x,y,z   = threeMore()
 292:         sn.decs = [smear(these)
 293:                    for these in zip(x.decs,
 294:                                     y.decs,
 295:                                     z.decs,
 296:                                     i.model.decs)]
 297:         if i.model.ok(sn):
 298:           return sn
 299:       
 300:     def news(i,n=None):
 301:       "Generating, say, 100 random instances."
 302:       return [i.eval( i.decs())
 303:               for _ in xrange(n or the.GADGETS.baseline)]
 304:   
 305:     def energy(i,can,logs):
 306:       "Returns an energy value to be minimized"
 307:       i.eval(can)
 308:       e = abs(1 - i.aggregate(can,logs))
 309:       if e < 0: e= 0
 310:       if e > 1: e= 1
 311:       return e
 312:     
 313:     def better1(i,now,last):
 314:       "Is one era better than another?"
 315:       better=worse=0
 316:       for now1,last1,about in zip(now.objs,
 317:                                   last.objs,
 318:                                   i.model.objs):
 319:         nowMed = median(now1.some())
 320:         lastMed= median(last1.some())
 321:         if about.better(nowMed, lastMed):
 322:           better += 1
 323:         elif nowMed != lastMed:
 324:           worse += 1
 325:       return better > 0 and worse < 1
 326:     
 327:     def fyi(i,x)   :
 328:       "Maybe, mention something"
 329:       the.GADGETS.verbose and say(x)
 330:       
 331:     def shout(i,x) :
 332:       "Add an emphasis to an output."
 333:       i.fyi("__" + x)
 334:       
 335:     def bye(i,info,first,now) :
 336:       """Optimizers return the distribution of values seen in
 337:          first and final era"""
 338:       i.fyi(info)
 339:       return first,now
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

<a href="gadgets.py#L621-L666"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 340:   @setting
 341:   def SA(): return o(
 342:       p=0.25,
 343:       cooling=1,
 344:       kmax=1000)
 345:     
 346:   def sa(m,baseline=None,also2=None):
 347:     def goodbye(x)  : return g.bye(x,first,now)
 348:     g = Gadgets(m)
 349:     def p(old,new,t): return ee**((old - new)/t)
 350:     k,eb,life = 0,1,the.GADGETS.lives
 351:     #===== setting up logs
 352:     also     = g.logs(also2) # log of all eras
 353:     first    = now  = g.logs(also)
 354:     g.logNews(first,baseline or g.news())
 355:     last, now  = now, g.logs(also)
 356:     #===== ok to go
 357:     s = g.decs()
 358:     e = g.energy(s,now)
 359:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 360:     while True:
 361:       info="."
 362:       k += 1
 363:       t  = (k/the.SA.kmax) ** (1/the.SA.cooling)
 364:       sn = g.mutate(s, also,the.SA.p)
 365:       en = g.energy(sn,also)
 366:       g.log1(sn,now)
 367:       if en < eb:
 368:         sb,eb = sn,en
 369:         g.shout("!")
 370:       if en < e:
 371:         s,e = sn,en
 372:         info = "+"
 373:       elif p(e,en,t) < r():
 374:         s,e = sn, en
 375:         info="?"
 376:       if k % the.GADGETS.era: 
 377:         g.fyi(info)
 378:       else:
 379:         life = life - 1
 380:         if g.better1(now, last)     : life = the.GADGETS.lives 
 381:         if life < 1                 : return goodbye("L")
 382:         if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 383:         if k > the.SA.kmax          : return goodbye("K")
 384:         g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 385:         last, now  = now, g.logs(also) 
```

### Differential Evolution

<a href="gadgets.py#L672-L715"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 386:   @setting
 387:   def DE(): return o(
 388:       cr = 0.4,
 389:       f  = 0.5,
 390:       npExpand = 10,
 391:       kmax=1000)
 392:     
 393:   def de(m,baseline=None,also2=None):
 394:     def goodbye(x)  : return g.bye(x,first,now)
 395:     g  = Gadgets(m)
 396:     np = len(g.model.decs) * the.DE.npExpand
 397:     k,eb,life = 0,1,the.GADGETS.lives
 398:     #===== setting up logs
 399:     also     = g.logs(also2) # also = log of all eras
 400:     first    = now  = g.logs(also)
 401:     frontier = g.logNews(first,baseline or g.news(np))
 402:     last, now  = now, g.logs(also)
 403:     #===== ok to go
 404:     sn = en = None
 405:     g.fyi("%4s [%2s] %3s "% (k,life,"     "))
 406:     while True:
 407:       for n,parent in enumerate(frontier):
 408:         info="."
 409:         k += 1
 410:         e  = g.aggregate(parent, also)
 411:         sn = g.xPlusFyz(lambda: another3(frontier,parent),
 412:                         the.DE.cr,
 413:                         the.DE.f)
 414:         en = g.energy(sn,also)
 415:         g.log1(sn,now)
 416:         if en < eb:
 417:           sb,eb = sn,en
 418:           g.shout("!")
 419:         if en < e:
 420:           frontier[n] = sn # goodbye parent
 421:           info = "+"
 422:         g.fyi(info)
 423:       life = life - 1
 424:       if g.better1(now, last)     : life = the.GADGETS.lives 
 425:       if life < 1                 : return goodbye("L")
 426:       if eb < the.GADGETS.epsilon : return goodbye("E %.5f" %eb)
 427:       if k > the.DE.kmax          : return goodbye("K")
 428:       g.fyi("\n%4s [%2s] %.3f %s" % (k,life,eb,info))
 429:       last, now  = now, g.logs(also) 
```

DE trick for finding three unique things in a list that are not `avoid`.

<a href="gadgets.py#L721-L733"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 430:   def another3(lst, avoid=None):
 431:     def another1():
 432:       x = avoid
 433:       while id(x) in seen: 
 434:         x = lst[  int(random.uniform(0,len(lst))) ]
 435:       seen.append( id(x) )
 436:       return x
 437:     # -----------------------
 438:     assert len(lst) > 4
 439:     avoid = avoid or lst[0]
 440:     seen  = [ id(avoid) ]
 441:     return another1(), another1(), another1()
 442:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

