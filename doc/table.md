[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[About](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Contact](http://menzies.us) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md)  (4 my grad class)


# Table: tables of data

````python

from lib import *
from col import *

@setting
def TBL(): return o(
    bad  = r'(["\' \t\r\n]|#.*)',
    sep  = ",",
    skip = "?",
    num  = '$',
    less = '<',
    more = '>',
    norm = True
)

def readcsv(file, t = None): 
  for cells in lines(file):
    if t:
      Row(cells,t)
    else:
      t = table0(cells)
  return t

def lines(file) :
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  kept = ""
  for line in open(file):
    now   = re.sub(the.TBL.bad,"",line)
    kept += now
    if kept:
      if not now[-1] == the.TBL.sep:
        yield map(atom, kept.split(the.TBL.sep))
        kept = ""

def table0(cells):
  t = o(num={},  sym={},  rows=[], all =[],indep={},
        less={}, more={}, goal={}, fields=cells)
  my= the.TBL
  def nump(cell):
    for char in [my.num, my.less, my.more]:
      if char in cell:
        return True
  for i,cell in enumerate(cells):
    if nump(cell):
      hdr = t.num[i] = Num()  
    else:
      hdr = t.sym[i] = Sym()
    hdr.txt = cell
    hdr.pos = i
    t.all += [hdr]
    if my.less in cell: t.goal[i] = t.less[i] = hdr
    if my.more in cell: t.goal[i] = t.more[i] = hdr
    if not i in t.goal: t.indep[i]= hdr
  return t

def clone(t):
  return table0(t.fields)
def rows2Table(t,rows):
  return cells2Table(t,[row.cells for row in rows])
def cells2Table(t,lstOfCells):
  t1 = clone(t)
  for cells in lstOfCells: Row(cells,t1)
  return t1

class Row:
  id=0
  def __init__(i,cells=[],t=None):
    Row.id  = i.id = Row.id + 1
    i.cells = cells
    i._cache = None
    if t:
      i.table = t
      t.rows += [i]
      i += cells
  def __iadd__(i,cells):
    i._cache = None
    for hdr in i.table.all:
      tmp = cells[hdr.pos]
      if tmp != the.TBL.skip:
        hdr += tmp
    return i
  def __getitem__(i,k): return i.cells[k]
  def __sub__(i,j)    : return dist(i,j,i.table)
  def __hash__(i)     : return i.id
  def __repr__(i)     : return '<'+str(i.cells)+'>'
  def xy(i,e,w,c,score=False):
    a = i - e
    b = i - w
    x = (a**2 + c**2 - b**2) / (2*c+0.00001)
    h = a if a**2 >= x**2 else b
    y = (h**2 - x**2)**0.5
    s = 0
    if score:
      if 0 <= x <= c:
        s = (b/a)*(e.fromHell() - w.fromHell())/c/y
    return o(it=i, a=a, b=b, c=c, x=x, y=y, s=s)
  @cache
  def fromHell(i) :
    n = inc = 0
    for hdr in i.table.more.values():
      n   += 1
      x    = i[hdr.pos]
      inc += hdr.fromHell(x,the.TBL.norm,True)
    for hdr in i.table.less.values():
      n   += 1
      x    = i[hdr.pos]
      inc += hdr.fromHell(x,the.TBL.norm,False)
    return inc**0.5 / n**0.5


def furthest(i,rows=None,t=None):
  return closest(i,rows,t, last=-10**32, better=gt)

def closest(i,rows=None,t=None, last=10**32, better=lt):
  t    = t or i.table
  rows = rows or t.rows
  out  = None
  for row in rows:
    if row.id != i.id:
      tmp = dist(i,row,t)
      if better(tmp,last):
        last,out = tmp,row
  return out
  
def dist(i,j,t):
  n = inc = 0
  skip = the.TBL.skip
  for hdr in t.indep.values():
    k    = hdr.pos
    x, y = i[k], j[k]
    if x == y == skip:
      continue
    n += 1
    if k in t.sym:
      inc += 0 if x==y else 1
    else:
      lo, hi = hdr.lo, hdr.hi
      mid    = (hi - lo)/2
      if the.TBL.norm:
        if x != skip: x = hdr.norm(x)
        if y != skip: y = hdr.norm(y)
        lo, hi, mid = 0, 1, 0.5
      if x == skip: x = hi if y < mid else lo
      if y == skip: y = hi if x < mid else lo
      inc += (x-y)**2
  return inc**0.5 / (n + 0.000001)**0.5
````


_________

<img src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">  

Copyright © 2015 [Tim Menzies](http://menzies.us).


This is free and unencumbered software released into the public domain.

For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

