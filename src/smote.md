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

   1:   
   2:   class Table:
   3:     " Tables keep `Some` values for each column in a string."
   4:     def __init__(i,header,what="_all_",keep=100,rows=[]):
   5:       i.header= header
   6:       i.what  = what
   7:       i.dep   = o(less=[], more=[], klass=None)
   8:       i.indep = o(nums=[], syms=[])
   9:       i.nums, i.syms, i.all = [],[],[]
  10:       i.rows  = Some(keep=keep)
  11:       for pos,name in enumerate(header):
  12:         i.col(pos,name)
  13:       map(i.__iadd__, rows)
  14:       i.there = There(i)
  15:     def clone(i,what=None,keep=None,rows=[]):
  16:       return Table(i.header,
  17:                    what= what or i.what,
  18:                    keep= keep or i.rows.keep,
  19:                    rows= rows)
  20:     def __iadd__(i,cells):
  21:       i.rows += [cells]
  22:       for col in i.all:
  23:         col += cells[col.pos]
  24:       return i
  25:     def klassp(i,x) : return "=" in x
  26:     def lessp( i,x) : return "<" in x
  27:     def morep( i,x) : return ">" in x
  28:     def nump(  i,x) : return "$" in x
  29:     def col(i,pos,name):
  30:       z      = Some()
  31:       z.pos  = pos
  32:       z.name = name
  33:       also   = i.nums 
  34:       if   i.morep(name) : i.dep.more += [z]
  35:       elif i.lessp(name) : i.dep.less += [z]
  36:       elif i.nump(name)  : i.indep.nums += [z]
  37:       else:
  38:         also = i.syms
  39:         if i.klassp(name): i.dep.klass = z
  40:         else             : i.indep.syms += [z]
  41:       i.all += [z]
  42:       also  += [z]
  43:     
  44:   class There:
  45:     def __init__(i,t):
  46:       i.t, i.dists = t,{}
  47:     def dist(i,j,k):
  48:       jid, kid = id(j),id(k)
  49:       if jid == kid : return 0
  50:       if jid > kid  : return i.dist(i.t,k,j)
  51:       key = (jid,kid)
  52:       if not key in i.dists :
  53:         i.dists[key] = dist(i.t,j,k)
  54:       return i.dists[key]
  55:     def furthest(i,r1,lst,best=-1,better=gt):
  56:       out = r1
  57:       for r2 in lst:
  58:         tmp = dist(i.t,r1,r2)
  59:         if tmp and better(tmp,best):
  60:           out,best = r2,tmp
  61:       return out
  62:     def closest(i,r1,lst):
  63:       return i.furthest(i,r1,lst,best=1e32,better=lt)
  64:     def nn(i,lst):
  65:       all,nn,rnn = [],{}, {}
  66:       for n1,r1 in enumerate(lst):
  67:         all += [(n1,r1)]
  68:         r2   = i.closest(r1,lst)
  69:         nn[ n1] = r2
  70:         rnn[n2] = rnn.get(n2,[]) + [n1]   
  71:       return nn,rnn
  72:     def decrowd(i,lst,min=2):
  73:       "zap nearest neighbors"
  74:       _,rnn = i.nn(i,lst)
  75:       rnn = sorted([z for z in rnn.items()],
  76:                    key = lambda pair: len(pair[1]),
  77:                    reverse=True)
  78:       out, dead = [],{}
  79:       for n,nears in rnn:
  80:         if len(nears) < min: break
  81:         if not n in dead:
  82:           out += [lst[n]]
  83:           for z in nears:
  84:             dead[z] = True
  85:       return out      
  86:       
  87:   def dist(t,j,k):
  88:     "Does the calcs"
  89:     def colxy(cols,xs,ys):
  90:       for col in cols:
  91:         x = xs[col.pos]
  92:         y = ys[col.pos]
  93:         if x == "?" and y=="?": continue
  94:         yield col,x,y
  95:     def far(col,x,y):
  96:       y = col.norm(y)
  97:       x = 0 if y > 0.5 else 1
  98:       return x,y
  99:     #---------
 100:     n=all=0
 101:     for col in colsxy(t.indep.syms,j,k):
 102:       if x== "?" or y == "?":
 103:         n   += 1
 104:         all += 1
 105:       else:
 106:         inc = 0 if x == y else 1
 107:         n   += 1
 108:         all += inc
 109:     for col,x,y in colxy(t.indep.nums,j,k):
 110:       if   x == "?" : x,y = far(col,x,y)
 111:       elif y == "?" : y,x = far(col,y,x)
 112:       else          : x,y = col.norm(x), col.norm(y)
 113:       n   += 1
 114:       all += (x-y)**2
 115:     return all**0.5 / n**0.5   
 116:   
 117:   def table(src):
 118:     for cells in values(src):
 119:       if t:
 120:         t += cells
 121:       else:
 122:        t = Table(cells)
 123:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="smote.py#L202-L207"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Default(dict):
   2:     def __init__(i, default): i.default = default
   3:     def __getitem__(i, key):
   4:       if key in i: return i.get(key)
   5:       return i.setdefault(key, i.default())
   6:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

