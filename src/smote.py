from __future__ import print_function, division
from ok import *
import random,re,sys
sys.dont_write_bytecode = True
from walkcsv import *

"""


# Smote

Read data, divide into klasses.

Keep at most N examples per klass (e.g. N=100).

If less than N examples per class, use synthetic oversamples:

- While less than N
   - Pick anything
   - Find nearest neighbor of same class
   - Create a new thing at some random distance between anything and neighbor

## Support code

"""
r     = random.random
rseed = random.seed
gt    = lambda x,y: x > y
lt    = lambda x,y: x < y

class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)

class Some:
  "Keep some things."
  def __init__(i, keep=8): # note, usually 256 or 128 or 64 (if brave)
    i.n, i.any, i.keep, i.ordered = 0,[],keep, False
  def __iadd__(i,x):
    i.ordered = False
    i.n += 1
    now = len(i.any)
    if now < i.keep:    # not full yet, so just keep it   
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x # zap some older value
    #else: forget x
    return i
  def sorted(i):
    i.any = i.any if i.ordered else sorted(i.any)
    i.ordered = True
    return i.any
  def lo(i): return i.sorted()[0]
  def hi(i): return i.sorted()[-1]
  def norm(i,x):
    lo,hi = i.lo(), i.hi()
    if x < lo: return 0
    if x > hi: return 1
    return (x - lo)/ (hi - lo + 1e-32)

"""

## Table

"""

class Table:
  " Tables keep `Some` values for each column in a string."
  def __init__(i,header,what="_all_",keep=100,rows=[]):
    i.header= header
    i.what  = what
    i.dep   = o(less=[], more=[], klass=None)
    i.indep = o(nums=[], syms=[])
    i.nums, i.syms, i.all = [],[],[]
    i.rows  = Some(keep=keep)
    for pos,name in enumerate(header):
      i.col(pos,name)
    map(i.__iadd__, rows)
    i.there = There(i)
  def clone(i,what=None,keep=None,rows=[]):
    return Table(i.header,
                 what= what or i.what,
                 keep= keep or i.rows.keep,
                 rows= rows)
  def __iadd__(i,cells):
    i.rows += [cells]
    for col in i.all:
      col += cells[col.pos]
    return i
  def klassp(i,x) : return "=" in x
  def lessp( i,x) : return "<" in x
  def morep( i,x) : return ">" in x
  def nump(  i,x) : return "$" in x
  def col(i,pos,name):
    z      = Some()
    z.pos  = pos
    z.name = name
    also   = i.nums 
    if   i.morep(name) : i.dep.more += [z]
    elif i.lessp(name) : i.dep.less += [z]
    elif i.nump(name)  : i.indep.nums += [z]
    else:
      also = i.syms
      if i.klassp(name): i.dep.klass = z
      else             : i.indep.syms += [z]
    i.all += [z]
    also  += [z]
  
class There:
  def __init__(i,t):
    i.t, i.dists = t,{}
  def dist(i,j,k):
    jid, kid = id(j),id(k)
    if jid == kid : return 0
    if jid > kid  : return i.dist(i.t,k,j)
    key = (jid,kid)
    if not key in i.dists :
      i.dists[key] = dist(i.t,j,k)
    return i.dists[key]
  def furthest(i,r1,lst,best=-1,better=gt):
    out = r1
    for r2 in lst:
      tmp = dist(i.t,r1,r2)
      if tmp and better(tmp,best):
        out,best = r2,tmp
    return out
  def closest(i,r1,lst):
    return i.furthest(i,r1,lst,best=1e32,better=lt)
  def nn(i,lst):
    all,nn,rnn = [],{}, {}
    for n1,r1 in enumerate(lst):
      all += [(n1,r1)]
      r2   = i.closest(r1,lst)
      nn[ n1] = r2
      rnn[n2] = rnn.get(n2,[]) + [n1]   
    return nn,rnn
  def decrowd(i,lst,min=2):
    "zap nearest neighbors"
    _,rnn = i.nn(i,lst)
    rnn = sorted([z for z in rnn.items()],
                 key = lambda pair: len(pair[1]),
                 reverse=True)
    out, dead = [],{}
    for n,nears in rnn:
      if len(nears) < min: break
      if not n in dead:
        out += [lst[n]]
        for z in nears:
          dead[z] = True
    return out      
    
def dist(t,j,k):
  "Does the calcs"
  def colxy(cols,xs,ys):
    for col in cols:
      x = xs[col.pos]
      y = ys[col.pos]
      if x == "?" and y=="?": continue
      yield col,x,y
  def far(col,x,y):
    y = col.norm(y)
    x = 0 if y > 0.5 else 1
    return x,y
  #---------
  n=all=0
  for col in colsxy(t.indep.syms,j,k):
    if x== "?" or y == "?":
      n   += 1
      all += 1
    else:
      inc = 0 if x == y else 1
      n   += 1
      all += inc
  for col,x,y in colxy(t.indep.nums,j,k):
    if   x == "?" : x,y = far(col,x,y)
    elif y == "?" : y,x = far(col,y,x)
    else          : x,y = col.norm(x), col.norm(y)
    n   += 1
    all += (x-y)**2
  return all**0.5 / n**0.5   

def table(src):
  for cells in values(src):
    if t:
      t += cells
    else:
     t = Table(cells)
  return t
"""

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

"""
class Default(dict):
  def __init__(i, default): i.default = default
  def __getitem__(i, key):
    if key in i: return i.get(key)
    return i.setdefault(key, i.default())

