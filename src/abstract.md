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
   1:   def items(x, depth=-1):
   2:     if isinstance(x,(list,tuple)):
   3:       for y in x:
   4:         for z in items(y, depth+1):
   5:           yield z
   6:     else:
   7:       yield depth,x
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
   8:   r = random.random
   9:   rseed = random.seed
  10:   
  11:   class Some:
  12:     def __init__(i, max=8): # note, usually 256 or 128 or 64 (if brave)
  13:       i.n, i.any, i.max = 0,[],max
  14:     def __iadd__(i,x):
  15:       i.n += 1
  16:       now = len(i.any)
  17:       if now < i.max:    # not full yet, so just keep it   
  18:         i.any += [x]
  19:       elif r() <= now/i.n:
  20:         i.any[ int(r() * now) ]= x # zap some older value
  21:       #else: forget x
  22:       return i
  23:   
  24:   @ok
  25:   def _some():
  26:     rseed(1)
  27:     s = Some(16)
  28:     for i in xrange(100000):
  29:       s += i
  30:     assert sorted(s.any)== [ 5852, 24193, 28929, 38266,
  31:                             41764, 42926, 51310, 52203,
  32:                             54651, 56743, 59368, 60794,
  33:                             61888, 82586, 83018, 88462]
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
  34:   weather="""
  35:   
  36:   outlook,
  37:   temperature,
  38:   humidity,?windy,play
  39:   sunny    , 85, 85, FALSE, no  # an interesting case
  40:   sunny    , 80, 90, TRUE , no
  41:   overcast , 83, 86, FALSE, yes
  42:   rainy    , 70, 96, FALSE, yes
  43:   rainy    , 68, 80, FALSE, yes
  44:   rainy    , 65, 70, TRUE , no
  45:   overcast , 64, 65, TRUE , 
  46:   yes
  47:   sunny    , 72, 95, FALSE, no
  48:   
  49:   sunny    , 69, 70, FALSE, yes
  50:   rainy    , 75, 80, FALSE, yes
  51:   sunny    , 75, 70, TRUE , yes
  52:   overcast , 72, 90, TRUE , yes
  53:   overcast , 81, 75, FALSE, yes
  54:   rainy    , 71, 91, TRUE , no"""
  55:   
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
  56:   
  57:   class o:
  58:     """Emulate Javascript's uber simple objects.
  59:     Note my convention: I use "`i`" not "`this`."""
  60:     def __init__(i,**d)    : i.__dict__.update(d)
  61:     def __setitem__(i,k,v) : i.__dict__[k] = v
  62:     def __getitem__(i,k)   : return i.__dict__[k]
  63:     def __repr__(i)        : return 'o'+str(i.__dict__)
  64:   
  65:   @ok
  66:   def _o():
  67:     x = o(name='tim',shoesize=9)
  68:     assert x.name     == 'tim'
  69:     assert x["name"]  == 'tim'
  70:     x.shoesize += 1
  71:     assert x.shoesize == 10
  72:     assert str(x) == "o{'name': 'tim', 'shoesize': 10}"
````
  
### Serious Python JuJu

Tricks to let us read from strings or files or zip files
or anything source at all. 

Not for beginners.

````python
  73:   def STRING(str):
  74:     def wrapper():
  75:       for c in str: yield c
  76:     return wrapper
  77:   
  78:   def FILE(filename, buffer_size=4096):
  79:     def chunks(filename):
  80:       with open(filename, "rb") as fp:
  81:         chunk = fp.read(buffer_size)
  82:         while chunk:
  83:           yield chunk
  84:           chunk = fp.read(buffer_size)
  85:     def wrapper():
  86:       for chunk in chunks(filename):
  87:         for char in chunk:
  88:           yield char
  89:     return wrapper
````

## Iterators

### Lines

Yield each line in a string

````python
  90:   def lines(src):
  91:     tmp=''
  92:     for ch in src(): # sneaky... src can evaluate to different ghings
  93:       if ch == "\n":
  94:         yield tmp
  95:         tmp = ''
  96:       else:
  97:         tmp += ch # for a (slightly) faster method,
  98:                   # in Python3, see http://goo.gl/LvgGx3
  99:     if tmp:
 100:       yield tmp
 101:   
 102:   @ok
 103:   def _line():
 104:     for line in lines(STRING(weather)):
 105:       print("[",line,"]",sep="")
 106:   
````

### Rows

Yield all non-blank lines,
joining lines that end in ','.

