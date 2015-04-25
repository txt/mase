from __future__ import print_function,division

from lib   import *
from table import *

@setting
def ANY() return o(
    poles=20
)

def anywhere(f):
  t = readcsv(f)
  n = len(t.rows)
  anywhere1(t,
            10 if n < 50 else the.ANY.poles)

def anywhere1(t,n):
  t.rows = shuffle(t.rows)
  poles  = t.rows[:n]
  while poles:
    e  = poles.pop()
    w  = poles.pop()
    c  = e - w
    se = e.fromHell()
    sw = w.fromHell()
    for j in t.rows[n:]:
      if se > sw:
        here(t,j,c,  e,w,se,sw)
      if sw > se:
        here(t,j,c,  w,e,sw,se)

def here(t,j,c,  e,w,se,sw):
  a   = e - j
  b   = w - j
  x   = (a**2 + c**2 - b**2) / (2*c)
  cols= len(t.indep)
  r   = the.ANY.poles
  if 0 <= x <= c:
    y   = (a**2 - x**2)**0.5
    inc = (a/b) * (se - sw)/(y**2) / cols / r
    for hdr in t.indep:
      col = hdr.pos
      j[col] = nudge(t,hdr,inc,
                     j[col], e[col])

def nudge(t,hdr,inc,jx,ex):
  if hdr.pos in t.nums:
    mutation = inc*(ex - jx)
    return hdr.wrap(ex + mutation)
  else:
    return ex if inc < r() else jx
