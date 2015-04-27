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
  t.rows = shuffle(t.rows)
  rows  = t.rows[n:]
  poles = sorted(t.rows[:n],
                 key=lambda x:x.fromHell())
  w = poles[0]
  v = {}
  for e in poles[1:]:
    c  = e - w
    se = e.fromHell()
    sw = w.fromHell()
    if sw > se:
      e,se,w,sw = w,sw,e,se
    for row in rows:
      v[row.id] = v.get(row.id,0) + \
                  row.xy(e,w,c,score=True).s
  tiles=[0.1,0.2,0.4,0.8,0.9,0.95,0.99]
  print(g(ntiles(sorted(v.values()),
                 tiles=tiles,
                 norm=True)))
  #print(sorted(v.values()))
