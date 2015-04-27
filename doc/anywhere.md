[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)
[Contents](https://github.com/txt/mase/blob/master/TOC.md) | [About](https://github.com/txt/mase/blob/master/ABOUT.md) | [Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) | [Code](https://github.com/txt/mase/tree/master/src) | [Contact](http://menzies.us)</em>



# Anywhere: Randomized Local Search

````python

from lib   import *
from table import *

@setting
def ANY(): return o(
    poles=10
)

def anywhere(f):
  t = readcsv(f)
  n = len(t.rows)
  anywhere1(t,
    10 if n < 50 else the.ANY.poles)

def anywhere1(t,n):
  log   = Num()
  t.rows = shuffle(t.rows)
  rows  = t.rows[-64:]
  poles = t.rows[:n]
  poles = sorted(poles, key=lambda x:x.fromHell())
  w = poles[0]
  v={}
  for e in poles[1:]:
    c  = e - w
    se = e.fromHell()
    sw = w.fromHell()
    if sw > se:
      e,se,w,sw = w,sw,e,se
    for row in rows:
      v[row.id] = v.get(row.id,0) + \
                  row.xy(e,w,c,score=True).s
  print(g(ntiles(sorted(v.values()),
                 tiles=[0.5,0.9,0.95,0.99],
                 norm=True)))
  #print(sorted(v.values()))
````



<img align=left src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">
Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

