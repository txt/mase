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
   print(x)
print("lift off!")
```

And here's my favorite iterator that descends recursive lists:

<a href="abstract.py#L57-L63"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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

<a href="abstract.py#L115-L140"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

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

<a href="abstract.py#L202-L223"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

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

<a href="abstract.py#L246-L261"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  56:   class o:
  57:     """Emulate Javascript's uber simple objects.
  58:     Note my convention: I use "`i`" not "`this`."""
  59:     def __init__(i,**d)    : i.__dict__.update(d)
  60:     def __setitem__(i,k,v) : i.__dict__[k] = v
  61:     def __getitem__(i,k)   : return i.__dict__[k]
  62:     def __repr__(i)        : return 'o'+str(i.__dict__)
  63:   
  64:   @ok
  65:   def _o():
  66:     x = o(name='tim',shoesize=9)
  67:     assert x.name     == 'tim'
  68:     assert x["name"]  == 'tim'
  69:     x.shoesize += 1
  70:     assert x.shoesize == 10
  71:     assert str(x) == "o{'name': 'tim', 'shoesize': 10}"
```
  
### Serious Python JuJu

Tricks to let us read from strings or files or zip files
or anything source at all. 

Not for beginners.

<a href="abstract.py#L272-L288"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  72:   def STRING(str):
  73:     def wrapper():
  74:       for c in str: yield c
  75:     return wrapper
  76:   
  77:   def FILE(filename, buffer_size=4096):
  78:     def chunks(filename):
  79:       with open(filename, "rb") as fp:
  80:         chunk = fp.read(buffer_size)
  81:         while chunk:
  82:           yield chunk
  83:           chunk = fp.read(buffer_size)
  84:     def wrapper():
  85:       for chunk in chunks(filename):
  86:         for char in chunk:
  87:           yield char
  88:     return wrapper
```

## Iterators

### Lines

Yield each line in a string

<a href="abstract.py#L298-L313"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  89:   def lines(src):
  90:     tmp=''
  91:     for ch in src(): # sneaky... src can evaluate to different ghings
  92:       if ch == "\n":
  93:         yield tmp
  94:         tmp = ''
  95:       else:
  96:         tmp += ch # for a (slightly) faster method,
  97:                   # in Python3, see http://goo.gl/LvgGx3
  98:     if tmp:
  99:       yield tmp
 100:   
 101:   @ok
 102:   def _line():
 103:     for line in lines(STRING(weather)):
 104:       print("[",line,"]",sep="")
```

### Rows

Yield all non-blank lines,
joining lines that end in ','.

<a href="abstract.py#L322-L338"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 105:   def rows(src):
 106:     b4 = ''
 107:     for line in lines(src):
 108:       line = re.sub(r"[\r\t ]*","",line)
 109:       line = re.sub(r"#.*","",line)
 110:       if not line: continue # skip blanks
 111:       if line[-1] == ',':   # maybe, continue lines
 112:         b4 += line
 113:       else:
 114:         yield b4 + line
 115:         b4 = ''
 116:         
 117:   @ok
 118:   def _row():
 119:     for row in rows(STRING(weather)):
 120:       print("[",row,"]",sep="")
 121:   
```

### Values

Coerce row values to floats, ints or strings. 
Jump over any cols we are ignoring

<a href="abstract.py#L347-L353"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 122:   def values(src):
 123:     want = None
 124:     for row in rows(src):
 125:       lst  = row.split(',')
 126:       want = want or [col for col in xrange(len(lst))
 127:                       if lst[col][0] != "?" ]
 128:       yield [ make(lst[col]) for col in want ]
```

Helper function.

<a href="abstract.py#L359-L363"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 129:   def make(x):
 130:     try   : return int(x)
 131:     except:
 132:       try   : return float(x)
 133:       except: return x
```

Test function.

<a href="abstract.py#L369-L372"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 134:   @ok
 135:   def _values():
 136:     for cells in values(STRING(weather)):
 137:       print(cells)
```

## Tables

Finally!

Tables keep `Some` values for each column in a string.
Assumes that the string contains a `klass` column
and keeps separate counts for each `klass`.

<a href="abstract.py#L384-L399"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 138:   def table(src, klass= -1, keep= False):
 139:     t = None
 140:     for cells in values(src):
 141:       if t:
 142:         k = cells[klass]
 143:         for cell,some,all in zip(cells,t.klasses[k],t.all):
 144:           some += cell
 145:           all  += cell
 146:         if keep:
 147:           t.rows += [cells]
 148:       else:
 149:        t = o(header = cells,
 150:              rows   = [],
 151:              all    = klass0(cells),
 152:              klasses= Default(lambda: klass0(t.header)))
 153:     return t
```

Helper functions:

+ If we reach for a klass information and we have not
  seen that klass before, create a list of `Some` counters
  (one for each column).

<a href="abstract.py#L409-L420"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 154:   class Default(dict):
 155:     def __init__(i, default): i.default = default
 156:     def __getitem__(i, key):
 157:       if key in i: return i.get(key)
 158:       return i.setdefault(key, i.default())
 159:   
 160:   def klass0(header):
 161:    tmp = [Some() for _ in header]
 162:    for n,header1 in enumerate(header):
 163:      tmp[n].pos  = n
 164:      tmp[n].name = header1
 165:    return tmp
```

Test functions: read from strings or files.

<a href="abstract.py#L426-L436"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 166:   @ok
 167:   def _tableFromString(src = STRING(weather)):
 168:     t = table(src)
 169:     for k,v in t.klasses.items():
 170:       for some in v:
 171:         print(":klass",k,":name",some.name,":col",some.pos,
 172:               ":seen",some.n,"\n\t:kept",some.any)
 173:   
 174:   @ok
 175:   def _tableFromFile():
 176:     _tableFromString(FILE("weather.csv"))
```

## Sanity Check

How much do we lose if from some sample `s1` we only keep some of the items in `s2`?
And just to make this interesting, we'll compare this error to what happens
if I sample that distribution twice, once to `s1` and once to `s3`.

For the results of the following code, see the top of this file.

<a href="abstract.py#L448-L481"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 177:   def samples(m0=128,f=random.random):
 178:     print("\n         \t    diff to all    \t    \t     diff to all")
 179:     print("         \t -------------------\t    \t -------------------")
 180:     print("all kept \t 10% 30% 50% 70% 90%\t kept\t 10% 30% 50% 70% 90%")
 181:     print("--- ---- \t --- --- --- --- ---\t ----\t --- --- --- --- ---")
 182:     m = m0
 183:     for _ in xrange(7):
 184:       m = m * 2
 185:       n = min(m0,m)
 186:       s1,s2,s3 = Some(m), Some(n),Some(m)
 187:       for _ in xrange(m):
 188:         x,y = f(),f()
 189:         s1 += x
 190:         s2 += x
 191:         s3 += y
 192:       print(m,"",n, "\t",diff(s1,s2),"\t",m,"\t",diff(s1,s3))
 193:   
 194:   def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
 195:     "Return percentiles in a list"
 196:     at  = lambda x: lst[ int(len(lst)*x) ]
 197:     return [ at(tile) for tile in tiles ]
 198:     
 199:   def diff(s1,s2):
 200:     "Return difference in the percentiles"
 201:     return [ abs(int(100*(most-less)))
 202:              for most,less in
 203:              zip(ntiles(sorted(s1.any)),
 204:                        ntiles(sorted(s2.any))) ]
 205:   
 206:   @ok
 207:   def _samples():
 208:     rseed(1)
 209:     for x in [64,128,256,512]:
 210:       samples(x)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

