[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Standard support utils

## The usual suspects

<a href="gadgets0.py#L58-L61"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from contextlib import contextmanager
   2:   import pprint,datetime,time
   3:   import random,math
   4:   from ok import *
```

## Some one(ish) liners.

<a href="gadgets0.py#L67-L114"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   5:   pi  = math.pi
   6:   ee  = math.e
   7:   sin = math.sin
   8:   sqrt= math.sqrt
   9:   r   = random.random
  10:   isa = isinstance
  11:   nl = lambda: print("")
  12:   
  13:   def seed(s=None):
  14:     if s == None: s = the.MISC.seed
  15:     random.seed(s)
  16:   
  17:   def say(*lst):
  18:     sys.stdout.write(', '.join(map(str,lst)))
  19:     sys.stdout.flush()
  20:   
  21:   def printer(i,**d):
  22:      return i.__class__.__name__ + str(o(**d))[1:]
  23:    
  24:   def r3(lst,n=3):
  25:     return map(lambda x:round(x,n),lst)
  26:   
  27:   
  28:   def r2(lst): return r3(lst,2)
  29:   def r5(lst): return r3(lst,5)
  30:   def r7(lst): return r3(lst,7)
  31:   def r10(lst): return r3(lst,10)
  32:   
  33:   
  34:   def shuffle(lst):
  35:     random.shuffle(lst)
  36:     return lst
  37:   
  38:   def ntiles(lst, tiles=None,ordered=True):
  39:     tiles = tiles or the.MISC.tiles
  40:     lst   = lst if ordered else sorted(lst)
  41:     at    = lambda x: lst[ int(len(lst)*x) ]
  42:     return [ at(tile) for tile in tiles ]
  43:   
  44:   def median(lst,ordered=False):
  45:     lst = sorted(lst)
  46:     m = len(lst)
  47:     j = lst[int(m/2)+1]
  48:     if m % 2:
  49:       return j
  50:     else:
  51:       i = lst[int(m/2)]
  52:       return (i+j)/2.1
```

## Some Iterators

<a href="gadgets0.py#L120-L134"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  53:   def item(items):
  54:     "return all items in a nested list"
  55:     if isinstance(items,(list,tuple)):
  56:       for one in items:
  57:         for x in item(one):
  58:           yield x
  59:     else:
  60:       yield items
  61:       
  62:   def pairs(lst):
  63:     "Return all pairs of items i,i+1 from a list."
  64:     last=lst[0]
  65:     for i in lst[1:]:
  66:       yield last,i
  67:       last = i    
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L140-L152"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  68:   def show(x, indent=None, width=None):
  69:     def has(x):
  70:       if isa(x,list): return [has(v) for v in x]
  71:       if isa(x,dict): return {k:has(v) for k,v
  72:                               in x.items()
  73:                               if k[0] != "_"}
  74:       if isa(x,o): return has(x.__dict__)
  75:       if isa(x,float): return '%g' % x
  76:       return x
  77:     print(pprint.pformat(has(x),
  78:               indent= indent or the.MISC.show.indent,
  79:               width = width  or the.MISC.show.width))
  80:   
```

## Javascript struct emulation

<a href="gadgets0.py#L158-L162"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  81:   class o:
  82:     def __init__(i,**d)    : i.__dict__.update(d)
  83:     def __setitem__(i,k,v) : i.__dict__[k] = v
  84:     def __getitem__(i,k)   : return i.__dict__[k]
  85:     def __repr__(i)        : return 'o'+str(i.__dict__)
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

<a href="gadgets0.py#L203-L215"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  86:   the = o()
  87:   
  88:   def setting(f):
  89:     "Decorator. Stores output of function in 'the'."
  90:     name = f.__name__
  91:     def wrapper(**d):
  92:       tmp = f()
  93:       tmp.__dict__.update(d) # maybe do some overrides
  94:       the[name] = tmp  # store the settings in `the`
  95:       return tmp
  96:     wrapper()  # so a side effect of loading the function
  97:                # is to call the function
  98:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L221-L227"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  99:   @setting
 100:   def MISC(): return o(
 101:       seed=1,
 102:       tiles=[0.1 ,0.3,0.5,0.7,0.9],
 103:       marks=["-" ," "," ","-"," "],
 104:       show=o(indent=2,
 105:              width=150))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

  
<a href="gadgets0.py#L243-L270"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 106:   def use(x,**y):
 107:     """Convenience function: for temporarily 
 108:        overwriting defaults."""
 109:     return (x,y)
 110:   
 111:   @contextmanager
 112:   def study(what,*usings,**flags):
 113:     """Maybe change settings. Always call 
 114:        seed(). Afterwards, set  settings back 
 115:        to defaults."""
 116:     loud = flags.get("verbose",True)
 117:     loud and print(
 118:           "\n# " + "-" * 50,                 # before
 119:           "\n# ", what, "\n#",               # before
 120:           datetime.datetime.now().strftime(  # before
 121:             "%Y-%m-%d %H:%M:%S"))            # before
 122:     for (using, override) in usings:         # before
 123:       using(**override)                      # before: make new settings
 124:     seed()                                   # before: reset seed
 125:     t1 = time.time()                         # before
 126:     loud and show(the)                       # before
 127:     loud and print("")                       # before
 128:     yield                                      
 129:     t2 = time.time()                         # after
 130:     loud and print("\n# " + "-" * 50)        # after
 131:     loud and print("# Runtime: %.3f secs\n" % (t2-t1))# after  : print runtime
 132:     for (using,_) in usings:                 # after  : reset settings
 133:       using()                                # after
```

<a href="gadgets0.py#L274-L305"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

 134:   
 135:   def xtile(lst,lo=0,hi=100,width=50, 
 136:                chops=None,
 137:                marks=None,
 138:                bar="|",star="*",show=" %3.0f"):
 139:     """The function _xtile_ takes a list of (possibly)
 140:     unsorted numbers and presents them as a horizontal
 141:     xtile chart (in ascii format). The default is a 
 142:     contracted _quintile_ that shows the 
 143:     10,30,50,70,90 breaks in the data (but this can be 
 144:     changed- see the optional flags of the function).
 145:     """
 146:     chops = chops or the.MISC.tiles
 147:     marks = marks or the.MISC.marks
 148:     def pos(p)   : return ordered[int(len(lst)*p)]
 149:     def place(x) : 
 150:       return int(width*float((x - lo))/(hi - lo))
 151:     def pretty(lst) : 
 152:       return ', '.join([show % x for x in lst])
 153:     ordered = sorted(lst)
 154:     lo      = min(lo,ordered[0])
 155:     hi      = max(hi,ordered[-1])
 156:     what    = [pos(p)   for p in chops]
 157:     where   = [place(n) for n in  what]
 158:     out     = [" "] * width
 159:     for one,two in pairs(where):
 160:       for i in range(one,two): 
 161:         out[i] = marks[0]
 162:       marks = marks[1:]
 163:     out[int(width/2)]    = bar
 164:     out[place(pos(0.5))] = star 
 165:     return ''.join(out) +  "," +  pretty(what)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

