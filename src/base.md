[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## Basic Stuff

General utils- should be useful for all Python programs.

## Standard Header

<a href="base.py#L10-L12"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from __future__ import division
   2:   import sys, random, math, datetime, time,re
   3:   sys.dont_write_bytecode = True
```
## Misc Stuff

### Everyone needs a logo

<a href="base.py#L19-L35"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def logo():
   2:     print """       
   3:                                    _.      
   4:                           _.-----'' `\ 
   5:               __..-----'''            `.
   6:              <            `\.           '\ 
   7:              :.              `.           `\ 
   8:               `:.              `.           `-.
   9:                 `:\ S  D     e   .             +.
  10:                   `:. e  o  d     `.  __.===::::;)
  11:             r   B   `: c       ___.__>'::::::a:f/'
  12:        e          a   `.  _,===:::=-'-=-\"\"\"''
  13:    s      a  b         '-/:::''
  14:                          ''
  15:             c
  16:     """
  17:     print The.misc.copyleft
```

### Options Handling

Place to store things and stuff.

_IDIOM_: every time you run an optimizer, show a
dump of the options used in that run.  

_TRICK_: store the options in a nested anonymous
container.

<a href="base.py#L49-L51"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class o: 
   2:     "Peter Norvig's trick for anonymous containers."
   3:     def __init__(i,**d): i.__dict__.update(d)
```

For example, here are the options used in this code.

<a href="base.py#L57-L82"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def small(l)  : return (l[0]+l[1])*0.5
   2:   def medium(l) : return (l[1]+l[2])*0.5
   3:   def large(l)  : return (l[2]+l[3])*0.5
   4:   
   5:   The= o(cache = 
   6:             o(keep    = 128  # size of sample sace
   7:              ,pending = 4
   8:             ),
   9:          sa =   
  10:             o(cooling = 0.6  # cooling schedule
  11:              ,kmax    = 1000 # max evals
  12:              ,patience= 2000  # run for at least this long
  13:              ,baseline= 100  # initial sample size 
  14:             ),
  15:          misc = 
  16:             o(verbose = False # show stuff?
  17:              ,epsilon = 1.01 # where is close, close enough
  18:              ,seed    = 1    # random number seed
  19:              ,era     = 100  # pause every end of era
  20:              ,repeats = 30   # repeated run
  21:               ,a12     = [0.56, 0.64, 0.71][0] # a12 threshold 
  22:              ,early   = 5 # early stopping
  23:              ,copyleft= """ SEARCH-BASED SE Tools
  24:    (c) 2014, copyright BSD-3, Tim Menzies"""
  25:             )
  26:          )
```

Here's code to dump nested containers:

<a href="base.py#L88-L103"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def showd(d,lvl=0): 
   2:     d = d if isinstance(d,dict) else d.__dict__
   3:     after, line,gap = [], '', '    ' * lvl
   4:     for k in sorted(d.keys()):
   5:       if k[0] == "_": continue
   6:       val = d[k]
   7:       if isinstance(val,(dict,o)):
   8:          after += [k]
   9:       else:
  10:         if callable(val):
  11:           val = val.__name__
  12:         line += (':%s %s ' % (k,val))
  13:     print gap + line
  14:     for k in after: 
  15:         print gap + (':%s' % k)
  16:         showd(d[k],lvl+1)
```

The above code displays _showd(The)_ as follows:

    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 

### Iterators ######################################

<a href="base.py#L118-L122"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def pairs(lst):
   2:     last=lst[0]
   3:     for i in lst[1:]:
   4:       yield last,i
   5:       last = i
```

### Timing Stuff

<a href="base.py#L128-L132"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def msecs(f):
   2:     import time
   3:     t1 = time.time()
   4:     f()
   5:     return (time.time() - t1) * 1000
```

### Random Stuff

<a href="base.py#L138-L143"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   rand=  random.random # generate nums 0..1
   2:   any=   random.choice # pull any from list
   3:   
   4:   def rseed(seed = None):
   5:     seed = seed or The.misc.seed
   6:     random.seed(seed) 
```

The above example shows a use of a global option.
Note that the following alternative for _rseed()_ 
would be buggy (since this alternate _rseed_ 
could very well use the 
_The.misc.seed_ known at load time and not some
seed you change at run time).

    def rseed(seed = The misc.seed): # do not
      random.seed(seed)              # do this

### Maths Stuff

<a href="base.py#L159-L170"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def log2(num): 
   2:     "Log base 2 of number"
   3:     return math.log(num)/math.log(2)
   4:   
   5:   def norm(x,lo,hi):
   6:     "Generate a num 0..1 for lo..hi"
   7:     tmp = (x - lo) / (hi - lo + 0.00001) 
   8:     return max(0,min(tmp,1))
   9:   
  10:   def mron(x,lo,hi):
  11:     "Generate a num 1..0 for lo..hi"
  12:     return 1 - norm(x,lo,hi)
```

### Printing stuff

<a href="base.py#L176-L196"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def burp(*lst):  
   2:     "If verbose enabled, print a list of things."
   3:     The.misc.verbose and say(
   4:       ', '.join(map(str,lst)))
   5:   
   6:   nl="\n"
   7:   def says(*lst):
   8:     say(' '.join(map(str,lst)))
   9:   
  10:   def say(x): 
  11:     "Print something with no trailing new line."
  12:     sys.stdout.write(str(x)); sys.stdout.flush()
  13:   
  14:   def gn(lst,n):
  15:     "Function to print floats in short form"
  16:     fmt = '%.' + str(n) + 'f'
  17:     return ', '.join([(fmt % x) for x in lst])
  18:   
  19:   def x(n):
  20:     "Shorthand for short floats"
  21:     return ':%3.1f' % n
```

The following convenience functions print a list
of floats to  0, 2, or 3 decimal places (useful for condensing old reports).

<a href="base.py#L203-L205"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def g0(lst): return gn(lst,0)
   2:   def g2(lst): return gn(lst,2)
   3:   def g3(lst): return gn(lst,3)
```

### Printing a xtile chart.

<a href="base.py#L211-L239"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def xtile(lst,lo=0,hi=0.001,width=50,
   2:                chops=[0.1 ,0.3,0.5,0.7,0.9],
   3:                marks=["-" ," "," ","-"," "],
   4:                bar="|",star="*",show=" %3.0f"):
   5:     """The function _xtile_ takes a list of (possibly)
   6:     unsorted numbers and presents them as a horizontal
   7:     xtile chart (in ascii format). The default is a 
   8:     contracted _quintile_ that shows the 
   9:     10,30,50,70,90 breaks in the data (but this can be 
  10:     changed- see the optional flags of the function).
  11:     """
  12:     def pos(p)   : return ordered[int(len(lst)*p)]
  13:     def place(x) : 
  14:       return int(width*float((x - lo))/(hi - lo))
  15:     def pretty(lst) : 
  16:       return ', '.join([show % x for x in lst])
  17:     ordered = sorted(lst)
  18:     lo      = min(lo,ordered[0])
  19:     hi      = max(hi,ordered[-1])
  20:     what    = [pos(p)   for p in chops]
  21:     where   = [place(n) for n in  what]
  22:     out     = [" "] * width
  23:     for one,two in pairs(where):
  24:       for i in range(one,two): 
  25:         out[i] = marks[0]
  26:       marks = marks[1:]
  27:     out[int(width/2)]    = bar
  28:     out[place(pos(0.5))] = star 
  29:     return ''.join(out) +  "," +  pretty(what)
```

For example, the example displays 1000 random numbers as follows:

    ---   *     |------      , 0.01,  0.15,  0.26,  0.52,  0.79

<a href="base.py#L247-L251"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def _tileX() :
   2:     import random
   3:     random.seed(1)
   4:     nums = [random.random()**2 for _ in range(100)]
   5:     print xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f")
```

## Coercion

<a href="base.py#L257-L262"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def atom(x):
   2:     "String to number."
   3:     try : return int(x)
   4:     except ValueError:
   5:       try : return float(x)
   6:       except ValueError: return x
```

### Command line processing ########################

The following code lets you call any function with keyword
defaults.

For example, consider the following function:

<a href="base.py#L273-L276"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   
   2:   def cmdDemo(who='Tim', when=2015, where='Raleigh'):
   3:     says(':who',who,':when',when,':where',where,nl)
   4:   
```
If this function is in a file with the last line:

    if __name__ == "__main__": eval(cmd())

Then this function can be called as follows:

    % python base.py  when 2010 who Jane

this would print 

    $ python base.py cmdDemo when 1990 who Jane
    :who Jane :when 1990 :where Raleigh 

Note that the arguments are supplied in a different
order to those seen in the function header.  Also,
if you do not mention some argument, it is filled in
from the function defaults.



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

