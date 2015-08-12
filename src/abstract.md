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

````python
<font color=red>   1:</font> def items(x, depth=-1):
<font color=red>   2:</font>   if isinstance(x,(list,tuple)):
<font color=red>   3:</font>     for y in x:
<font color=red>   4:</font>       for z in items(y, depth+1):
<font color=red>   5:</font>         yield z
<font color=red>   6:</font>   else:
<font color=red>   7:</font>     yield depth,x
````

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

````python
<font color=red>   8:</font> r = random.random
<font color=red>   9:</font> rseed = random.seed
<font color=red>  10:</font> 
<font color=red>  11:</font> class Some:
<font color=red>  12:</font>   def __init__(i, max=8): # note, usually 256 or 128 or 64 (if brave)
<font color=red>  13:</font>     i.n, i.any, i.max = 0,[],max
<font color=red>  14:</font>   def __iadd__(i,x):
<font color=red>  15:</font>     i.n += 1
<font color=red>  16:</font>     now = len(i.any)
<font color=red>  17:</font>     if now < i.max:    # not full yet, so just keep it   
<font color=red>  18:</font>       i.any += [x]
<font color=red>  19:</font>     elif r() <= now/i.n:
<font color=red>  20:</font>       i.any[ int(r() * now) ]= x # zap some older value
<font color=red>  21:</font>     #else: forget x
<font color=red>  22:</font>     return i
<font color=red>  23:</font> 
<font color=red>  24:</font> @ok
<font color=red>  25:</font> def _some():
<font color=red>  26:</font>   rseed(1)
<font color=red>  27:</font>   s = Some(16)
<font color=red>  28:</font>   for i in xrange(100000):
<font color=red>  29:</font>     s += i
<font color=red>  30:</font>   assert sorted(s.any)== [ 5852, 24193, 28929, 38266,
<font color=red>  31:</font>                           41764, 42926, 51310, 52203,
<font color=red>  32:</font>                           54651, 56743, 59368, 60794,
<font color=red>  33:</font>                           61888, 82586, 83018, 88462]
````
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

````python
<font color=red>  34:</font> weather="""
<font color=red>  35:</font> 
<font color=red>  36:</font> outlook,
<font color=red>  37:</font> temperature,
<font color=red>  38:</font> humidity,?windy,play
<font color=red>  39:</font> sunny    , 85, 85, FALSE, no  # an interesting case
<font color=red>  40:</font> sunny    , 80, 90, TRUE , no
<font color=red>  41:</font> overcast , 83, 86, FALSE, yes
<font color=red>  42:</font> rainy    , 70, 96, FALSE, yes
<font color=red>  43:</font> rainy    , 68, 80, FALSE, yes
<font color=red>  44:</font> rainy    , 65, 70, TRUE , no
<font color=red>  45:</font> overcast , 64, 65, TRUE , 
<font color=red>  46:</font> yes
<font color=red>  47:</font> sunny    , 72, 95, FALSE, no
<font color=red>  48:</font> 
<font color=red>  49:</font> sunny    , 69, 70, FALSE, yes
<font color=red>  50:</font> rainy    , 75, 80, FALSE, yes
<font color=red>  51:</font> sunny    , 75, 70, TRUE , yes
<font color=red>  52:</font> overcast , 72, 90, TRUE , yes
<font color=red>  53:</font> overcast , 81, 75, FALSE, yes
<font color=red>  54:</font> rainy    , 71, 91, TRUE , no"""
<font color=red>  55:</font> 
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

Lets handle all that mess with iterators.

## Support code

### Standard Header

Load some standard tools.

````python
<font color=red>  56:</font> 
<font color=red>  57:</font> class o:
<font color=red>  58:</font>   """Emulate Javascript's uber simple objects.
<font color=red>  59:</font>   Note my convention: I use "`i`" not "`this`."""
<font color=red>  60:</font>   def __init__(i,**d)    : i.__dict__.update(d)
<font color=red>  61:</font>   def __setitem__(i,k,v) : i.__dict__[k] = v
<font color=red>  62:</font>   def __getitem__(i,k)   : return i.__dict__[k]
<font color=red>  63:</font>   def __repr__(i)        : return 'o'+str(i.__dict__)
<font color=red>  64:</font> 
<font color=red>  65:</font> @ok
<font color=red>  66:</font> def _o():
<font color=red>  67:</font>   x = o(name='tim',shoesize=9)
<font color=red>  68:</font>   assert x.name     == 'tim'
<font color=red>  69:</font>   assert x["name"]  == 'tim'
<font color=red>  70:</font>   x.shoesize += 1
<font color=red>  71:</font>   assert x.shoesize == 10
<font color=red>  72:</font>   assert str(x) == "o{'name': 'tim', 'shoesize': 10}"
````
  
