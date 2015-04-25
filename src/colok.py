#!/usr/bin/python
from __future__ import print_function,division

from col import *

@ok
def _sym():
  lst1 = list('to be or not to be')
  lst2 = list('that is the question')
  s = Sym(lst1)
  for c in lst2:
    s += c
  show(s)

@ok
def _nums(n = 512):
  seed(1)
  sum1 = sum2 = sum3 = 0
  tiles= [x/100.0 for x in xrange(1,100,1)]
  with settings(use(COL,cache = 128)):
    lst1 = sorted([r() for _ in xrange(n)])
    lst2 = sorted([r() for _ in xrange(n)])
    lst3 = Num(lst1).all()
    for x,y,z in zip(ntiles(lst1, tiles),
                     ntiles(lst2, tiles),
                     ntiles(lst3, tiles)):
                     
      sum1 += x
      sum2 += y
      sum3 += z
  randomError   = abs(1 - sum1/sum2)
  samplingError = abs(1 - sum2/sum3)
  assert randomError > samplingError

@ok
def _equal(n=12):
  seed(1)
  lst1 = [r() for _ in xrange(n)]
  p    = 1.01
  lst2 = [z**p for z in lst1]
  assert not Num(lst1) != Num(lst2)
  p    = 1.2
  lst3 = [z**p for z in lst1]
  assert Num(lst1) != Num(lst3)
