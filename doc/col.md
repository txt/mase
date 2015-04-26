
<em>[![Home](https://raw.githubusercontent.com/txt/mase/master/img/home.png) Home](https://github.com/txt/mase/blob/master/README.md)   
[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner.png">](https://github.com/txt/mase/blob/master/README.md)
[Contents](https://github.com/txt/mase/blob/master/TOC.md) | [About](https://github.com/txt/mase/blob/master/ABOUT.md) | [Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) | [Code](https://github.com/txt/mase/tree/master/src) | [Contact](http://menzies.us)</em>



# Num,Sym : Knowledge about numbers and symbols

````python

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
    assert isinstance(x,(float,int))
    i.ordered = False
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
    i._cache += x
    return i
  def all(i):
    if not i.ordered:
      i._cache.all = sorted(i._cache.all)
      i.ordered = True
    return i._cache.all
  def norm(i,x):
    return (x - i.lo) / (i.hi - i.lo + 0.00001)
  def trim(i,x):
    return max(i.lo, min(x, i.hi))
  def ntiles(i,t=[0.1,0.3,0.5,0.7,0.9]):
    return ntiles(i.all(),t)
  def fromHell(i,x,norm, want):
    if want:
      hell =  0 if norm else i.lo
    else:
      hell =  1 if norm else i.hi
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
 
````

__________


![lic](https://raw.githubusercontent.com/txt/mase/master/img/license.png)

Copyright © 2015 [Tim Menzies](http://menzies.us), email: <tim.menzies@gmail.com>.

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

