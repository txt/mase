from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# Test suite for a generic optimizer

"""
from ok import *
from gadgets import *

@ok
def _seed():
  seed(1)
  assert 0.134364244111 < r() < 0.134364244113 

@ok
def _log():
  with study("log",
             use(somes,size=10)):
    log = Log()
    [log + y for y in
     shuffle([x for x in xrange(20)])]
    assert log.lo==0
    assert log.hi==19
    assert log.some() == [9, 11, 13, 15, 6,
                          19, 12, 14, 16, 1]
  # after the study, all the defaults are
  # back to zero
  assert the.somes.size == 256

@ok
def _fill():
  b4 = Candidate([1,2],[2,4])
  assert str(fill(b4)) ==  \
         "o{'aggregate': None, "  + \
         "'objs': [None, None], " + \
         "'decs': [None, None]}"

print(More('asd'))
