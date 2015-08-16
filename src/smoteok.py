from __future__ import print_function, division
from ok import *
import sys
sys.dont_write_bytecode = True
from smote import *

@ok
def _some():
  rseed(1)
  s = Some(16)
  for i in xrange(100000):
    s += i
  assert sorted(s.any)== [ 5852, 24193, 28929, 38266,
                          41764, 42926, 51310, 52203,
                          54651, 56743, 59368, 60794,
                          61888, 82586, 83018, 88462]
  print(s.hi())

weather="""

outlook,
temperature,
humidity,?windy,play
sunny    , 85, 85, FALSE, no  # an interesting case
sunny    , 80, 90, TRUE , no
overcast , 83, 86, FALSE, yes
rainy    , 70, 96, FALSE, yes
rainy    , 68, 80, FALSE, yes
rainy    , 65, 70, TRUE , no
overcast , 64, 65, TRUE , 
yes
sunny    , 72, 95, FALSE, no

sunny    , 69, 70, FALSE, yes
rainy    , 75, 80, FALSE, yes
sunny    , 75, 70, TRUE , yes
overcast , 72, 90, TRUE , yes
overcast , 81, 75, FALSE, yes
rainy    , 71, 91, TRUE , no"""
