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

<a href="gadgets0.py#L66-L104"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
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
  43:     
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L110-L122"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  44:   def show(x, indent=None, width=None):
  45:     def has(x):
  46:       if isa(x,list): return [has(v) for v in x]
  47:       if isa(x,dict): return {k:has(v) for k,v
  48:                               in x.items()
  49:                               if k[0] != "_"}
  50:       if isa(x,o): return has(x.__dict__)
  51:       if isa(x,float): return '%g' % x
  52:       return x
  53:     print(pprint.pformat(has(x),
  54:               indent= indent or the.MISC.show.indent,
  55:               width = width  or the.MISC.show.width))
  56:   
```

## Javascript struct emulation

<a href="gadgets0.py#L128-L132"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  57:   class o:
  58:     def __init__(i,**d)    : i.__dict__.update(d)
  59:     def __setitem__(i,k,v) : i.__dict__[k] = v
  60:     def __getitem__(i,k)   : return i.__dict__[k]
  61:     def __repr__(i)        : return 'o'+str(i.__dict__)
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

<a href="gadgets0.py#L173-L185"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  62:   the = o()
  63:   
  64:   def setting(f):
  65:     "Decorator. Stores output of function in 'the'."
  66:     name = f.__name__
  67:     def wrapper(**d):
  68:       tmp = f()
  69:       tmp.__dict__.update(d) # maybe do some overrides
  70:       the[name] = tmp  # store the settings in `the`
  71:       return tmp
  72:     wrapper()  # so a side effect of loading the function
  73:                # is to call the function
  74:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L191-L196"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  75:   @setting
  76:   def MISC(): return o(
  77:       seed=1,
  78:       tiles=[0.1,0.3,0.5,0.7,0.9],
  79:       show=o(indent=2,
  80:              width=50))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

  
<a href="gadgets0.py#L212-L237"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  81:   def use(x,**y):
  82:     """Convenience function: for temporarily 
  83:        overwriting defaults."""
  84:     return (x,y)
  85:   
  86:   @contextmanager
  87:   def study(what,*usings):
  88:     """Maybe change settings. Always call 
  89:        seed(). Afterwards, set  settings back 
  90:        to defaults."""
  91:     print("\n# " + "-" * 50,                 # before
  92:           "\n# ", what, "\n#",               # before
  93:           datetime.datetime.now().strftime(  # before
  94:             "%Y-%m-%d %H:%M:%S"))            # before
  95:     for (using, override) in usings:         # before
  96:       using(**override)                      # before: make new settings
  97:     seed()                                   # before: reset seed
  98:     t1 = time.time()                         # before
  99:     show(the)                                # before
 100:     print("")                                # before
 101:     yield                                      
 102:     t2 = time.time()                         # after
 103:     print("\n# " + "-" * 50)                 # after
 104:     print("# Runtime: %.3f secs\n" % (t2-t1))# after  : print runtime
 105:     for (using,_) in usings:                 # after  : reset settings
 106:       using()                                # after
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

