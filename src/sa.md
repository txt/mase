[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## SA (plus tricks)

This file shows some
of Timm's tricks for building an optimization.

To illustrate the tricks, they are applied to 
build a simulated annealer.

In sumamry, those tricks are:

+ [Some basic Python tricks](basepy);
+ [Tricks for logging values](logpy);
+ [Tricks for succinctly specifying models](modelspy);
+ [Tricks for running optimization studies](optimizepy).

Share and enjoy.


### Standard Headers
<a href="sa.py#L23-L27"><img align=right src="http://www.craiggiven.com/textfile_icon.gif"></a><br clear=all>
```python

   1:   from __future__ import division
   2:   import sys
   3:   sys.dont_write_bytecode = True
   4:   
   5:   from models import *
```

### Code

The following code assumes that _energy_ is the 
sum of the dependent variables.

The _m_ variable is an instance of class [Model](modelspy).

This code seeks to maximize the energy
so we normalize energies
in the range lo..hi  to 1..0 .

A baseline study collects standard values for these
dependent values: see the _base_ variable, which calls the
model The.sa.baseline number of times. 

These baseline is
used to learn the _lo,hi_ values of the energy
which is then used to normalize all future energies
one to zero, min to max.

In the following, we terminate early if we fall within
_The.misc.epsilon_ of best energy or we do more
that _The.sa.kmax_ iterations.
 
Finally, the _burp_ function prints some output- which can
suppressed via _The.misc.verbose=False_.

<a href="sa.py#L58-L92"><img align=right src="http://www.craiggiven.com/textfile_icon.gif"></a><br clear=all>
```python

   1:   def sa(m):
   2:     def more(k,e):
   3:       if k > The.sa.patience:
   4:         if e > 1/The.misc.epsilon:
   5:           return False
   6:       return True
   7:     def energy(m,it): 
   8:       m.depIT(it)
   9:       return sum(it.y) 
  10:     def maybe(old,new,temp): 
  11:       return math.e**((new - old)/temp) < rand()  
  12:     base = Num([energy(m, m.indepIT()) 
  13:                for _ in xrange(The.sa.baseline)])
  14:     sb = s = m.indepIT()
  15:     eb = e = mron(energy(m,s), base.lo, base.hi)
  16:     k = 0
  17:     while k <  The.sa.kmax and more(k,eb):
  18:       if not k % The.misc.era: 
  19:         burp("\n", str(k).zfill(4),x(eb), ' ') 
  20:       k += 1
  21:       mark = "."
  22:       sn = m.aroundIT(s,p=1)
  23:       en = mron(energy(m,sn), base.lo, base.hi)
  24:       if en >  (e * The.misc.epsilon):
  25:         s,e = sn,en
  26:         mark = "+"
  27:       elif maybe(e,en, 
  28:                  k/The.sa.kmax**The.sa.cooling):
  29:         s,e = sn,en
  30:         mark = "?"
  31:       if en > (eb * The.misc.epsilon):
  32:         sb,eb = sn,en
  33:         mark = "!"
  34:       burp(mark)
  35:     return sb,eb    
```

## Example

Defining a study using _sa_.

<a href="sa.py#L100-L111"><img align=right src="http://www.craiggiven.com/textfile_icon.gif"></a><br clear=all>
```python

   1:   @study
   2:   def saDemo(model='Schaffer'):
   3:     "Basic study."
   4:     The.misc.verbose= True
   5:     The.misc.era = 25
   6:     print "!!!",model
   7:     model = eval(model + '()')
   8:     print "\n",model.name()
   9:     sb,eb = sa(model)
  10:     x= g3(sb.x)
  11:     y= g3(sb.y)
  12:     print "\n------\n:e",eb,"\n:y",y,"\n:x",x
```

Output from the first call:


    ### saDemo ##################################################
    # 2014-09-02 11:19:58
    # Basic study.
    
    Schaffer
    
    , 0000, :0.2,  !.?+?+??.+?.++?+.++...?.+
    , 0025, :1.0,  .?+..?+?+..+..?++..??+.?.
    , 0050, :1.0,  +....?+.?+.+.?++++?+.?.+.
    , 0075, :1.0,  .?+......?+..?+......+...
    , 0100, :1.0,  .+........?+.?++++?.+?+..
    , 0125, :1.0,  ..+...?+.................
    , 0150, :1.0,  ................?++...+?.
    , 0175, :1.0,  +++...?+.+.?++.......?.+.
    , 0200, :1.0,  ...?+..+.+..?+.+.+.......
    , 0225, :1.0,  ...?+..............+...?+
    , 0250, :1.0,  .
    ------
    :e 0.997611905488 
    :y 0.490, 1.690 
    :x 0.700
    
    --------------------------------------------------
    
    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 
    
    # Runtime: 0.007 secs
    
Output from the second call:

    ### saDemo ##################################################
    # 2014-09-02 11:19:58
    # Basic study.
    
    ZDT1
    
    , 0000, :0.2,  !?+?!??++?+?++.!?++.....?
    , 0025, :0.8,  !?+?+?+.+..+....?.+.?++.+
    , 0050, :1.0,  ?+?..?+?+.+.....+.+...?..
    , 0075, :1.0,  ?++?......?+.+....?..?++.
    , 0100, :1.0,  +.......?..?+.+.......?.+
    , 0125, :1.0,  ++?+.....................
    , 0150, :1.0,  ?++...?..?+.+.?+++..?+..+
    , 0175, :1.0,  +...............?......+.
    , 0200, :1.0,  .........................
    , 0225, :1.0,  ....?++.+......?+........
    , 0250, :1.0,  .
    ------
    :e 1 
    :y 0.125, 4.186 
    :x 0.125, 0.407, 0.137, 0.079, 0.154, 0.301, 
       0.999, 0.479, 0.109, 0.454, 0.395, 0.333, 
       0.268, 0.196, 0.926, 0.322, 0.133, 0.470, 
       0.043, 0.134, 0.755, 0.859, 0.156, 0.318, 
       0.196, 0.416, 0.133, 0.089, 0.386, 0.618
    
    --------------------------------------------------
    
    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 
    
    # Runtime: 0.011 secs
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

