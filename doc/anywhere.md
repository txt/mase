[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[About](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Contact](http://menzies.us) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) 


# Anywhere: Randomized Local Search

````python

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
      old = v.get(row.id,0)
      new = row.xy(e,w,c,score=True).s
      v[row.id] = max(old,new)
  print(g(ntiles(sorted(v.values()),
                 norm=True)))
  #print(sorted(v.values()))
````


_________

<img src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">  

Copyright © 2015 [Tim Menzies](http://menzies.us).


This is free and unencumbered software released into the public domain.

For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

