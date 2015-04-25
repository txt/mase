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
  anywhere1(
    t,
    10 if n < 50 else the.ANY.poles)

def anywhere1(t,n):
  t.rows = shuffle(t.rows)
  poles  = t.rows[:n]
  rest   = t.rows[n:]
  while poles:
    e  = poles.pop()
    w  = poles.pop()
    c  = e - w
    se = e.fromHell()
    sw = w.fromHell()
    for i in rest:
      if se > sw:
        return here(t,i,c,n,  e,w,se,sw)
      else:
        return here(t,i,c,n,  w,e,sw,se)

def here(t,i,c,n,  e,w,se,sw):
  a   = e - i
  b   = w - i
  x   = (a**2 + c**2 - b**2) / (2*c)
  print(">",x,c)
  if 0 <= x <= c:
    cols= len(t.indep)
    r   = the.ANY.poles
    y   = (a**2 - x**2)**0.5
    inc = (a/b) * (se - sw)/(y**2) / cols / n
    old = i.cells
    new = old[:]
    for hdr in t.indep.values():
      j = hdr.pos
      if j in t.num:
        new[j] = hdr.wrap(i[j] + inc*(e[j] - i[j]))
      else:
        new[j] = e[j] if inc < r() else i[j]
    print("")
    print(">",old)
    print(">",new)
    i += new 
    
