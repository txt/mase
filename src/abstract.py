from __future__ import print_function, division
from ok import *
import random,re

"""

# Abstraction (Advanced Python Coding)



Layers within layers within layers..

In the following, we will
divide the problem into layers of abstraction where `iterators`
separate out the various concerns. Easier to debug! Good
Zen Python coding.


## Background

From Wikipedia:

+ In computer science, abstraction is a technique for managing complexity of computer systems. 
+ It works by establishing a level of complexity on which a person interacts with the system, suppressing the more complex details below the current level. 
+ The programmer works with an idealized interface (usually well defined) and can add additional levels of functionality that would otherwise be too complex to handle. 
  + For example, a programmer writing code that involves numerical operations may not be interested in the way numbers are represented in the underlying hardware (e.g. whether they're 16 bit or 32 bit integers), and where those details have been suppressed it can be said that they were abstracted away, leaving simply numbers with which the programmer can work. 
  + In addition, a task of sending an email message across continents would be extremely complex if you start with a piece of optic cable and basic hardware components. 
By using layers of complexity that have been created to abstract away the physical cables, network layout and presenting the programmer with a virtual data channel, this task is manageable.

Abstraction can apply to control or to data: Control abstraction is the abstraction of actions while data abstraction is that of data structures.

+ _Data abstraction_ allows handling data bits in meaningful ways. For example, it is the basic motivation behind datatype and object-oriented programming.
+ _Control abstraction_ involves the use of subprograms and related concepts control flows

The rest of this page is about control abstraction, as implemented by Python's iterator. If a functions `return` statement
is replaced with `yield` then that function becomes a _generator_, whose internal details can now be ignored.

For example, if you want to launch a rocket....

```python
def countdown(n):
   while n >= 0:
     yield n
     n -= 1

print("We are go for launch")
for x in countdown(10):
   print(n)
print("lift off!")
```

And here's my favorite iterator that descends recursive lists:

"""
def items(x, depth=-1):
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y, depth+1):
        yield z
  else:
    yield depth,x
"""

This lets me do things like (a) traverse a nested structure and (b) write pretty print that structure.
For example:

```python
for depth,x in items(  [10,
                        [   20,
                            30],
                        40,
                        [   (  50,
                               60,
                               70),
                            [  80,
                               90,
                               100],
                            110]]):
  print(" |.. " *depth,x)
```
Output:

```
10
 |..  20
 |..  30
 40
 |..  |..  50
 |..  |..  60
 |..  |..  70
 |..  |..  80
 |..  |..  90
 |..  |..  100
 |..  110
```

Anyway, lets apply this idea to a real problem. 


## Problem

If   parsing 1,000,000
records, in a table of data, keep  a small sample
of that large space, without blowing memory.

How?

+ Read a table of data and keep some sample of each column.
  Specifically, keep up to `max` things (and if we see more than that,
  delete older values).

"""
r = random.random
rseed = random.seed

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
  assert sorted(s.any)== [ 5852, 24193, 28929, 38266,
                          41764, 42926, 51310, 52203,
                          54651, 56743, 59368, 60794,
                          61888, 82586, 83018, 88462]
"""
Turns out, we do not lose much (caveat: need to keep more than 16... 256 seems a reasonable default).

```
$ python -B abstract.py

              diff to all                  diff to all
           -------------------          -------------------
all kept   10% 30% 50% 70% 90%   kept   10% 30% 50% 70% 90%
--- ----   --- --- --- --- ---   ----   --- --- --- --- ---
128  64    [4, 0, 5, 6, 1]       128    [0, 2, 1, 4, 3]
256  64    [1, 2, 4, 2, 1]       256    [2, 4, 5, 3, 1]
512  64    [1, 0, 2, 3, 7]       512    [0, 0, 5, 4, 1]
1024  64   [1, 5, 10, 4, 1]     1024    [0, 1, 1, 0, 0]
2048  64   [0, 1, 5, 3, 7]      2048    [0, 2, 3, 4, 2]
4096  64   [2, 9, 8, 4, 8]      4096    [0, 1, 0, 1, 0]
8192  64   [0, 4, 3, 2, 0]      8192    [0, 0, 0, 0, 0]

                diff to all                diff to all
             -------------------         -------------------
all kept     10% 30% 50% 70% 90%  kept   10% 30% 50% 70% 90%
--- ----     --- --- --- --- ---  ----   --- --- --- --- ---
256  128     [0, 0, 1, 0, 0]      256    [3, 0, 4, 2, 1]
512  128     [3, 2, 2, 6, 0]      512    [0, 1, 5, 6, 1]
1024  128    [6, 7, 5, 5, 1]     1024    [0, 2, 0, 3, 0]
2048  128    [1, 2, 2, 0, 2]     2048    [0, 1, 1, 0, 0]
4096  128    [1, 0, 3, 0, 1]     4096    [1, 2, 1, 0, 0]
8192  128    [5, 3, 1, 0, 0]     8192    [0, 0, 1, 0, 0]
16384  128   [5, 9, 3, 0, 0]     16384   [0, 0, 0, 0, 0]

                 diff to all                diff to all
             -------------------         -------------------
all kept     10% 30% 50% 70% 90%  kept   10% 30% 50% 70% 90%
--- ----     --- --- --- --- ---  ----   --- --- --- --- ---
512  256     [0, 1, 1, 1, 0]      512    [1, 2, 0, 0, 1]
1024  256    [1, 1, 4, 2, 0]     1024    [0, 1, 2, 1, 0]
2048  256    [1, 2, 1, 2, 0]     2048    [0, 0, 0, 0, 1]
4096  256    [0, 1, 1, 2, 0]     4096    [0, 1, 0, 0, 0]
8192  256    [3, 2, 1, 5, 4]     8192    [0, 0, 0, 0, 0]
16384  256   [3, 0, 4, 3, 0]    16384   [0, 0, 0, 0, 0]
32768  256   [0, 2, 5, 5, 2]    32768   [0, 0, 0, 0, 0]

              diff to all                diff to all
           -------------------         -------------------
all kept   10% 30% 50% 70% 90%  kept   10% 30% 50% 70% 90%
--- ----   --- --- --- --- ---  ----   --- --- --- --- ---
1024  512    [2, 0, 0, 0, 0]   1024    [1, 1, 2, 3, 0]
2048  512    [0, 0, 1, 0, 0]   2048    [0, 1, 0, 0, 2]
4096  512    [0, 0, 1, 0, 1]   4096    [1, 0, 0, 0, 0]
8192  512    [1, 0, 0, 1, 2]   8192    [0, 0, 0, 0, 0]
16384  512   [0, 2, 1, 0, 0]   16384   [0, 0, 0, 0, 0]
32768  512   [1, 2, 1, 0, 2]   32768   [0, 0, 0, 0, 0]
65536  512   [1, 1, 0, 0, 0]   65536   [0, 0, 0, 0, 0]
```


## Example data

14 items: 9 examples of playing golf, 5 of not playing golf.

"""
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

