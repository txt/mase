[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


 
# Compartmental Modeling


## Diapers

 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 
C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers

<a href="stockflow.py#L28-L107"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class o:
   2:     """Emulate Javascript's uber simple objects.
   3:     Note my convention: I use "`i`" not "`this`."""
   4:     def has(i)             : return i.__dict__
   5:     def __init__(i,**d)    : i.has().update(d)
   6:     def __setitem__(i,k,v) : i.has()[k] = v
   7:     def __getitem__(i,k)   : return i.has()[k]
   8:     def __repr__(i)        : return 'o'+str(i.has())
   9:     def copy(i): 
  10:         j = o()
  11:         for k in i.has(): j[k] = i[k]
  12:         return j
  13:     def asList(i,keys=[]):
  14:       keys = keys or i.keys()
  15:       return [i[k] for k in keys]
  16:         
  17:   class Has:
  18:     def __init__(i,init,lo=0,hi=100):
  19:       i.init,i.lo,i.hi = init,lo,hi
  20:     def restrain(i,x):
  21:       return max(i.lo, 
  22:                  min(i.hi, x))
  23:     def rank(i):
  24:       if isa(i,Flow) : return 3
  25:       if isa(i,Stock): return 1
  26:       if isa(i,Aux)  : return 2
  27:     def __repr__(i):
  28:       return str(dict(what=i.__class__.__name__,
  29:                   name= i.name,init= i.init,
  30:                    lo  = i.lo,  hi  = i.hi))
  31:                    
  32:   
  33:   class Flow(Has) : pass
  34:   class Stock(Has): pass
  35:   class Aux(Has)  : pass
  36:   
  37:   F,S,A=Flow,Stock,Aux
  38:   
  39:   class Model:
  40:     def about(i):
  41:       tmp=i.have()
  42:       for k,v in tmp.has().items():
  43:         v.name = k
  44:       return tmp 
  45:     def run(i,dt=1,tmax=100): 
  46:       print(r())
  47:       t,u, keep  = 0, o(), []
  48:       about = i.about()
  49:       keys  = sorted(about.keys, 
  50:                      key=lambda z:z.rank())
  51:       print(keys)
  52:       for k,a in about.items(): 
  53:         u[k] = a.init
  54:       keep = [["t"] +  keys,
  55:               [0] + about.asList(u,keys)]
  56:       while t < tmax:
  57:         v = copy(u)
  58:         i.step(dt,t,u,v)
  59:         for k in about: 
  60:           v[k] = about[k].restrain(v[k])
  61:         keep += [[dt] + about.asList(u,keys)]
  62:         t += dt
  63:       return keep
  64:         
  65:   class Diapers(Model):
  66:     def have(i):
  67:       return o(C = S(20), D = S(0),
  68:                q = F(0),  r = F(8), s = F(0))
  69:     def step(i,dt,t,u,v):
  70:       def saturday(x): return int(x) % 7 == 6
  71:       v.C +=  dt*(u.q - u.r)
  72:       v.D +=  dt*(u.r - u.s)
  73:       v.q  =  70  if saturday(t) else 0 
  74:       v.s  =  u.D if saturday(t) else 0
  75:       if t == 27: # special case (the day i forget)
  76:         v.s = 0
  77:   
  78:   @ok
  79:   def _diapers1():
  80:     print(Diapers().about())
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

