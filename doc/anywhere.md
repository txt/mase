[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)
[Contents](https://github.com/txt/mase/blob/master/TOC.md) | [About](https://github.com/txt/mase/blob/master/ABOUT.md) | [Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) | [Code](https://github.com/txt/mase/tree/master/src) | [Contact](http://menzies.us)</em>



# Anywhere: Randomized Local Search

````python

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
    
````

__________


![lic](https://raw.githubusercontent.com/txt/mase/master/img/license.png)

Copyright © 2015 [Tim Menzies](http://menzies.us), email: <tim.menzies@gmail.com>.

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

