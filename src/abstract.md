[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 




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

<a href="abstract.py#L56-L62"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def items(x, depth=-1):
   2:     if isinstance(x,(list,tuple)):
   3:       for y in x:
   4:         for z in items(y, depth+1):
   5:           yield z
   6:     else:
   7:       yield depth,x
```

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

<a href="abstract.py#L114-L139"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   r = random.random
   2:   rseed = random.seed
   3:   
   4:   class Some:
   5:     def __init__(i, max=8): # note, usually 256 or 128 or 64 (if brave)
   6:       i.n, i.any, i.max = 0,[],max
   7:     def __iadd__(i,x):
   8:       i.n += 1
   9:       now = len(i.any)
  10:       if now < i.max:    # not full yet, so just keep it   
  11:         i.any += [x]
  12:       elif r() <= now/i.n:
  13:         i.any[ int(r() * now) ]= x # zap some older value
  14:       #else: forget x
  15:       return i
  16:   
  17:   @ok
  18:   def _some():
  19:     rseed(1)
  20:     s = Some(16)
  21:     for i in xrange(100000):
  22:       s += i
  23:     assert sorted(s.any)== [ 5852, 24193, 28929, 38266,
  24:                             41764, 42926, 51310, 52203,
  25:                             54651, 56743, 59368, 60794,
  26:                             61888, 82586, 83018, 88462]
```
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

<a href="abstract.py#L201-L222"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   weather="""
   2:   
   3:   outlook,
   4:   temperature,
   5:   humidity,?windy,play
   6:   sunny    , 85, 85, FALSE, no  # an interesting case
   7:   sunny    , 80, 90, TRUE , no
   8:   overcast , 83, 86, FALSE, yes
   9:   rainy    , 70, 96, FALSE, yes
  10:   rainy    , 68, 80, FALSE, yes
  11:   rainy    , 65, 70, TRUE , no
  12:   overcast , 64, 65, TRUE , 
  13:   yes
  14:   sunny    , 72, 95, FALSE, no
  15:   
  16:   sunny    , 69, 70, FALSE, yes
  17:   rainy    , 75, 80, FALSE, yes
  18:   sunny    , 75, 70, TRUE , yes
  19:   overcast , 72, 90, TRUE , yes
  20:   overcast , 81, 75, FALSE, yes
  21:   rainy    , 71, 91, TRUE , no"""
  22:   
```

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

<a href="abstract.py#L245-L260"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class o:
   2:     """Emulate Javascript's uber simple objects.
   3:     Note my convention: I use "`i`" not "`this`."""
   4:     def __init__(i,**d)    : i.__dict__.update(d)
   5:     def __setitem__(i,k,v) : i.__dict__[k] = v
   6:     def __getitem__(i,k)   : return i.__dict__[k]
   7:     def __repr__(i)        : return 'o'+str(i.__dict__)
   8:   
   9:   @ok
  10:   def _o():
  11:     x = o(name='tim',shoesize=9)
  12:     assert x.name     == 'tim'
  13:     assert x["name"]  == 'tim'
  14:     x.shoesize += 1
  15:     assert x.shoesize == 10
  16:     assert str(x) == "o{'name': 'tim', 'shoesize': 10}"
```
  
### Serious Python JuJu

Tricks to let us read from strings or files or zip files
or anything source at all. 

Not for beginners.

<a href="abstract.py#L271-L287"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def STRING(str):
   2:     def wrapper():
   3:       for c in str: yield c
   4:     return wrapper
   5:   
   6:   def FILE(filename, buffer_size=4096):
   7:     def chunks(filename):
   8:       with open(filename, "rb") as fp:
   9:         chunk = fp.read(buffer_size)
  10:         while chunk:
  11:           yield chunk
  12:           chunk = fp.read(buffer_size)
  13:     def wrapper():
  14:       for chunk in chunks(filename):
  15:         for char in chunk:
  16:           yield char
  17:     return wrapper
```

## Iterators

### Lines

Yield each line in a string

<a href="abstract.py#L297-L312"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def lines(src):
   2:     tmp=''
   3:     for ch in src(): # sneaky... src can evaluate to different ghings
   4:       if ch == "\n":
   5:         yield tmp
   6:         tmp = ''
   7:       else:
   8:         tmp += ch # for a (slightly) faster method,
   9:                   # in Python3, see http://goo.gl/LvgGx3
  10:     if tmp:
  11:       yield tmp
  12:   
  13:   @ok
  14:   def _line():
  15:     for line in lines(STRING(weather)):
  16:       print("[",line,"]",sep="")
```

### Rows

Yield all non-blank lines,
joining lines that end in ','.

<a href="abstract.py#L321-L337"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def rows(src):
   2:     b4 = ''
   3:     for line in lines(src):
   4:       line = re.sub(r"[\r\t ]*","",line)
   5:       line = re.sub(r"#.*","",line)
   6:       if not line: continue # skip blanks
   7:       if line[-1] == ',':   # maybe, continue lines
   8:         b4 += line
   9:       else:
  10:         yield b4 + line
  11:         b4 = ''
  12:         
  13:   @ok
  14:   def _row():
  15:     for row in rows(STRING(weather)):
  16:       print("[",row,"]",sep="")
  17:   
```

### Values

Coerce row values to floats, ints or strings. 
Jump over any cols we are ignoring

<a href="abstract.py#L346-L352"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def values(src):
   2:     want = None
   3:     for row in rows(src):
   4:       lst  = row.split(',')
   5:       want = want or [col for col in xrange(len(lst))
   6:                       if lst[col][0] != "?" ]
   7:       yield [ make(lst[col]) for col in want ]
```

Helper function.

<a href="abstract.py#L358-L362"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def make(x):
   2:     try   : return int(x)
   3:     except:
   4:       try   : return float(x)
   5:       except: return x
```

Test function.

<a href="abstract.py#L368-L371"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   @ok
   2:   def _values():
   3:     for cells in values(STRING(weather)):
   4:       print(cells)
```

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

<a href="abstract.py#L383-L396"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def table(src, klass= -1, keep= False):
   2:     t = None
   3:     for cells in values(src):
   4:       if t:
   5:         k = cells[klass]
   6:         for cell,some in zip(cells,t.klasses[k]):
   7:           some += cell
   8:         if keep:
   9:           t.rows += [cells]
  10:       else:
  11:        t = o(header = cells,
  12:              rows   = [],
  13:              klasses= Default(lambda: klass0(t.header)))
  14:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="abstract.py#L406-L417"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Default(dict):
   2:     def __init__(i, default): i.default = default
   3:     def __getitem__(i, key):
   4:       if key in i: return i.get(key)
   5:       return i.setdefault(key, i.default())
   6:   
   7:   def klass0(header):
   8:    tmp = [Some() for _ in header]
   9:    for n,header1 in enumerate(header):
  10:      tmp[n].pos  = n
  11:      tmp[n].name = header1
  12:    return tmp
```

Test functions: read from strings or files.

<a href="abstract.py#L423-L433"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   @ok
   2:   def _tableFromString(src = STRING(weather)):
   3:     t = table(src)
   4:     for k,v in t.klasses.items():
   5:       for some in v:
   6:         print(":klass",k,":name",some.name,":col",some.pos,
   7:               ":seen",some.n,"\n\t:kept",some.any)
   8:   
   9:   @ok
  10:   def _tableFromFile():
  11:     _tableFromString(FILE("weather.csv"))
```

## Sanity Check

How much do we lose if from some sample `s1` we only keep some of the items in `s2`?
And just to make this interesting, we'll compare this error to what happens
if I sample that distribution twice, once to `s1` and once to `s3`.

For the results of the following code, see the top of this file.

<a href="abstract.py#L445-L477"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def samples(m0=128,f=random.random):
   2:     print("\n         \t    diff to all    \t    \t     diff to all")
   3:     print("         \t -------------------\t    \t -------------------")
   4:     print("all kept \t 10% 30% 50% 70% 90%\t kept\t 10% 30% 50% 70% 90%")
   5:     print("--- ---- \t --- --- --- --- ---\t ----\t --- --- --- --- ---")
   6:     m = m0
   7:     for _ in xrange(7):
   8:       m = m * 2
   9:       n = min(m0,m)
  10:       s1,s2,s3 = Some(m), Some(n),Some(m)
  11:       for _ in xrange(m):
  12:         x,y = f(),f()
  13:         s1 += x
  14:         s2 += x
  15:         s3 += y
  16:       print(m,"",n, "\t",diff(s1,s2),"\t",m,"\t",diff(s1,s3))
  17:   
  18:   def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
  19:     "Return percentiles in a list"
  20:     at  = lambda x: lst[ int(len(lst)*x) ]
  21:     return [ at(tile) for tile in tiles ]
  22:     
  23:   def diff(s1,s2):
  24:     "Return difference in the percentiles"
  25:     return [ abs(int(100*(most-less)))
  26:              for most,less in
  27:              zip(ntiles(sorted(s1.any)),
  28:                        ntiles(sorted(s2.any))) ]
  29:   
  30:   @ok
  31:   def _samples():
  32:     rseed(1)
  33:     for x in [64,128,256,512]:
  34:       samples(x)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

