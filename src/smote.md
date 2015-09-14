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

<a href="smote.py#L26-L64"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   r     = random.random
   2:   rseed = random.seed
   3:   gt    = lambda x,y: x > y
   4:   lt    = lambda x,y: x < y
   5:   
   6:   class o:
   7:     """Emulate Javascript's uber simple objects.
   8:     Note my convention: I use "`i`" not "`this`."""
   9:     def __init__(i,**d)    : i.__dict__.update(d)
  10:     def __setitem__(i,k,v) : i.__dict__[k] = v
  11:     def __getitem__(i,k)   : return i.__dict__[k]
  12:     def __repr__(i)        : return 'o'+str(i.__dict__)
  13:   
  14:   class Some:
  15:     "Keep some things."
  16:     def __init__(i, keep=8): # note, usually 256 or 128 or 64 (if brave)
  17:       i.n, i.any, i.keep, i.ordered = 0,[],keep, False
  18:     def __iadd__(i,x):
  19:       i.ordered = False
  20:       i.n += 1
  21:       now = len(i.any)
  22:       if now < i.keep:    # not full yet, so just keep it   
  23:         i.any += [x]
  24:       elif r() <= now/i.n:
  25:         i.any[ int(r() * now) ]= x # zap some older value
  26:       #else: forget x
  27:       return i
  28:     def sorted(i):
  29:       i.any = i.any if i.ordered else sorted(i.any)
  30:       i.ordered = True
  31:       return i.any
  32:     def lo(i): return i.sorted()[0]
  33:     def hi(i): return i.sorted()[-1]
  34:     def norm(i,x):
  35:       lo,hi = i.lo(), i.hi()
  36:       if x < lo: return 0
  37:       if x > hi: return 1
  38:       return (x - lo)/ (hi - lo + 1e-32)
  39:   
```

## Table

<a href="smote.py#L70-L192"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  40:   
  41:   class Table:
  42:     " Tables keep `Some` values for each column in a string."
  43:     def __init__(i,header,what="_all_",keep=100,rows=[]):
  44:       i.header= header
  45:       i.what  = what
  46:       i.dep   = o(less=[], more=[], klass=None)
  47:       i.indep = o(nums=[], syms=[])
  48:       i.nums, i.syms, i.all = [],[],[]
  49:       i.rows  = Some(keep=keep)
  50:       for pos,name in enumerate(header):
  51:         i.col(pos,name)
  52:       map(i.__iadd__, rows)
  53:       i.there = There(i)
  54:     def clone(i,what=None,keep=None,rows=[]):
  55:       return Table(i.header,
  56:                    what= what or i.what,
  57:                    keep= keep or i.rows.keep,
  58:                    rows= rows)
  59:     def __iadd__(i,cells):
  60:       i.rows += [cells]
  61:       for col in i.all:
  62:         col += cells[col.pos]
  63:       return i
  64:     def klassp(i,x) : return "=" in x
  65:     def lessp( i,x) : return "<" in x
  66:     def morep( i,x) : return ">" in x
  67:     def nump(  i,x) : return "$" in x
  68:     def col(i,pos,name):
  69:       z      = Some()
  70:       z.pos  = pos
  71:       z.name = name
  72:       also   = i.nums 
  73:       if   i.morep(name) : i.dep.more += [z]
  74:       elif i.lessp(name) : i.dep.less += [z]
  75:       elif i.nump(name)  : i.indep.nums += [z]
  76:       else:
  77:         also = i.syms
  78:         if i.klassp(name): i.dep.klass = z
  79:         else             : i.indep.syms += [z]
  80:       i.all += [z]
  81:       also  += [z]
  82:     
  83:   class There:
  84:     def __init__(i,t):
  85:       i.t, i.dists = t,{}
  86:     def dist(i,j,k):
  87:       jid, kid = id(j),id(k)
  88:       if jid == kid : return 0
  89:       if jid > kid  : return i.dist(i.t,k,j)
  90:       key = (jid,kid)
  91:       if not key in i.dists :
  92:         i.dists[key] = dist(i.t,j,k)
  93:       return i.dists[key]
  94:     def furthest(i,r1,lst,best=-1,better=gt):
  95:       out = r1
  96:       for r2 in lst:
  97:         tmp = dist(i.t,r1,r2)
  98:         if tmp and better(tmp,best):
  99:           out,best = r2,tmp
 100:       return out
 101:     def closest(i,r1,lst):
 102:       return i.furthest(i,r1,lst,best=1e32,better=lt)
 103:     def nn(i,lst):
 104:       all,nn,rnn = [],{}, {}
 105:       for n1,r1 in enumerate(lst):
 106:         all += [(n1,r1)]
 107:         r2   = i.closest(r1,lst)
 108:         nn[ n1] = r2
 109:         rnn[n2] = rnn.get(n2,[]) + [n1]   
 110:       return nn,rnn
 111:     def decrowd(i,lst,min=2):
 112:       "zap nearest neighbors"
 113:       _,rnn = i.nn(i,lst)
 114:       rnn = sorted([z for z in rnn.items()],
 115:                    key = lambda pair: len(pair[1]),
 116:                    reverse=True)
 117:       out, dead = [],{}
 118:       for n,nears in rnn:
 119:         if len(nears) < min: break
 120:         if not n in dead:
 121:           out += [lst[n]]
 122:           for z in nears:
 123:             dead[z] = True
 124:       return out      
 125:       
 126:   def dist(t,j,k):
 127:     "Does the calcs"
 128:     def colxy(cols,xs,ys):
 129:       for col in cols:
 130:         x = xs[col.pos]
 131:         y = ys[col.pos]
 132:         if x == "?" and y=="?": continue
 133:         yield col,x,y
 134:     def far(col,x,y):
 135:       y = col.norm(y)
 136:       x = 0 if y > 0.5 else 1
 137:       return x,y
 138:     #---------
 139:     n=all=0
 140:     for col in colsxy(t.indep.syms,j,k):
 141:       if x== "?" or y == "?":
 142:         n   += 1
 143:         all += 1
 144:       else:
 145:         inc = 0 if x == y else 1
 146:         n   += 1
 147:         all += inc
 148:     for col,x,y in colxy(t.indep.nums,j,k):
 149:       if   x == "?" : x,y = far(col,x,y)
 150:       elif y == "?" : y,x = far(col,y,x)
 151:       else          : x,y = col.norm(x), col.norm(y)
 152:       n   += 1
 153:       all += (x-y)**2
 154:     return all**0.5 / n**0.5   
 155:   
 156:   def table(src):
 157:     for cells in values(src):
 158:       if t:
 159:         t += cells
 160:       else:
 161:        t = Table(cells)
 162:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="smote.py#L202-L207"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 163:   class Default(dict):
 164:     def __init__(i, default): i.default = default
 165:     def __getitem__(i, key):
 166:       if key in i: return i.get(key)
 167:       return i.setdefault(key, i.default())
 168:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

