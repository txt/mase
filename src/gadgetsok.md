[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Test suite for a generic optimizer

<a href="gadgetsok.py#L10-L86"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from ok import *
   2:   from gadgets import *
   3:   
   4:   @ok
   5:   def _seed():
   6:     seed(1)
   7:     assert 0.134364244111 < r() < 0.134364244113 
   8:   
   9:   @ok
  10:   def _log():
  11:     with study("log",
  12:                use(SOMES,size=10)):
  13:       log = Log()
  14:       [log + y for y in
  15:        shuffle([x for x in xrange(20)])]
  16:       assert log.lo==0
  17:       assert log.hi==19
  18:       assert log.some() == [9, 11, 13, 15, 6,
  19:                             19, 12, 14, 16, 1]
  20:     # after the study, all the defaults are
  21:     # back to zero
  22:     assert the.SOMES.size == 256
  23:   
  24:   @ok
  25:   def _fill():
  26:     b4 = Candidate([1,2],[2,4])
  27:     assert str(fill(b4)) ==  \
  28:            "o{'aggregate': None, "  + \
  29:            "'objs': [None, None], " + \
  30:            "'decs': [None, None]}"
  31:   
  32:   @ok
  33:   def _want():
  34:     with study("log",
  35:                use(SOMES,size=10)):
  36:       for klass in [Less,More]:
  37:         w = klass("fred",lo=0,hi=10)
  38:         guess = [w.guess() for _ in xrange(20)]
  39:         log = Log(guess)
  40:         assert w.restrain(20) == 10
  41:         assert w.wrap(15) == 5
  42:         assert not w.ok(12)
  43:         assert w.ok(8)
  44:         show(sorted(log.some()))
  45:         show(map(lambda n: w.fromHell(n,log),
  46:                  sorted(log.some())))
  47:   
  48:   @ok
  49:   def _gadgets1(f=Schaffer):
  50:     with study(f.__name__,
  51:                use(MISC,
  52:                    tiles=[0.05,0.1,0.2,0.4,0.8])):
  53:       g=Gadgets(f())
  54:       g.baseline()
  55:       print("aggregates:",
  56:             g.log.aggregate.tiles())
  57:       for whats in ['decs', 'objs']:
  58:         print("")
  59:         for n,what in enumerate(g.log[whats]):
  60:           print(whats, n,what.tiles())
  61:   
  62:   @ok
  63:   def _gadgets2(): _gadgets1(Fonseca)
  64:   
  65:   @ok
  66:   def _gadgets3(): _gadgets1(Kursawe)
  67:   
  68:   @ok
  69:   def _mutate():
  70:     for m in [0.3,0.7]:
  71:       with study("mutate",
  72:                  use(GADGETS,mutate=m)):
  73:         g=Gadgets(Kursawe())
  74:         one = g.decs()
  75:         two = g.mutate(one)
  76:         print(m, r5(one.decs))
  77:         print(m, r5(two.decs))
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

