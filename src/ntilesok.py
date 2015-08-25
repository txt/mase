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
  print(ntiles(r1))
  print(ntiles(r2))
