from __future__ import print_function, division

from lib import *

@setting
def COL(): return o(
    cache = 256,
    dull  = [0.147, # small
             0.33,  # medium
             0.474  # large
            ][0]
    )

class Sym:
  def __init__(i,inits=[]):
    i.most,i.mode, i.counts = 0,None,{}
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    n = i.counts[x] = i.counts.get(x,0) + 1
    if n > i.most:
      i.most,i.mode = n,x
    return i
  def norm(i,x): return x
  
class Num:
  def __init__(i, inits=[],lo=10**32, hi=-10**32):
    i.lo, i.hi, i._cache  = lo,hi, Cache()
    i.ordered = False
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    i.ordered = False
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
    i._cache += x
    return x
  def all(i):
    if not i.ordered:
      i._cache.all = sorted(i._cache.all)
      i.ordered = True
    return i._cache.all
  def norm(i,x):
    return (x - i.lo) / (i.hi - i.lo + 0.00001)
  def trim(i,x):
    return max(i.lo, min(x, i.hi))
  def fromHell(i,x,norm, want):
    if want: hell =  0 if norm else i.lo
    else:    hell =  1 if norm else i.hi
    if norm:
      x = i.norm(x) 
    return (x-hell)**2
  def wrap(i,x):
    gap = i.hi - i.lo
    if x > i.hi:
      return i.lo + ((i.hi - x) % gap)
    if x < i.lo:
      return i.lo + ((x - i.lo) % gap)
    return x
  
  def __ne__(i,j):
    lt = gt = n = 0
    for x in i.all():
      for y in j.all():
        n += 1
        if x > y: gt += 1
        if x < y: lt += 1
    return abs(gt - lt) / n > the.COL.dull
        
class Cache:
  def __init__(i, init=[], max=None):
    i.n, i.all, i.max = 0,[],max or the.COL.cache
    map(i.__iadd__,init)
  def __iadd__(i,x):
    i.n += 1
    now = len(i.all)
    if now < i.max:
      i.all += [x]
    elif r() <= now/i.n:
      i.all[ int(r() * now) ]= x
    return i
 
