[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Standard support utils

## The usual suspects

<a href="gadgets0.py#L57-L60"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from contextlib import contextmanager
   2:   import pprint,datetime,time
   3:   import random,math
   4:   from ok import *
```

## Some one(ish) liners.

<a href="gadgets0.py#L66-L103"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   5:   pi  = math.pi
   6:   ee  = math.e
   7:   sin = math.sin
   8:   sqrt= math.sqrt
   9:   r   = random.random
  10:   isa = isinstance
  11:   
  12:   def say(*lst):
  13:     sys.stdout.write(', '.join(map(str,lst)))
  14:     sys.stdout.flush()
  15:     
  16:   def r3(lst,n=3):
  17:     return map(lambda x:round(x,n),lst)
  18:   
  19:   def r5(lst): return r3(lst,5)
  20:   
  21:   def seed(x=None):
  22:     random.seed(x or the.MISC.seed)
  23:   
  24:   def shuffle(lst):
  25:     random.shuffle(lst)
  26:     return lst
  27:   
  28:   def ntiles(lst, tiles=None,ordered=True):
  29:     tiles = tiles or the.MISC.tiles
  30:     lst   = lst if ordered else sorted(lst)
  31:     at    = lambda x: lst[ int(len(lst)*x) ]
  32:     return [ at(tile) for tile in tiles ]
  33:   
  34:   def median(lst,ordered=False):
  35:     lst = sorted(lst)
  36:     m = len(lst)
  37:     j = lst[int(m/2)+1]
  38:     if m % 2:
  39:       return j
  40:     else:
  41:       i = lst[int(m/2)]
  42:       return (i+j)/2.1
```

## Some Iterators

<a href="gadgets0.py#L109-L123"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  43:   def item(items):
  44:     "return all items in a nested list"
  45:     if isinstance(items,(list,tuple)):
  46:       for one in items:
  47:         for x in item(one):
  48:           yield x
  49:     else:
  50:       yield items
  51:       
  52:   def pairs(lst):
  53:     "Return all pairs of items i,i+1 from a list."
  54:     last=lst[0]
  55:     for i in lst[1:]:
  56:       yield last,i
  57:       last = i    
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L129-L141"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  58:   def show(x, indent=None, width=None):
  59:     def has(x):
  60:       if isa(x,list): return [has(v) for v in x]
  61:       if isa(x,dict): return {k:has(v) for k,v
  62:                               in x.items()
  63:                               if k[0] != "_"}
  64:       if isa(x,o): return has(x.__dict__)
  65:       if isa(x,float): return '%g' % x
  66:       return x
  67:     print(pprint.pformat(has(x),
  68:               indent= indent or the.MISC.show.indent,
  69:               width = width  or the.MISC.show.width))
  70:   
```

## Javascript struct emulation

<a href="gadgets0.py#L147-L151"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  71:   class o:
  72:     def __init__(i,**d)    : i.__dict__.update(d)
  73:     def __setitem__(i,k,v) : i.__dict__[k] = v
  74:     def __getitem__(i,k)   : return i.__dict__[k]
  75:     def __repr__(i)        : return 'o'+str(i.__dict__)
```

## Magic constants

A place to store all the magic params, and reset
them after some study.

That place has the following properties:

+ Magic constants do not become 1000 global variables:
  + All such constants are nested inside one global called `the`.
+ It is all stored in one central place (so we
  can print all the current constants);
  + This code stores everything in a magic place called `the`.
+ That place can be updated from all over the code base
  (so the specification of those constants can be
  distributed over to near the code that actually uses them);
  + This code defines a decorator that wraps any function
    that defines a settings.
  + E.g. see `MISC`, below.
+ Using the `study`
  function, defined below, it is possible to:
   + Temporarily override those values;
   + Then reset all those values back to
     some defaults.

The code assumes that settings are set via some method:

```python
def theseSettings(**overrides):
  d1 = theSettings()
  d1.update(overrides)
  the.theseSettings = d1
```

This is a common enough pattern that I auto-create the above
using a decorator around a function that returns
a dictionary.

<a href="gadgets0.py#L192-L204"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  76:   the = o()
  77:   
  78:   def setting(f):
  79:     "Decorator. Stores output of function in 'the'."
  80:     name = f.__name__
  81:     def wrapper(**d):
  82:       tmp = f()
  83:       tmp.__dict__.update(d) # maybe do some overrides
  84:       the[name] = tmp  # store the settings in `the`
  85:       return tmp
  86:     wrapper()  # so a side effect of loading the function
  87:                # is to call the function
  88:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L210-L216"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  89:   @setting
  90:   def MISC(): return o(
  91:       seed=1,
  92:       tiles=[0.1 ,0.3,0.5,0.7,0.9],
  93:       marks=["-" ," "," ","-"," "],
  94:       show=o(indent=2,
  95:              width=50))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

  
<a href="gadgets0.py#L232-L257"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  96:   def use(x,**y):
  97:     """Convenience function: for temporarily 
  98:        overwriting defaults."""
  99:     return (x,y)
 100:   
 101:   @contextmanager
 102:   def study(what,*usings):
 103:     """Maybe change settings. Always call 
 104:        seed(). Afterwards, set  settings back 
 105:        to defaults."""
 106:     print("\n# " + "-" * 50,                 # before
 107:           "\n# ", what, "\n#",               # before
 108:           datetime.datetime.now().strftime(  # before
 109:             "%Y-%m-%d %H:%M:%S"))            # before
 110:     for (using, override) in usings:         # before
 111:       using(**override)                      # before: make new settings
 112:     seed()                                   # before: reset seed
 113:     t1 = time.time()                         # before
 114:     show(the)                                # before
 115:     print("")                                # before
 116:     yield                                      
 117:     t2 = time.time()                         # after
 118:     print("\n# " + "-" * 50)                 # after
 119:     print("# Runtime: %.3f secs\n" % (t2-t1))# after  : print runtime
 120:     for (using,_) in usings:                 # after  : reset settings
 121:       using()                                # after
```

<a href="gadgets0.py#L261-L292"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 122:   
 123:   def xtile(lst,lo=0,hi=100,width=50, 
 124:                chops=None,
 125:                marks=None,
 126:                bar="|",star="*",show=" %3.0f"):
 127:     """The function _xtile_ takes a list of (possibly)
 128:     unsorted numbers and presents them as a horizontal
 129:     xtile chart (in ascii format). The default is a 
 130:     contracted _quintile_ that shows the 
 131:     10,30,50,70,90 breaks in the data (but this can be 
 132:     changed- see the optional flags of the function).
 133:     """
 134:     chops = chops or the.MISC.tiles
 135:     marks = marks or the.MISC.marks
 136:     def pos(p)   : return ordered[int(len(lst)*p)]
 137:     def place(x) : 
 138:       return int(width*float((x - lo))/(hi - lo))
 139:     def pretty(lst) : 
 140:       return ', '.join([show % x for x in lst])
 141:     ordered = sorted(lst)
 142:     lo      = min(lo,ordered[0])
 143:     hi      = max(hi,ordered[-1])
 144:     what    = [pos(p)   for p in chops]
 145:     where   = [place(n) for n in  what]
 146:     out     = [" "] * width
 147:     for one,two in pairs(where):
 148:       for i in range(one,two): 
 149:         out[i] = marks[0]
 150:       marks = marks[1:]
 151:     out[int(width/2)]    = bar
 152:     out[place(pos(0.5))] = star 
 153:     return ''.join(out) +  "," +  pretty(what)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