### Serious Python JuJu

Tricks to let us read from strings or files or zip files
or anything source at all. 

Not for beginners.

````python
<font color=red>  73:</font> def STRING(str):
<font color=red>  74:</font>   def wrapper():
<font color=red>  75:</font>     for c in str: yield c
<font color=red>  76:</font>   return wrapper
<font color=red>  77:</font> 
<font color=red>  78:</font> def FILE(filename, buffer_size=4096):
<font color=red>  79:</font>   def chunks(filename):
<font color=red>  80:</font>     with open(filename, "rb") as fp:
<font color=red>  81:</font>       chunk = fp.read(buffer_size)
<font color=red>  82:</font>       while chunk:
<font color=red>  83:</font>         yield chunk
<font color=red>  84:</font>         chunk = fp.read(buffer_size)
<font color=red>  85:</font>   def wrapper():
<font color=red>  86:</font>     for chunk in chunks(filename):
<font color=red>  87:</font>       for char in chunk:
<font color=red>  88:</font>         yield char
<font color=red>  89:</font>   return wrapper
````

## Iterators

### Lines

Yield each line in a string

````python
<font color=red>  90:</font> def lines(src):
<font color=red>  91:</font>   tmp=''
<font color=red>  92:</font>   for ch in src(): # sneaky... src can evaluate to different ghings
<font color=red>  93:</font>     if ch == "\n":
<font color=red>  94:</font>       yield tmp
<font color=red>  95:</font>       tmp = ''
<font color=red>  96:</font>     else:
<font color=red>  97:</font>       tmp += ch # for a (slightly) faster method,
<font color=red>  98:</font>                 # in Python3, see http://goo.gl/LvgGx3
<font color=red>  99:</font>   if tmp:
<font color=red> 100:</font>     yield tmp
<font color=red> 101:</font> 
<font color=red> 102:</font> @ok
<font color=red> 103:</font> def _line():
<font color=red> 104:</font>   for line in lines(STRING(weather)):
<font color=red> 105:</font>     print("[",line,"]",sep="")
<font color=red> 106:</font> 
````

### Rows

Yield all non-blank lines,
joining lines that end in ','.

````python
<font color=red> 107:</font> def rows(src):
<font color=red> 108:</font>   b4 = ''
<font color=red> 109:</font>   for line in lines(src):
<font color=red> 110:</font>     line = re.sub(r"[\r\t ]*","",line)
<font color=red> 111:</font>     line = re.sub(r"#.*","",line)
<font color=red> 112:</font>     if not line: continue # skip blanks
<font color=red> 113:</font>     if line[-1] == ',':   # maybe, continue lines
<font color=red> 114:</font>       b4 += line
<font color=red> 115:</font>     else:
<font color=red> 116:</font>       yield b4 + line
<font color=red> 117:</font>       b4 = ''
<font color=red> 118:</font>       
<font color=red> 119:</font> @ok
<font color=red> 120:</font> def _row():
<font color=red> 121:</font>   for row in rows(STRING(weather)):
<font color=red> 122:</font>     print("[",row,"]",sep="")
<font color=red> 123:</font> 
````

### Values

Coerce row values to floats, ints or strings. 
Jump over any cols we are ignoring

````python
<font color=red> 124:</font> def values(src):
<font color=red> 125:</font>   want = None
<font color=red> 126:</font>   for row in rows(src):
<font color=red> 127:</font>     lst  = row.split(',')
<font color=red> 128:</font>     want = want or [col for col in xrange(len(lst))
<font color=red> 129:</font>                     if lst[col][0] != "?" ]
<font color=red> 130:</font>     yield [ make(lst[col]) for col in want ]
````

Helper function.

````python
<font color=red> 131:</font> def make(x):
<font color=red> 132:</font>   try   : return int(x)
<font color=red> 133:</font>   except:
<font color=red> 134:</font>     try   : return float(x)
<font color=red> 135:</font>     except: return x
````

Test function.

````python
<font color=red> 136:</font> @ok
<font color=red> 137:</font> def _values():
<font color=red> 138:</font>   for cells in values(STRING(weather)):
<font color=red> 139:</font>     print(cells)
<font color=red> 140:</font> 
````

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

