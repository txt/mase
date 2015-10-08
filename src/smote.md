[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 




# Smote

Read data, divide into klasses.

Keep at most N examples per klass (e.g. N=100).

If less than N examples per class, use synthetic oversamples:

- While less than N
   - Pick anything
   - Find nearest neighbor of same class
   - Create a new thing at some random distance between anything and neighbor

## Support code

<a href="smote.py#L37-L70"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   
   2:   class Log:
   3:     def __init__(i,inits=[]):
   4:       i.reset()
   5:       i.n = 0 
   6:       i.cache=Some()
   7:       map(i.add,inits)
   8:     def add(i,x):
   9:       if x != the.COL.missing:
  10:         i.add1(x)
  11:         i.n += 1
  12:         i.cache.add(x)
  13:   
  14:   class Num(Log):
  15:     def reset(i):
  16:       i.hi = i.lo = None
  17:       i.mu = i.sd = i.m2 = 0  
  18:     def add1(i,z):
  19:       i.lo  = min(z,i.lo)
  20:       i.hi  = max(z,i.hi)
  21:       delta = z - i.mu;
  22:       i.mu += delta/i.n
  23:       i.m2 += delta*(z - i.mu)
  24:       if i.n > 1:
  25:         i.sd = (i.m2/(i.n - 1))**0.5
  26:   
  27:   class Sym(Log):
  28:     def reset(i):
  29:       i.most, i.mode, i.all = 1,0,None,{}
  30:     def add1(i,z):
  31:       tmp = i.all[z] = i.all.get(z,0) + 1
  32:       if tmp > i.most:
  33:         i.most,i.mode = tmp,z
  34:       
```

## Table

<a href="smote.py#L76-L198"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  35:   
  36:   class Table:
  37:     " Tables keep `Some` values for each column in a string."
  38:     def __init__(i,header,what="_all_",keep=100,rows=[]):
  39:       i.header= header
  40:       i.what  = what
  41:       i.dep   = o(less=[], more=[], klass=None)
  42:       i.indep = o(nums=[], syms=[])
  43:       i.nums, i.syms, i.all = [],[],[]
  44:       i.rows  = Some(keep=keep)
  45:       for pos,name in enumerate(header):
  46:         i.col(pos,name)
  47:       map(i.__iadd__, rows)
  48:       i.there = There(i)
  49:     def clone(i,what=None,keep=None,rows=[]):
  50:       return Table(i.header,
  51:                    what= what or i.what,
  52:                    keep= keep or i.rows.keep,
  53:                    rows= rows)
  54:     def __iadd__(i,cells):
  55:       i.rows += [cells]
  56:       for col in i.all:
  57:         col += cells[col.pos]
  58:       return i
  59:     def klassp(i,x) : return "=" in x
  60:     def lessp( i,x) : return "<" in x
  61:     def morep( i,x) : return ">" in x
  62:     def nump(  i,x) : return "$" in x
  63:     def col(i,pos,name):
  64:       z      = Some()
  65:       z.pos  = pos
  66:       z.name = name
  67:       also   = i.nums 
  68:       if   i.morep(name) : i.dep.more += [z]
  69:       elif i.lessp(name) : i.dep.less += [z]
  70:       elif i.nump(name)  : i.indep.nums += [z]
  71:       else:
  72:         also = i.syms
  73:         if i.klassp(name): i.dep.klass = z
  74:         else             : i.indep.syms += [z]
  75:       i.all += [z]
  76:       also  += [z]
  77:     
  78:   class There:
  79:     def __init__(i,t):
  80:       i.t, i.dists = t,{}
  81:     def dist(i,j,k):
  82:       jid, kid = id(j),id(k)
  83:       if jid == kid : return 0
  84:       if jid > kid  : return i.dist(i.t,k,j)
  85:       key = (jid,kid)
  86:       if not key in i.dists :
  87:         i.dists[key] = dist(i.t,j,k)
  88:       return i.dists[key]
  89:     def furthest(i,r1,lst,best=-1,better=gt):
  90:       out = r1
  91:       for r2 in lst:
  92:         tmp = dist(i.t,r1,r2)
  93:         if tmp and better(tmp,best):
  94:           out,best = r2,tmp
  95:       return out
  96:     def closest(i,r1,lst):
  97:       return i.furthest(i,r1,lst,best=1e32,better=lt)
  98:     def nn(i,lst):
  99:       all,nn,rnn = [],{}, {}
 100:       for n1,r1 in enumerate(lst):
 101:         all += [(n1,r1)]
 102:         r2   = i.closest(r1,lst)
 103:         nn[ n1] = r2
 104:         rnn[n2] = rnn.get(n2,[]) + [n1]   
 105:       return nn,rnn
 106:     def decrowd(i,lst,min=2):
 107:       "zap nearest neighbors"
 108:       _,rnn = i.nn(i,lst)
 109:       rnn = sorted([z for z in rnn.items()],
 110:                    key = lambda pair: len(pair[1]),
 111:                    reverse=True)
 112:       out, dead = [],{}
 113:       for n,nears in rnn:
 114:         if len(nears) < min: break
 115:         if not n in dead:
 116:           out += [lst[n]]
 117:           for z in nears:
 118:             dead[z] = True
 119:       return out      
 120:       
 121:   def dist(t,j,k):
 122:     "Does the calcs"
 123:     def colxy(cols,xs,ys):
 124:       for col in cols:
 125:         x = xs[col.pos]
 126:         y = ys[col.pos]
 127:         if x == "?" and y=="?": continue
 128:         yield col,x,y
 129:     def far(col,x,y):
 130:       y = col.norm(y)
 131:       x = 0 if y > 0.5 else 1
 132:       return x,y
 133:     #---------
 134:     n=all=0
 135:     for col in colsxy(t.indep.syms,j,k):
 136:       if x== "?" or y == "?":
 137:         n   += 1
 138:         all += 1
 139:       else:
 140:         inc = 0 if x == y else 1
 141:         n   += 1
 142:         all += inc
 143:     for col,x,y in colxy(t.indep.nums,j,k):
 144:       if   x == "?" : x,y = far(col,x,y)
 145:       elif y == "?" : y,x = far(col,y,x)
 146:       else          : x,y = col.norm(x), col.norm(y)
 147:       n   += 1
 148:       all += (x-y)**2
 149:     return all**0.5 / n**0.5   
 150:   
 151:   def table(src):
 152:     for cells in values(src):
 153:       if t:
 154:         t += cells
 155:       else:
 156:        t = Table(cells)
 157:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="smote.py#L208-L213"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 158:   class Default(dict):
 159:     def __init__(i, default): i.default = default
 160:     def __getitem__(i, key):
 161:       if key in i: return i.get(key)
 162:       return i.setdefault(key, i.default())
 163:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

