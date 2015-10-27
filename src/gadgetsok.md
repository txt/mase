[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Test suite for some generic optimizer gadgets

<a href="gadgetsok.py#L57-L264"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from ok import *
   2:   from gadgets import *
   3:   
   4:   #@ok
   5:   def _seed():
   6:     seed(1)
   7:     assert 0.134364244111 < r() < 0.134364244113 
   8:   
   9:     
  10:   #@ok
  11:   def _xtileX() :
  12:     import random
  13:     seed(1)
  14:     nums1 = [r()**2 for _ in range(100)]
  15:     nums2 = [r()**0.5 for _ in range(100)]
  16:     for nums in [nums1,nums2]:
  17:       print(xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f"))
  18:   
  19:   
  20:   
  21:   
  22:   #@ok
  23:   def _log():
  24:     with study("log",
  25:                use(SOMES,size=10)):
  26:       log = Log()
  27:       [log + y for y in
  28:        shuffle([x for x in xrange(20)])]
  29:       assert log.lo==0
  30:       assert log.hi==19
  31:       print(sorted(log.some()))
  32:       print(sorted(log.some()))
  33:       assert sorted(log.some()) == [1, 6, 9, 11, 12,
  34:                                     13, 14, 15, 16, 19]
  35:       
  36:     # after the study, all the defaults are
  37:     # back to zero
  38:     assert the.SOMES.size == 256
  39:   
  40:   
  41:   #@ok
  42:   def _fill1():
  43:     b4 = Schaffer([1],[1,2])
  44:     assert str(b4.clone()) ==  \
  45:       "Schaffer{'objs': [None], " + \
  46:       "'aggregated': None, 'decs': [None, None]}"
  47:   
  48:   #@ok
  49:   def _fill2():
  50:     b4 = Schaffer()
  51:     assert b4.clone().__class__ == Schaffer
  52:   
  53:   #@ok
  54:   def _want():
  55:     with study("log",
  56:                use(SOMES,size=10)):
  57:       for klass in [Less,More]:
  58:         z = klass("fred",lo=0,hi=10)
  59:         guess = [z.guess() for _ in xrange(20)]
  60:         log = Log(guess)
  61:         assert z.restrain(20) == 10
  62:         assert z.wrap(15) == 5
  63:         assert not z.ok(12)
  64:         assert z.ok(8)
  65:         print("\n"+klass.__name__)
  66:         show(sorted(log.some()))
  67:         show(map(lambda n: z.fromHell(n,log),
  68:                  sorted(log.some())))
  69:     
  70:   #@ok
  71:   def _gadgets1(f=Schaffer):
  72:     with study(f.__name__,
  73:                use(MISC,
  74:                    tiles=[0.05,0.1,0.2,0.4,0.8])):
  75:       g=Gadgets(f())
  76:       log = g.logs()
  77:       g.logNews(log, g.news())
  78:       print("aggregates:",
  79:             log.aggregate.tiles())
  80:       for whats in ['decs', 'objs']:
  81:         print("")
  82:         for n,what in enumerate(log[whats]):
  83:           print(whats, n,what.tiles())
  84:   
  85:          
  86:   #@ok
  87:   def _gadgets2(): _gadgets1(Fonseca)
  88:   
  89:   #@ok
  90:   def _gadgets3(): _gadgets1(Kursawe)
  91:   
  92:   #@ok
  93:   def _gadgets4(): _gadgets1(ZDT1)
  94:   
  95:   #@ok
  96:   def _mutate():
  97:     for m in [0.3,0.6]:
  98:       with study("mutate",
  99:                  use(GADGETS,mutate=m)):
 100:         g=Gadgets(Kursawe())
 101:         log =g.logs()
 102:         g.logNews(log,
 103:                   g.news(100))
 104:         one = g.decs()
 105:         two = g.mutate(one,log,the.GADGETS.mutate)
 106:         print(m, r5(one.decs))
 107:         print(m, r5(two.decs))
 108:   
 109:   
 110:               
 111:   #@ok
 112:   def _opt(m=Schaffer,optimizer=sa):
 113:     def show(txt,what,all):
 114:       all = sorted(all)
 115:       lo, hi = all[0], all[-1]
 116:       print("##",txt,xtile(what,lo=lo,hi=hi,width=25,show=" %6.2f"),m.__class__.__name__)
 117:     with study(m.__name__,
 118:                use(GADGETS,
 119:                    verbose=True),
 120:                use(MISC,
 121:                    tiles=[0,   0.1,0.3 ,0.5,0.7,0.99],
 122:                    marks=["0" ,"1", "3","5","7","!"])):
 123:       m = m()
 124:       firsts,lasts=optimizer(m)
 125:       for first,last,name in zip(firsts.objs,
 126:                                  lasts.objs,
 127:                                  m.objs):
 128:         all = first.some() + last.some()
 129:         print("\n" + name.txt)
 130:         show("FIRST:",first.some(),all)
 131:         show("LAST :",last.some(), all)
 132:   
 133:   def _de(m=Schaffer):
 134:     _opt(m,de)
 135:   
 136:   
 137:   #@ok
 138:   def _opt0(): _opt()
 139:   @ok
 140:   def _de0(): _de(Schaffer)
 141:   
 142:   #@ok
 143:   def _opt1(): _opt(Fonseca,sa)
 144:   @ok
 145:   def _de0(): _de(Fonseca)
 146:   
 147:   #@ok
 148:   def _opt2(): _opt(Kursawe)
 149:   @ok
 150:   def _de0(): _de(Kursawe)
 151:   
 152:   #@ok
 153:   def _opt3(): _opt(ZDT1)
 154:   @ok
 155:   def _de0(): _de(ZDT1)
 156:   
 157:   #@ok
 158:   def _opt4(): _opt(Viennet4)
 159:   @ok
 160:   def _de0(): _de(Viennet4)
 161:   
 162:   #@ok
 163:   def _threeOthers():
 164:     seed(1)
 165:     lst = list('abcdefg')
 166:     print(another3(lst,'a'))
 167:   
 168:   
 169:   def opts(optimizers,models,n=20):
 170:     def report(lst,what):
 171:        print("",', '.join(map(str,r2(lst))),
 172:              model.__name__,
 173:              what,
 174:              sep=", ")
 175:     tiles=[0.25,0.50,0.75]
 176:     print("#"," "*(n-2),r5(tiles))
 177:     for model in models:
 178:       shown=False
 179:       for opt in optimizers:
 180:         seed()
 181:         firsts = Log()
 182:         lasts  = Log()
 183:         for i in xrange(n):
 184:           say(".")
 185:           m = model()
 186:           g = Gadgets(m)
 187:           baseline = g.news(the.GADGETS.baseline)
 188:           with study(opt.__name__,use(GADGETS,
 189:                                       verbose=False),
 190:                      verbose=False):
 191:             first,last = opt(m,baseline)
 192:             firsts.adds( first.aggregate.some() )
 193:             lasts.adds(  last.aggregate.some() )
 194:         if shown:
 195:           report(firsts.stats(tiles),"baseline")
 196:           say("."*n)
 197:           shown = True
 198:         report(lasts.stats(tiles),opt.__name__)
 199:       print("")
 200:   
 201:               
 202:   #@ok
 203:   def _opts():
 204:     opts([sa,de],[Schaffer,Fonseca,Kursawe,ZDT1,Viennet4])
 205:   
 206:   
 207:   
 208:   unittest.enough()    
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