````python
 107:   def rows(src):
 108:     b4 = ''
 109:     for line in lines(src):
 110:       line = re.sub(r"[\r\t ]*","",line)
 111:       line = re.sub(r"#.*","",line)
 112:       if not line: continue # skip blanks
 113:       if line[-1] == ',':   # maybe, continue lines
 114:         b4 += line
 115:       else:
 116:         yield b4 + line
 117:         b4 = ''
 118:         
 119:   @ok
 120:   def _row():
 121:     for row in rows(STRING(weather)):
 122:       print("[",row,"]",sep="")
 123:   
````

### Values

Coerce row values to floats, ints or strings. 
Jump over any cols we are ignoring

````python
 124:   def values(src):
 125:     want = None
 126:     for row in rows(src):
 127:       lst  = row.split(',')
 128:       want = want or [col for col in xrange(len(lst))
 129:                       if lst[col][0] != "?" ]
 130:       yield [ make(lst[col]) for col in want ]
````

Helper function.

````python
 131:   def make(x):
 132:     try   : return int(x)
 133:     except:
 134:       try   : return float(x)
 135:       except: return x
````

Test function.

````python
 136:   @ok
 137:   def _values():
 138:     for cells in values(STRING(weather)):
 139:       print(cells)
 140:   
````

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

````python
 141:   def table(src, klass= -1, keep= False):
 142:     t = None
 143:     for cells in values(src):
 144:       if t:
 145:         k = cells[klass]
 146:         for cell,some in zip(cells,t.klasses[k]):
 147:           some += cell
 148:         if keep:
 149:           t.rows += [cells]
 150:       else:
 151:        t = o(header = cells,
 152:              rows   = [],
 153:              klasses= Default(lambda: klass0(t.header)))
 154:     return t
````

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

````python
 155:   class Default(dict):
 156:     def __init__(i, default): i.default = default
 157:     def __getitem__(i, key):
 158:       if key in i: return i.get(key)
 159:       return i.setdefault(key, i.default())
 160:   
 161:   def klass0(header):
 162:    tmp = [Some() for _ in header]
 163:    for n,header1 in enumerate(header):
 164:      tmp[n].pos  = n
 165:      tmp[n].name = header1
 166:    return tmp
````

Test functions: read from strings or files.

````python
 167:   @ok
 168:   def _tableFromString(src = STRING(weather)):
 169:     t = table(src)
 170:     for k,v in t.klasses.items():
 171:       for some in v:
 172:         print(":klass",k,":name",some.name,":col",some.pos,
 173:               ":seen",some.n,"\n\t:kept",some.any)
 174:   
 175:   @ok
 176:   def _tableFromFile():
 177:     _tableFromString(FILE("weather.csv"))
````

## Sanity Check

How much do we lose if from some sample `s1` we only keep some of the items in `s2`?
And just to make this interesting, we'll compare this error to what happens
if I sample that distribution twice, once to `s1` and once to `s3`.

For the results of the following code, see the top of this file.

````python
 178:   
 179:   def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
 180:     "Return percentiles in a list"
 181:     at  = lambda x: lst[ int(len(lst)*x) ]
 182:     return [ at(tile) for tile in tiles ]
 183:     
 184:   def diff(s1,s2):
 185:     "Return difference in the percentiles"
 186:     return [ abs(int(100*(most-less)))
 187:              for most,less in
 188:              zip(ntiles(sorted(s1.any)),
 189:                        ntiles(sorted(s2.any))) ]
 190:   
 191:   def samples(m0=128,f=random.random):
 192:     print("\n         \t    diff to all    \t    \t     diff to all")
 193:     print("         \t -------------------\t    \t -------------------")
 194:     print("all kept \t 10% 30% 50% 70% 90%\t kept\t 10% 30% 50% 70% 90%")
 195:     print("--- ---- \t --- --- --- --- ---\t ----\t --- --- --- --- ---")
 196:     m = m0
 197:     for _ in xrange(7):
 198:       m = m * 2
 199:       n = min(m0,m)
 200:       s1,s2,s3 = Some(m), Some(n),Some(m)
 201:       for _ in xrange(m):
 202:         x,y = f(),f()
 203:         s1 += x
 204:         s2 += x
 205:         s3 += y
 206:       print(m,"",n, "\t",diff(s1,s2),"\t",m,"\t",diff(s1,s3))
 207:       
 208:   @ok
 209:   def _samples():
 210:     rseed(1)
 211:     for x in [64,128,256,512]:
 212:       samples(x)
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

