from __future__ import print_function,division

"""

# Anywhere: Randomized Local Search

"""

from lib   import *
from table import *

@setting
def ANY(): return o(
    poles=20
)

def anywhere(f):
  t = readcsv(f)
  n = len(t.rows)
  anywhere1(t,
    10 if n < 50 else the.ANY.poles)

def anywhere1(t,n):
  log   = Num()
  t.rows= shuffle(t.rows)
  poles = t.rows[:n]
  rows  = t.rows[n:]
  v = {}
  while poles:
    e  = poles.pop()
    w  = poles.pop()
    c  = e - w
    se = e.fromHell()
    sw = w.fromHell()
    if sw > se:
      e,se,w,sw = w,sw,e,se
    for row in rows:
      v[row.id] = v.get(row.id,0) + \
                  row.xy(e,w,c).s  
  lst = sorted(v.values())
  for z in lst: log += z
  print([int(100*log.norm(z)) for z in lst])
