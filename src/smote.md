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

<a href="smote.py#L55-L106"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   r     = random.random
   2:   rseed = random.seed
   3:   gt    = lambda x,y: x > y
   4:   lt    = lambda x,y: x < y
   5:   
   6:   
   7:   class Some:
   8:     "Keep some things."
   9:     def __init__(i, keep=None): # note, usually 256 or 128 or 64 (if brave)
  10:       i.keep = keep or the.COL.cache
  11:       i.n, i.any  = 0,[]
  12:     def add(i,x):
  13:       i.n += 1
  14:       now = len(i.any)
  15:       if now < i.keep:       
  16:         i.any += [x]
  17:       elif r() <= now/i.n:
  18:         i.any[ int(r() * now) ]= x 
  19:   
  20:   class Log:
  21:     def __init__(i,inits=[]):
  22:       i.reset()
  23:       i.n = 0 
  24:       i.cache=Some()
  25:       map(i.add,inits)
  26:     def add(i,x):
  27:       if x != the.COL.missing:
  28:         i.add1(x)
  29:         i.n += 1
  30:         i.cache.add(x)
  31:   
  32:   class Num(Log):
  33:     def reset(i):
  34:       i.hi = i.lo = None
  35:       i.mu = i.sd = i.m2 = 0  
  36:     def add1(i,z):
  37:       i.lo  = min(z,i.lo)
  38:       i.hi  = max(z,i.hi)
  39:       delta = z - i.mu;
  40:       i.mu += delta/i.n
  41:       i.m2 += delta*(z - i.mu)
  42:       if i.n > 1:
  43:         i.sd = (i.m2/(i.n - 1))**0.5
  44:   
  45:   class Sym(Log):
  46:     def reset(i):
  47:       i.most, i.mode, i.all = 1,0,None,{}
  48:     def add1(i,z):
  49:       tmp = i.all[z] = i.all.get(z,0) + 1
  50:       if tmp > i.most:
  51:         i.most,i.mode = tmp,z
  52:       
```

## Table

<a href="smote.py#L112-L234"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  53:   
  54:   class Table:
  55:     " Tables keep `Some` values for each column in a string."
  56:     def __init__(i,header,what="_all_",keep=100,rows=[]):
  57:       i.header= header
  58:       i.what  = what
  59:       i.dep   = o(less=[], more=[], klass=None)
  60:       i.indep = o(nums=[], syms=[])
  61:       i.nums, i.syms, i.all = [],[],[]
  62:       i.rows  = Some(keep=keep)
  63:       for pos,name in enumerate(header):
  64:         i.col(pos,name)
  65:       map(i.__iadd__, rows)
  66:       i.there = There(i)
  67:     def clone(i,what=None,keep=None,rows=[]):
  68:       return Table(i.header,
  69:                    what= what or i.what,
  70:                    keep= keep or i.rows.keep,
  71:                    rows= rows)
  72:     def __iadd__(i,cells):
  73:       i.rows += [cells]
  74:       for col in i.all:
  75:         col += cells[col.pos]
  76:       return i
  77:     def klassp(i,x) : return "=" in x
  78:     def lessp( i,x) : return "<" in x
  79:     def morep( i,x) : return ">" in x
  80:     def nump(  i,x) : return "$" in x
  81:     def col(i,pos,name):
  82:       z      = Some()
  83:       z.pos  = pos
  84:       z.name = name
  85:       also   = i.nums 
  86:       if   i.morep(name) : i.dep.more += [z]
  87:       elif i.lessp(name) : i.dep.less += [z]
  88:       elif i.nump(name)  : i.indep.nums += [z]
  89:       else:
  90:         also = i.syms
  91:         if i.klassp(name): i.dep.klass = z
  92:         else             : i.indep.syms += [z]
  93:       i.all += [z]
  94:       also  += [z]
  95:     
  96:   class There:
  97:     def __init__(i,t):
  98:       i.t, i.dists = t,{}
  99:     def dist(i,j,k):
 100:       jid, kid = id(j),id(k)
 101:       if jid == kid : return 0
 102:       if jid > kid  : return i.dist(i.t,k,j)
 103:       key = (jid,kid)
 104:       if not key in i.dists :
 105:         i.dists[key] = dist(i.t,j,k)
 106:       return i.dists[key]
 107:     def furthest(i,r1,lst,best=-1,better=gt):
 108:       out = r1
 109:       for r2 in lst:
 110:         tmp = dist(i.t,r1,r2)
 111:         if tmp and better(tmp,best):
 112:           out,best = r2,tmp
 113:       return out
 114:     def closest(i,r1,lst):
 115:       return i.furthest(i,r1,lst,best=1e32,better=lt)
 116:     def nn(i,lst):
 117:       all,nn,rnn = [],{}, {}
 118:       for n1,r1 in enumerate(lst):
 119:         all += [(n1,r1)]
 120:         r2   = i.closest(r1,lst)
 121:         nn[ n1] = r2
 122:         rnn[n2] = rnn.get(n2,[]) + [n1]   
 123:       return nn,rnn
 124:     def decrowd(i,lst,min=2):
 125:       "zap nearest neighbors"
 126:       _,rnn = i.nn(i,lst)
 127:       rnn = sorted([z for z in rnn.items()],
 128:                    key = lambda pair: len(pair[1]),
 129:                    reverse=True)
 130:       out, dead = [],{}
 131:       for n,nears in rnn:
 132:         if len(nears) < min: break
 133:         if not n in dead:
 134:           out += [lst[n]]
 135:           for z in nears:
 136:             dead[z] = True
 137:       return out      
 138:       
 139:   def dist(t,j,k):
 140:     "Does the calcs"
 141:     def colxy(cols,xs,ys):
 142:       for col in cols:
 143:         x = xs[col.pos]
 144:         y = ys[col.pos]
 145:         if x == "?" and y=="?": continue
 146:         yield col,x,y
 147:     def far(col,x,y):
 148:       y = col.norm(y)
 149:       x = 0 if y > 0.5 else 1
 150:       return x,y
 151:     #---------
 152:     n=all=0
 153:     for col in colsxy(t.indep.syms,j,k):
 154:       if x== "?" or y == "?":
 155:         n   += 1
 156:         all += 1
 157:       else:
 158:         inc = 0 if x == y else 1
 159:         n   += 1
 160:         all += inc
 161:     for col,x,y in colxy(t.indep.nums,j,k):
 162:       if   x == "?" : x,y = far(col,x,y)
 163:       elif y == "?" : y,x = far(col,y,x)
 164:       else          : x,y = col.norm(x), col.norm(y)
 165:       n   += 1
 166:       all += (x-y)**2
 167:     return all**0.5 / n**0.5   
 168:   
 169:   def table(src):
 170:     for cells in values(src):
 171:       if t:
 172:         t += cells
 173:       else:
 174:        t = Table(cells)
 175:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="smote.py#L244-L249"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 176:   class Default(dict):
 177:     def __init__(i, default): i.default = default
 178:     def __getitem__(i, key):
 179:       if key in i: return i.get(key)
 180:       return i.setdefault(key, i.default())
 181:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

