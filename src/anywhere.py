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
  anywhere1(
    t,
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
    for i in t.rows[n:]:
      if se > sw:
        here(t,i,c,n,  e,w,se,sw)
      if sw > se:
        here(t,i,c,n,  w,e,sw,se)

def here(t,i,c,n,  e,w,se,sw):
  a   = e - i
  b   = w - i
  x   = (a**2 + c**2 - b**2) / (2*c)
  cols= len(t.indep)
  r   = the.ANY.poles
  if 0 <= x <= c:
    y   = (a**2 - x**2)**0.5
    inc = (a/b) * (se - sw)/(y**2) / cols / n
    for hdr in t.indep:
      col = hdr.pos
      i[col] = nudge(t,hdr,inc,
                     i[col], e[col])

def nudge(t,hdr,inc,ix,ex):
  if hdr.pos in t.nums:
    return hdr.wrap(ex + inc*(ex - ix))
  else:
    return ex if inc < r() else ix
