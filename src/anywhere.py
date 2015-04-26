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
  log = Num()
  t.rows= shuffle(t.rows)
  poles = t.rows[:n]
  rows  = t.rows[n:]
  while poles:
    e   = poles.pop()
    w   = poles.pop()
    c   = e - w
    se  = e.fromHell()
    sw  = w.fromHell()
    if sw > se:
      e,se,w,sw = w,sw,e,se
    least = sorted([row.xy(e,w,c) for row in rows],
                   key = lambda row : row.x)
    least = [x for x in least
             if 0 <= x.x <= c][0].it
    most = dist(least,e,t)
    maybe = sorted([place(pole,e,t) for pole in poles])
    if maybe:
      maybe = maybe[-1][-1]
      print(maybe.id,
            e.id,
            dist(maybe,e,t),
            c)
    #exit()
    #for b in best:
     # print(b)
   
#       for (i,pole) in enumerate(poles)
    
#        return here1(t,c,n,e,w,se,sw,rows,poles)
#     else:
#       return here1(t,c,n,w,e,sw,se,rows,poles)
    
#     for one in rows:
#       asIs = one
#       toBe = here(t,c,n,e,w,se,sw,poles)
#       log +=   dist(asIs,toBe,t)
#   print(g(log.ntiles([0.1,0.2,0.3,0.4,
#                       0.5,0.6,0.7,0.8,0.9])))

def place(pole,i,t):
  w = pole.fromHell()
  d = dist(i,pole,t)
  return w / d**2, d,pole
  
# def here(t,c,n,e,w,se,sw,rows,poles):
  

# def here1(t,one,c,n,e,w,se,sw,poles):
#   a   = e - one
#   b   = w - one + 0.0001
#   x   = (a**2 + c**2 - b**2) / (2*c)
#   new = one.cells[:]
#   if 0 <= x <= c:
#     y   = (a**2 - x**2)**0.5 + 0.0001
#     inc = (a/b)*(se - sw)/(y**2) / n 
#     for hdr in t.indep.values():
#       j = hdr.pos
#       if j in t.num:
#         new[j] = hdr.wrap(one[j] + inc*(e[j] - one[j]))
#       else:
#         new[j] = e[j] if inc < r() else one[j]
#   return new
    
