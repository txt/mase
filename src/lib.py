from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from ok import *

def bchop(a, k, lo=0, hi=None,
          x= lambda z:z, y=lambda z:z, ordered=True):
  hi = hi or len(a) - 1
  a  = a if ordered else sorted(a,key=x)
  print(a)
  if k <= x(a[0]): return y(a[0])
  if k > x(a[-1]): return y(a[-1])
  while lo < hi:
    if hi < lo: return None
    mid = (lo+hi)//2
    midval = x(a[mid])
    if midval < k  : lo = mid+1
    elif midval > k: hi = mid - 2
    else:            return y(a[mid])
    print(midval,lo,mid,hi)
  return None

@ok
def _bchop():
  lst = [(1,"juca"),(22,"james"),(53,"xuxa"),(44,"delicia")]
  first = lambda z:z[0]
  last  = lambda z:z[-1]
  print(bchop(lst,4,ordered=False,x=first,y=last))
