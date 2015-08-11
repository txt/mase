[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Abstraction in Python

Layers within layers within layers..

## Problem

Read a huge table of data and keep a sample of each column.

````python

weather="""

outlook,
temperature,
humidity,?windy,play
sunny    , 85, 85, FALSE, no  # an interesting case
sunny    , 80, 90, TRUE , no
overcast , 83, 86, FALSE, yes
rainy    , 70, 96, FALSE, yes
rainy    , 68, 80, FALSE, yes
rainy    , 65, 70, TRUE , no
overcast , 64, 65, TRUE , 
yes
sunny    , 72, 95, FALSE, no

sunny    , 69, 70, FALSE, yes
rainy    , 75, 80, FALSE, yes
sunny    , 75, 70, TRUE , yes
overcast , 72, 90, TRUE , yes
overcast , 81, 75, FALSE, yes
rainy    , 71, 91, TRUE , no"""

````

Note that the table is messy- blank lines, spaces, comments,
some lines split over multiple physical lines.  
Also:

+ there are some columns we just want to ignore (see `?windy`)
+  when we read these strings, we need to coerce
  these values to either strings, ints, or floats.
+ This string has rows belonging to different `klass`es
  (see last column). We want our tables to keep counts
  separately for each column.

## Solution

Divide the problem into layers of abstraction where `iterators`
separate out the various concerns. Easier to debug! Good
Zen Python coding.

## Standard Header

Load some standard tools.

````python
from ok import *
import random,re

r = random.random
rseed = random.seed

class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)

@ok
def _o():
  x = o(name='tim',shoesize=9)
  assert x.name     == 'tim'
  assert x["name"]  == 'tim'
  x.shoesize += 1
  assert x.shoesize == 10
  assert str(x) == "o{'name': 'tim', 'shoesize': 10}"
````

## Sampling with `Some`

Keep up to `max` things (and if we see more than that,
delete older values).

````python
class Some:
  def __init__(i, max=8): # note, usually 256 or 128 or 64 (if brave)
    i.n, i.any, i.max = 0,[],max
  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:    # not full yet, so just keep it   
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x # zap some older value
    #else: forget x
    return i

@ok
def _some():
  rseed(1)
  s = Some(16)
  for i in xrange(100000):
    s += i
  assert sorted(s.any)== [5852, 24193, 28929, 38266,
                          41764, 42926, 51310, 52203,
                          54651, 56743, 59368, 60794,
                          61888, 82586, 83018, 88462]
````

## Iterators

### Lines

Yield each line in a string

````python
def lines(str):
  tmp=''
  for ch in str:
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch
  if tmp:
    yield tmp

@ok
def _line():
  for line in lines(weather):
    print("[",line,"]",sep="")
````

### Rows

Yield all non-blank lines,
joining lines that end in ','.

````python
def rows(str):
  b4 = ''
  for line in lines(str):
    line = re.sub(r"[\r\t ]*","",line)
    line = re.sub(r"#.*","",line)
    if not line: continue # skip blanks
    if line[-1] == ',':   # maybe, continue lines
      b4 += line
    else:
      yield b4 + line
      b4 = ''
      
@ok
def _row():
  for row in rows(weather):
    print("[",row,"]",sep="")

````

### Values

Co-erce row values to floats, ints or strings. 
Jump over any cols we are ignoring

````python
def values(str):
  want = None
  for row in rows(str):
    lst  = row.split(',')
    want = want or [col for col in xrange(len(lst))
                    if lst[col][0] != "?" ]
    yield [ make(lst[col]) for col in want ]
````

Helper function.

````python
def make(x):
  try   : return int(x)
  except:
    try   : return float(x)
    except: return x
````

Test function.

````python
@ok
def _values():
  for cells in values(weather):
    print(cells)

````

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

````python
def table(str, klass= -1, keep= False):
  t = None
  for cells in values(str):
    if t:
      k = cells[klass]
      for cell,some in zip(cells,t.klasses[k]):
        some += cell
      if keep:
        t.rows += [cells]
    else:
     t = o(header = cells,
           rows   = [],
           klasses= Default(lambda: klass0(t.header)))
  return t
````

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

````python
class Default(dict):
  def __init__(i, default): i.default = default
  def __getitem__(i, key):
    if key in i: return i.get(key)
    return i.setdefault(key, i.default())

def klass0(header):
 tmp = [Some() for _ in header]
 for n,header1 in enumerate(header):
   tmp[n].pos  = n
   tmp[n].name = header1
 return tmp
````

Test function.

````python
@ok
def _table():
  t = table(weather)
  for k,v in t.klasses.items():
    for some in v:
      print(":klass",k,":name",some.name,":col",some.pos,
            ":seen",some.n,"\n\t:kept",some.any)

````

Note that for the above data, this machinery is not
that interesting. But consider-- if were parsing 1,000,000
records, the above could be used to get a small sample
of that large space, without blowing memory.

````python
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

