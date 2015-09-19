[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Standard support utils

## The usual suspects

<a href="gadgets0.py#L12-L15"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from contextlib import contextmanager
   2:   import pprint,datetime,time
   3:   import random,math
   4:   from ok import *
```

## Some one liners.

<a href="gadgets0.py#L21-L44"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   5:   pi  = math.pi
   6:   ee  = math.e
   7:   sin = math.sin
   8:   sqrt= math.sqrt
   9:   r   = random.random
  10:   isa = isinstance
  11:   
  12:   def r3(lst,n=3):
  13:     return map(lambda x:round(x,n),lst)
  14:   
  15:   def r5(lst): return r3(lst,5)
  16:   
  17:   def seed(x=None):
  18:     random.seed(x or the.MISC.seed)
  19:   
  20:   def shuffle(lst):
  21:     random.shuffle(lst)
  22:     return lst
  23:   
  24:   def ntiles(lst, tiles=None,ordered=True):
  25:     tiles = tiles or the.MISC.tiles
  26:     lst   = lst if ordered else sorted(lst)
  27:     at    = lambda x: lst[ int(len(lst)*x) ]
  28:     return [ at(tile) for tile in tiles ]
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L50-L62"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  29:   def show(x, indent=None, width=None):
  30:     def has(x):
  31:       if isa(x,list): return [has(v) for v in x]
  32:       if isa(x,dict): return {k:has(v) for k,v
  33:                               in x.items()
  34:                               if k[0] != "_"}
  35:       if isa(x,o): return has(x.__dict__)
  36:       if isa(x,float): return '%g' % x
  37:       return x
  38:     print(pprint.pformat(has(x),
  39:               indent= indent or the.MISC.show.indent,
  40:               width = width  or the.MISC.show.width))
  41:   
```

## Javascript struct emulation

<a href="gadgets0.py#L68-L72"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  42:   class o:
  43:     def __init__(i,**d)    : i.__dict__.update(d)
  44:     def __setitem__(i,k,v) : i.__dict__[k] = v
  45:     def __getitem__(i,k)   : return i.__dict__[k]
  46:     def __repr__(i)        : return 'o'+str(i.__dict__)
```

## Magic constants

A place to store all the magic params, and reset
them after some study.

That place has the following properties:

+ It is all stored in one central place (so we
  can print all the current constants);
  + This code stores everything in a magic place called `the`.
+ That place can be updated from all over the code base
  (so the specification of those constants can be
  distributed over to near the code that actually uses them);
  + This code defines a decorator that wraps any function
    that defines a settings.
  + E.g. see `MISC`, below.
+ It is possible to:
   + Temporarily override those values;
   + Then reset all those values back to
     some defaults.

The last two requirements are handled by the `study`
function, shown below.

<a href="gadgets0.py#L100-L112"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  47:   the = o()
  48:   
  49:   def setting(f):
  50:     "Decorator. Stores output of function in 'the'."
  51:     name = f.__name__
  52:     def wrapper(**d):
  53:       tmp = f()
  54:       tmp.__dict__.update(d) # maybe do some overrides
  55:       the[name] = tmp  # store the settings in `the`
  56:       return tmp
  57:     wrapper()  # so a side effect of loading the function
  58:                # is to call the function
  59:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L118-L123"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  60:   @setting
  61:   def MISC(): return o(
  62:       seed=1,
  63:       tiles=[0.1,0.3,0.5,0.7,0.9],
  64:       show=o(indent=2,
  65:              width=50))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

While we are about it, lets print

+ the date;
+ what  `the` values were active at the time. 
+ how long it took to run the code

<a href="gadgets0.py#L138-L163"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  66:   def use(x,**y):
  67:     """Convenience function: for temporarily 
  68:        overwriting defaults."""
  69:     return (x,y)
  70:   
  71:   @contextmanager
  72:   def study(what,*usings):
  73:     """Maybe change settings. Always call 
  74:        seed(). Afterwards, set  settings back 
  75:        to defaults."""
  76:     print("\n# " + "-" * 50,                 # before
  77:           "\n# ", what, "\n#",               # before
  78:           datetime.datetime.now().strftime(  # before
  79:             "%Y-%m-%d %H:%M:%S"))            # before
  80:     for (using, override) in usings:         # before
  81:       using(**override)                      # before
  82:     seed()                                   # before
  83:     t1 = time.time()                         # before
  84:     show(the)                                # before
  85:     print("")                                # before
  86:     yield                                      
  87:     t2 = time.time()                         # after
  88:     print("\n# " + "-" * 50)                 # after
  89:     print("# Runtime: %.3f secs\n" % (t2-t1))# after
  90:     for (using,_) in usings:                 # after
  91:       using()                                # after
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

