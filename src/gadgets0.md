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

<a href="gadgets0.py#L66-L111"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   5:   pi  = math.pi
   6:   ee  = math.e
   7:   sin = math.sin
   8:   sqrt= math.sqrt
   9:   r   = random.random
  10:   isa = isinstance
  11:   seed=random.seed
  12:   
  13:   nl = lambda: print("")
  14:   
  15:   def say(*lst):
  16:     sys.stdout.write(', '.join(map(str,lst)))
  17:     sys.stdout.flush()
  18:   
  19:   def printer(i,**d):
  20:      return i.__class__.__name__ + str(o(**d))[1:]
  21:    
  22:   def r3(lst,n=3):
  23:     return map(lambda x:round(x,n),lst)
  24:   
  25:   
  26:   def r2(lst): return r3(lst,2)
  27:   def r5(lst): return r3(lst,5)
  28:   def r7(lst): return r3(lst,7)
  29:   def r10(lst): return r3(lst,10)
  30:   
  31:   
  32:   def shuffle(lst):
  33:     random.shuffle(lst)
  34:     return lst
  35:   
  36:   def ntiles(lst, tiles=None,ordered=True):
  37:     tiles = tiles or the.MISC.tiles
  38:     lst   = lst if ordered else sorted(lst)
  39:     at    = lambda x: lst[ int(len(lst)*x) ]
  40:     return [ at(tile) for tile in tiles ]
  41:   
  42:   def median(lst,ordered=False):
  43:     lst = sorted(lst)
  44:     m = len(lst)
  45:     j = lst[int(m/2)+1]
  46:     if m % 2:
  47:       return j
  48:     else:
  49:       i = lst[int(m/2)]
  50:       return (i+j)/2.1
```

## Some Iterators

<a href="gadgets0.py#L117-L131"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  51:   def item(items):
  52:     "return all items in a nested list"
  53:     if isinstance(items,(list,tuple)):
  54:       for one in items:
  55:         for x in item(one):
  56:           yield x
  57:     else:
  58:       yield items
  59:       
  60:   def pairs(lst):
  61:     "Return all pairs of items i,i+1 from a list."
  62:     last=lst[0]
  63:     for i in lst[1:]:
  64:       yield last,i
  65:       last = i    
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L137-L149"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  66:   def show(x, indent=None, width=None):
  67:     def has(x):
  68:       if isa(x,list): return [has(v) for v in x]
  69:       if isa(x,dict): return {k:has(v) for k,v
  70:                               in x.items()
  71:                               if k[0] != "_"}
  72:       if isa(x,o): return has(x.__dict__)
  73:       if isa(x,float): return '%g' % x
  74:       return x
  75:     print(pprint.pformat(has(x),
  76:               indent= indent or the.MISC.show.indent,
  77:               width = width  or the.MISC.show.width))
  78:   
```

## Javascript struct emulation

<a href="gadgets0.py#L155-L159"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  79:   class o:
  80:     def __init__(i,**d)    : i.__dict__.update(d)
  81:     def __setitem__(i,k,v) : i.__dict__[k] = v
  82:     def __getitem__(i,k)   : return i.__dict__[k]
  83:     def __repr__(i)        : return 'o'+str(i.__dict__)
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

<a href="gadgets0.py#L200-L212"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  84:   the = o()
  85:   
  86:   def setting(f):
  87:     "Decorator. Stores output of function in 'the'."
  88:     name = f.__name__
  89:     def wrapper(**d):
  90:       tmp = f()
  91:       tmp.__dict__.update(d) # maybe do some overrides
  92:       the[name] = tmp  # store the settings in `the`
  93:       return tmp
  94:     wrapper()  # so a side effect of loading the function
  95:                # is to call the function
  96:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L218-L224"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  97:   @setting
  98:   def MISC(): return o(
  99:       seed=1,
 100:       tiles=[0.1 ,0.3,0.5,0.7,0.9],
 101:       marks=["-" ," "," ","-"," "],
 102:       show=o(indent=2,
 103:              width=150))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

  
<a href="gadgets0.py#L240-L267"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 104:   def use(x,**y):
 105:     """Convenience function: for temporarily 
 106:        overwriting defaults."""
 107:     return (x,y)
 108:   
 109:   @contextmanager
 110:   def study(what,*usings,**flags):
 111:     """Maybe change settings. Always call 
 112:        seed(). Afterwards, set  settings back 
 113:        to defaults."""
 114:     loud = flags.get("verbose",True)
 115:     loud and print(
 116:           "\n# " + "-" * 50,                 # before
 117:           "\n# ", what, "\n#",               # before
 118:           datetime.datetime.now().strftime(  # before
 119:             "%Y-%m-%d %H:%M:%S"))            # before
 120:     for (using, override) in usings:         # before
 121:       using(**override)                      # before: make new settings
 122:     seed()                                   # before: reset seed
 123:     t1 = time.time()                         # before
 124:     loud and show(the)                       # before
 125:     loud and print("")                       # before
 126:     yield                                      
 127:     t2 = time.time()                         # after
 128:     loud and print("\n# " + "-" * 50)        # after
 129:     loud and print("# Runtime: %.3f secs\n" % (t2-t1))# after  : print runtime
 130:     for (using,_) in usings:                 # after  : reset settings
 131:       using()                                # after
```

<a href="gadgets0.py#L271-L302"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 132:   
 133:   def xtile(lst,lo=0,hi=100,width=50, 
 134:                chops=None,
 135:                marks=None,
 136:                bar="|",star="*",show=" %3.0f"):
 137:     """The function _xtile_ takes a list of (possibly)
 138:     unsorted numbers and presents them as a horizontal
 139:     xtile chart (in ascii format). The default is a 
 140:     contracted _quintile_ that shows the 
 141:     10,30,50,70,90 breaks in the data (but this can be 
 142:     changed- see the optional flags of the function).
 143:     """
 144:     chops = chops or the.MISC.tiles
 145:     marks = marks or the.MISC.marks
 146:     def pos(p)   : return ordered[int(len(lst)*p)]
 147:     def place(x) : 
 148:       return int(width*float((x - lo))/(hi - lo))
 149:     def pretty(lst) : 
 150:       return ', '.join([show % x for x in lst])
 151:     ordered = sorted(lst)
 152:     lo      = min(lo,ordered[0])
 153:     hi      = max(hi,ordered[-1])
 154:     what    = [pos(p)   for p in chops]
 155:     where   = [place(n) for n in  what]
 156:     out     = [" "] * width
 157:     for one,two in pairs(where):
 158:       for i in range(one,two): 
 159:         out[i] = marks[0]
 160:       marks = marks[1:]
 161:     out[int(width/2)]    = bar
 162:     out[place(pos(0.5))] = star 
 163:     return ''.join(out) +  "," +  pretty(what)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

