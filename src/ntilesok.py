from __future__ import print_function, division
import sys,random
sys.dont_write_bytecode = True
from ok import *

from ntiles import *

"""

# showing off ntiles

"""

r = random.random
rseed = random.seed


@ok
def _ntiles():
  r1  = [ r() for _ in xrange(1000)]
  r2 = [ x**2 for x in r1]
  print("\nlong",ntiles(r1,ordered=False))
  print("\nshort",ntiles(r1,tiles=[0.25,0.5,0.75]))    
  print("\nother",ntiles(r2))

@ok
def _isSorted2():
  assert isSorted([1,2,3])
  assert isSorted([1,4,3]) 
  
  
  