````python
<font color=red> 141:</font> def table(src, klass= -1, keep= False):
<font color=red> 142:</font>   t = None
<font color=red> 143:</font>   for cells in values(src):
<font color=red> 144:</font>     if t:
<font color=red> 145:</font>       k = cells[klass]
<font color=red> 146:</font>       for cell,some in zip(cells,t.klasses[k]):
<font color=red> 147:</font>         some += cell
<font color=red> 148:</font>       if keep:
<font color=red> 149:</font>         t.rows += [cells]
<font color=red> 150:</font>     else:
<font color=red> 151:</font>      t = o(header = cells,
<font color=red> 152:</font>            rows   = [],
<font color=red> 153:</font>            klasses= Default(lambda: klass0(t.header)))
<font color=red> 154:</font>   return t
````

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

````python
<font color=red> 155:</font> class Default(dict):
<font color=red> 156:</font>   def __init__(i, default): i.default = default
<font color=red> 157:</font>   def __getitem__(i, key):
<font color=red> 158:</font>     if key in i: return i.get(key)
<font color=red> 159:</font>     return i.setdefault(key, i.default())
<font color=red> 160:</font> 
<font color=red> 161:</font> def klass0(header):
<font color=red> 162:</font>  tmp = [Some() for _ in header]
<font color=red> 163:</font>  for n,header1 in enumerate(header):
<font color=red> 164:</font>    tmp[n].pos  = n
<font color=red> 165:</font>    tmp[n].name = header1
<font color=red> 166:</font>  return tmp
````

Test functions: read from strings or files.

````python
<font color=red> 167:</font> @ok
<font color=red> 168:</font> def _tableFromString(src = STRING(weather)):
<font color=red> 169:</font>   t = table(src)
<font color=red> 170:</font>   for k,v in t.klasses.items():
<font color=red> 171:</font>     for some in v:
<font color=red> 172:</font>       print(":klass",k,":name",some.name,":col",some.pos,
<font color=red> 173:</font>             ":seen",some.n,"\n\t:kept",some.any)
<font color=red> 174:</font> 
<font color=red> 175:</font> @ok
<font color=red> 176:</font> def _tableFromFile():
<font color=red> 177:</font>   _tableFromString(FILE("weather.csv"))
````

## Sanity Check

How much do we lose if from some sample `s1` we only keep some of the items in `s2`?
And just to make this interesting, we'll compare this error to what happens
if I sample that distribution twice, once to `s1` and once to `s3`.

For the results of the following code, see the top of this file.

````python
<font color=red> 178:</font> 
<font color=red> 179:</font> def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
<font color=red> 180:</font>   "Return percentiles in a list"
<font color=red> 181:</font>   at  = lambda x: lst[ int(len(lst)*x) ]
<font color=red> 182:</font>   return [ at(tile) for tile in tiles ]
<font color=red> 183:</font>   
<font color=red> 184:</font> def diff(s1,s2):
<font color=red> 185:</font>   "Return difference in the percentiles"
<font color=red> 186:</font>   return [ abs(int(100*(most-less)))
<font color=red> 187:</font>            for most,less in
<font color=red> 188:</font>            zip(ntiles(sorted(s1.any)),
<font color=red> 189:</font>                      ntiles(sorted(s2.any))) ]
<font color=red> 190:</font> 
<font color=red> 191:</font> def samples(m0=128,f=random.random):
<font color=red> 192:</font>   print("\n         \t    diff to all    \t    \t     diff to all")
<font color=red> 193:</font>   print("         \t -------------------\t    \t -------------------")
<font color=red> 194:</font>   print("all kept \t 10% 30% 50% 70% 90%\t kept\t 10% 30% 50% 70% 90%")
<font color=red> 195:</font>   print("--- ---- \t --- --- --- --- ---\t ----\t --- --- --- --- ---")
<font color=red> 196:</font>   m = m0
<font color=red> 197:</font>   for _ in xrange(7):
<font color=red> 198:</font>     m = m * 2
<font color=red> 199:</font>     n = min(m0,m)
<font color=red> 200:</font>     s1,s2,s3 = Some(m), Some(n),Some(m)
<font color=red> 201:</font>     for _ in xrange(m):
<font color=red> 202:</font>       x,y = f(),f()
<font color=red> 203:</font>       s1 += x
<font color=red> 204:</font>       s2 += x
<font color=red> 205:</font>       s3 += y
<font color=red> 206:</font>     print(m,"",n, "\t",diff(s1,s2),"\t",m,"\t",diff(s1,s3))
<font color=red> 207:</font>     
<font color=red> 208:</font> @ok
<font color=red> 209:</font> def _samples():
<font color=red> 210:</font>   rseed(1)
<font color=red> 211:</font>   for x in [64,128,256,512]:
<font color=red> 212:</font>     samples(x)
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

