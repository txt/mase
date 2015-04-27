from __future__ import print_function,division

"""

# Anywhere: Randomized Local Search

"""

from lib   import *
from table import *

@setting
def ANY(): return o(
    poles=10
)

def anywhere(f):
  t      = readcsv(f)
  t.rows = shuffle(t.rows)
  n      = the.ANY.poles
  m      = min(len(t.rows) - n, 64)
  rows   = t.rows[-1*m:]
  poles  = sorted(t.rows[:n],
                  key=lambda x:x.fromHell())
  w      = poles[0]
  v      = {}
  for e in poles[1:]:
    c  = e - w
    for row in rows:
      v[row.id] = v.get(row.id,0) + \
                  row.xy(e,w,c,score=True).s
  print(g(ntiles(sorted(v.values()),
                 norm=True)))
  #print(sorted(v.values()))
