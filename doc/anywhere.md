
<em>[Home](https://github.com/txt/mase/blob/master/README.md)   
[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner.png">](https://github.com/txt/mase/blob/master/README.md)
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
    
````

__________


![lic](img/license.png)

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

