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
   3:   import random
   4:   from ok import *
```

## Some one liners.

<a href="gadgets0.py#L21-L29"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   5:   r   = random.random
   6:   isa = isinstance
   7:   
   8:   def seed(x=None):
   9:     random.seed(x or the.misc.seed)
  10:   
  11:   def shuffle(lst):
  12:     random.shuffle(lst)
  13:     return lst
```

## Printing some structure of arbitrary depth:

<a href="gadgets0.py#L35-L47"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  14:   def show(x, indent=None, width=None):
  15:     def has(x):
  16:       if isa(x,list): return [has(v) for v in x]
  17:       if isa(x,dict): return {k:has(v) for k,v
  18:                               in x.items()
  19:                               if k[0] != "_"}
  20:       if isa(x,o): return has(x.__dict__)
  21:       if isa(x,float): return '%g' % x
  22:       return x
  23:     print(pprint.pformat(has(x),
  24:               indent= indent or the.misc.show.indent,
  25:               width = width  or the.misc.show.width))
  26:   
```

## Javascript struct emulation

<a href="gadgets0.py#L53-L57"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  27:   class o:
  28:     def __init__(i,**d)    : i.__dict__.update(d)
  29:     def __setitem__(i,k,v) : i.__dict__[k] = v
  30:     def __getitem__(i,k)   : return i.__dict__[k]
  31:     def __repr__(i)        : return 'o'+str(i.__dict__)
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
  + E.g. see `misc`, below.
+ It is possible to:
   + Temporarily override those values;
   + Then reset all those values back to
     some defaults.

The last two requirements are handled by the `study`
function, shown below.

<a href="gadgets0.py#L85-L97"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  32:   the = o()
  33:   
  34:   def setting(f):
  35:     "Decorator. Stores output of function in 'the'."
  36:     name = f.__name__
  37:     def wrapper(**d):
  38:       tmp = f()
  39:       tmp.__dict__.update(d) # maybe do some overrides
  40:       the[name] = tmp  # store the settings in `the`
  41:       return tmp
  42:     wrapper()  # so a side effect of loading the function
  43:                # is to call the function
  44:     return wrapper
```

### Set some settings

<a href="gadgets0.py#L103-L107"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  45:   @setting
  46:   def misc(): return o(
  47:       seed=1,
  48:       show=o(indent=2,
  49:              width=50))
```

### Temporarily Setting, the Resetting

Here's a place to explore changes to the defaults, and have
all those changes undo afterwards.

<a href="gadgets0.py#L116-L140"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  50:   def use(x,**y):
  51:     """Convenience function: for temporarily 
  52:        overwriting defaults."""
  53:     return (x,y)
  54:   
  55:   @contextmanager
  56:   def study(what,*usings):
  57:     """Maybe change settings. Always call 
  58:        seed(). Afterwards, set  settings back 
  59:        to defaults."""
  60:     print("\n# " + "-" * 50,
  61:           "\n# ", what, "\n#",
  62:           datetime.datetime.now().strftime(
  63:             "%Y-%m-%d %H:%M:%S"))
  64:     for (using, override) in usings:
  65:       using(**override)
  66:     seed()
  67:     t1 = time.time()
  68:     yield
  69:     show(the)
  70:     t2 = time.time()
  71:     print("\n# " + "-" * 50)
  72:     print("# Runtime: %.3f secs" % (t2-t1))
  73:     for (using,_) in usings:
  74:       using()
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