"""

Note that the table is messy- blank lines, spaces, comments,
some lines split over multiple physical lines.  
Also:

+ there are some columns we just want to ignore (see `?windy`)
+  when we read these strings, we need to coerce
  these values to either strings, ints, or floats.
+ This string has rows belonging to different `klass`es
  (see last column). We want our tables to keep counts
  separately for each column.

Lets handle all that mess with iterators.

## Support code

### Standard Header

Load some standard tools.

"""
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
"""
  
### Serious Python JuJu

Tricks to let us read from strings or files or zip files
or anything source at all. 

Not for beginners.

"""
def STRING(str):
  def wrapper():
    for c in str: yield c
  return wrapper

def FILE(filename, buffer_size=4096):
  def chunks(filename):
    with open(filename, "rb") as fp:
      chunk = fp.read(buffer_size)
      while chunk:
        yield chunk
        chunk = fp.read(buffer_size)
  def wrapper():
    for chunk in chunks(filename):
      for char in chunk:
        yield char
  return wrapper
"""

## Iterators

### Lines

Yield each line in a string

"""
def lines(src):
  tmp=''
  for ch in src(): # sneaky... src can evaluate to different ghings
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch # for a (slightly) faster method,
                # in Python3, see http://goo.gl/LvgGx3
  if tmp:
    yield tmp

@ok
def _line():
  for line in lines(STRING(weather)):
    print("[",line,"]",sep="")
"""

### Rows

Yield all non-blank lines,
joining lines that end in ','.

"""
def rows(src):
  b4 = ''
  for line in lines(src):
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
  for row in rows(STRING(weather)):
    print("[",row,"]",sep="")

"""

### Values

Coerce row values to floats, ints or strings. 
Jump over any cols we are ignoring

"""
def values(src):
  want = None
  for row in rows(src):
    lst  = row.split(',')
    want = want or [col for col in xrange(len(lst))
                    if lst[col][0] != "?" ]
    yield [ make(lst[col]) for col in want ]
"""

Helper function.

"""
def make(x):
  try   : return int(x)
  except:
    try   : return float(x)
    except: return x
"""

Test function.

"""
@ok
def _values():
  for cells in values(STRING(weather)):
    print(cells)
"""

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

"""
def table(src, klass= -1, keep= False):
  t = None
  for cells in values(src):
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
"""

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

"""
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
"""

Test functions: read from strings or files.

"""           
@ok
def _tableFromString(src = STRING(weather)):
  t = table(src)
  for k,v in t.klasses.items():
    for some in v:
      print(":klass",k,":name",some.name,":col",some.pos,
            ":seen",some.n,"\n\t:kept",some.any)

@ok
def _tableFromFile():
  _tableFromString(FILE("weather.csv"))
"""

## Sanity Check

How much do we lose if from some sample `s1` we only keep some of the items in `s2`?
And just to make this interesting, we'll compare this error to what happens
if I sample that distribution twice, once to `s1` and once to `s3`.

For the results of the following code, see the top of this file.

"""
def samples(m0=128,f=random.random):
  print("\n         \t    diff to all    \t    \t     diff to all")
  print("         \t -------------------\t    \t -------------------")
  print("all kept \t 10% 30% 50% 70% 90%\t kept\t 10% 30% 50% 70% 90%")
  print("--- ---- \t --- --- --- --- ---\t ----\t --- --- --- --- ---")
  m = m0
  for _ in xrange(7):
    m = m * 2
    n = min(m0,m)
    s1,s2,s3 = Some(m), Some(n),Some(m)
    for _ in xrange(m):
      x,y = f(),f()
      s1 += x
      s2 += x
      s3 += y
    print(m,"",n, "\t",diff(s1,s2),"\t",m,"\t",diff(s1,s3))

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
  "Return percentiles in a list"
  at  = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]
  
def diff(s1,s2):
  "Return difference in the percentiles"
  return [ abs(int(100*(most-less)))
           for most,less in
           zip(ntiles(sorted(s1.any)),
                     ntiles(sorted(s2.any))) ]

@ok
def _samples():
  rseed(1)
  for x in [64,128,256,512]:
    samples(x)
