[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Test suite for some generic optimizer gadgets

<a href="gadgetsok.py#L57-L259"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
  35:   def _fill1():
  36:     b4 = Candidate([1,2],[2,4])
  37:     assert str(b4.clone()) ==  \
  38:       "Candidate{'objs': [None, None], " + \
  39:       "'aggregated': None, 'decs': [None, None]}"
  40:   
  41:   @ok
  42:   def _fill2():
  43:     b4 = Schaffer()
  44:     assert b4.clone().__class__ == Schaffer
  45:   
  46:   @ok
  47:   def _want():
  48:     with study("log",
  49:                use(SOMES,size=10)):
  50:       for klass in [Less,More]:
  51:         z = klass("fred",lo=0,hi=10)
  52:         guess = [z.guess() for _ in xrange(20)]
  53:         log = Log(guess)
  54:         assert z.restrain(20) == 10
  55:         assert z.wrap(15) == 5
  56:         assert not z.ok(12)
  57:         assert z.ok(8)
  58:         print("\n"+klass.__name__)
  59:         show(sorted(log.some()))
  60:         show(map(lambda n: z.fromHell(n,log),
  61:                  sorted(log.some())))
  62:   
  63:       
  64:   
  65:   
  66:   @ok
  67:   def _gadgets1(f=Schaffer):
  68:     with study(f.__name__,
  69:                use(MISC,
  70:                    tiles=[0.05,0.1,0.2,0.4,0.8])):
  71:       g=Gadgets(f())
  72:       log = g.logs()
  73:       g.logNews(log, g.news())
  74:       print("aggregates:",
  75:             log.aggregate.tiles())
  76:       for whats in ['decs', 'objs']:
  77:         print("")
  78:         for n,what in enumerate(log[whats]):
  79:           print(whats, n,what.tiles())
  80:   
  81:   @ok
  82:   def _gadgets2(): _gadgets1(Fonseca)
  83:   
  84:   @ok
  85:   def _gadgets3(): _gadgets1(Kursawe)
  86:   
  87:   @ok
  88:   def _gadgets4(): _gadgets1(ZDT1)
  89:   
  90:   @ok
  91:   def _mutate():
  92:     for m in [0.3,0.6]:
  93:       with study("mutate",
  94:                  use(GADGETS,mutate=m)):
  95:         g=Gadgets(Kursawe())
  96:         log =g.logs()
  97:         g.logNews(log,
  98:                   g.news(100))
  99:         one = g.decs()
 100:         two = g.mutate(one,log,the.GADGETS.mutate)
 101:         print(m, r5(one.decs))
 102:         print(m, r5(two.decs))
 103:   
 104:   
 105:               
 106:   @ok
 107:   def _opt(m=Schaffer,optimizer=sa):
 108:     def show(txt,what,all):
 109:       all = sorted(all)
 110:       lo, hi = all[0], all[-1]
 111:       print("##",txt,xtile(what,lo=lo,hi=hi,width=25,show=" %6.2f"),m.__class__.__name__)
 112:     with study(m.__name__,
 113:                use(GADGETS,
 114:                    verbose=True),
 115:                use(MISC,
 116:                    tiles=[0,   0.1,0.3 ,0.5,0.7,0.99],
 117:                    marks=["0" ,"1", "3","5","7","!"])):
 118:       m = m()
 119:       firsts,lasts=optimizer(m)
 120:       for first,last,name in zip(firsts.objs,
 121:                                  lasts.objs,
 122:                                  m.objs):
 123:         all = first.some() + last.some()
 124:         print("\n" + name.txt)
 125:         show("FIRST:",first.some(),all)
 126:         show("LAST :",last.some(), all)
 127:   
 128:   def _de(m=Schaffer):
 129:     _opt(m,de)
 130:   
 131:   
 132:   @ok
 133:   def _opt0(): _opt()
 134:   @ok
 135:   def _de0(): _de(Schaffer)
 136:   
 137:   @ok
 138:   def _opt1(): _opt(Fonseca,sa)
 139:   @ok
 140:   def _de0(): _de(Fonseca)
 141:   
 142:   @ok
 143:   def _opt2(): _opt(Kursawe)
 144:   @ok
 145:   def _de0(): _de(Kursawe)
 146:   
 147:   @ok
 148:   def _opt3(): _opt(ZDT1)
 149:   @ok
 150:   def _de0(): _de(ZDT1)
 151:   
 152:   @ok
 153:   def _opt4(): _opt(Viennet4)
 154:   @ok
 155:   def _de0(): _de(Viennet4)
 156:   
 157:   @ok
 158:   def _threeOthers():
 159:     seed(1)
 160:     lst = list('abcdefg')
 161:     print(another3(lst,'a'))
 162:   
 163:   
 164:   def opts(optimizers,models,n=20):
 165:     def report(lst,what):
 166:        print("",', '.join(map(str,r2(lst))),
 167:              model.__name__,
 168:              what,
 169:              sep=", ")
 170:     tiles=[0.25,0.50,0.75]
 171:     print("#"," "*(n-2),r5(tiles))
 172:     for model in models:
 173:       shown=False
 174:       for opt in optimizers:
 175:         seed()
 176:         firsts = Log()
 177:         lasts  = Log()
 178:         for i in xrange(n):
 179:           say(".")
 180:           m = model()
 181:           g = Gadgets(m)
 182:           baseline = g.news(the.GADGETS.baseline)
 183:           with study(opt.__name__,use(GADGETS,
 184:                                       verbose=False),
 185:                      verbose=False):
 186:             first,last = opt(m,baseline)
 187:             firsts.adds( first.aggregate.some() )
 188:             lasts.adds(  last.aggregate.some() )
 189:         if shown:
 190:           report(firsts.stats(tiles),"baseline")
 191:           say("."*n)
 192:           shown = True
 193:         report(lasts.stats(tiles),opt.__name__)
 194:       print("")
 195:   
 196:               
 197:   @ok
 198:   def _opts():
 199:     opts([sa,de],[Schaffer,Fonseca,Kursawe,ZDT1,Viennet4])
 200:   
 201:   
 202:   
 203:   unittest.enough()    
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

