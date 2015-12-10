from __future__ import division
import random
r= random.random

def diff(lst1,lst2,
       small= [0.147, 0.33, 0.474][0],
       ca   = [(0.05,1.36), (0.01,1.63)][0][1]):
  gt = lt = dnn = 0
  n1,n2 = len(lst1),len(lst2)
  for x,y in zip(sorted(lst1),sorted(lst2)):
    diff = abs(x-y)
    if diff > dnn: dnn = diff
    for z in lst2:
      if x > z: gt += 1
      if x < z: lt += 1
  ks = ca*( (n1+n2) / (n1*n2 ) )**0.5
  cd = abs(gt - lt) / (n1*n2)
  
  print dict(diff=diff,gt=gt,dnn = dnn,lt=lt,ks=ks,cd=cd,small=small)
  return dnn > ks, cd > small

def _diff():
  n = 256
  m = 1.15
  lst1 = [r() for _ in xrange(n)]
  lst2 = [x*m for x in lst1]
  return diff(lst1,lst2)

print _diff()
