[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Test suite for some generic optimizer gadgets

<a href="gadgetsok.py#L55-L177"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
  10:   def _xtileX() :
  11:     import random
  12:     seed(1)
  13:     nums1 = [r()**2 for _ in range(100)]
  14:     nums2 = [r()**0.5 for _ in range(100)]
  15:     for nums in [nums1,nums2]:
  16:       print(xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f"))
  17:   
  18:     
  19:   @ok
  20:   def _log():
  21:     with study("log",
  22:                use(SOMES,size=10)):
  23:       log = Log()
  24:       [log + y for y in
  25:        shuffle([x for x in xrange(20)])]
  26:       assert log.lo==0
  27:       assert log.hi==19
  28:       assert log.some() == [9, 11, 13, 15, 6,
  29:                             19, 12, 14, 16, 1]
  30:     # after the study, all the defaults are
  31:     # back to zero
  32:     assert the.SOMES.size == 256
  33:   
  34:   @ok
  35:   def _fill():
  36:     b4 = Candidate([1,2],[2,4])
  37:     assert str(canCopy(b4)) ==  \
  38:            "o{'aggregate': None, "  + \
  39:            "'objs': [None, None], " + \
  40:            "'decs': [None, None]}"
  41:   
  42:   @ok
  43:   def _want():
  44:     with study("log",
  45:                use(SOMES,size=10)):
  46:       for klass in [Less,More]:
  47:         w = klass("fred",lo=0,hi=10)
  48:         guess = [w.guess() for _ in xrange(20)]
  49:         log = Log(guess)
  50:         assert w.restrain(20) == 10
  51:         assert w.wrap(15) == 5
  52:         assert not w.ok(12)
  53:         assert w.ok(8)
  54:         show(sorted(log.some()))
  55:         show(map(lambda n: w.fromHell(n,log),
  56:                  sorted(log.some())))
  57:   
  58:   @ok
  59:   def _gadgets1(f=Schaffer):
  60:     with study(f.__name__,
  61:                use(MISC,
  62:                    tiles=[0.05,0.1,0.2,0.4,0.8])):
  63:       g=Gadgets(f())
  64:       log = g.logs()
  65:       g.baseline(log)
  66:       print("aggregates:",
  67:             log.aggregate.tiles())
  68:       for whats in ['decs', 'objs']:
  69:         print("")
  70:         for n,what in enumerate(log[whats]):
  71:           print(whats, n,what.tiles())
  72:   
  73:   @ok
  74:   def _gadgets2(): _gadgets1(Fonseca)
  75:   
  76:   @ok
  77:   def _gadgets3(): _gadgets1(Kursawe)
  78:   
  79:   @ok
  80:   def _mutate():
  81:     for m in [0.3,0.7]:
  82:       with study("mutate",
  83:                  use(GADGETS,mutate=m)):
  84:         g=Gadgets(Kursawe())
  85:         one = g.decs()
  86:         two = g.mutate(one)
  87:         print(m, r5(one.decs))
  88:         print(m, r5(two.decs))
  89:   
  90:   @ok
  91:   def _sa1(m=Schaffer):
  92:     def show(txt,what,all):
  93:       all = sorted(all)
  94:       lo, hi = all[0], all[-1]
  95:       print(txt,xtile(what,lo=lo,hi=hi,width=25,show=" %3.2f"))
  96:     with study(m.__name__,
  97:                use(MISC,
  98:                    tiles=[0,   0.1,0.3 ,0.5,0.7,0.99],
  99:                    marks=["0" ,"1", "3","5","7","!"])):
 100:       m = m()
 101:       firsts,lasts=sa(m).run()
 102:       print("")
 103:       for first,last,name in zip(firsts.objs,
 104:                                  lasts.objs,
 105:                                  m.objs):
 106:         all = first.some() + last.some()
 107:         print("\n" + name.txt)
 108:         show("FIRST:",first.some(),all)
 109:         show("LAST :",last.some(), all)
 110:   
 111:   @ok
 112:   def _sa2(): _sa1(Fonseca)
 113:   
 114:   
 115:   @ok
 116:   def _sa3(): _sa1(Kursawe)
 117:   
 118:   
 119:   @ok
 120:   def _sa4(): _sa1(ZDT1)
 121:   
 122:   
 123:       
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

