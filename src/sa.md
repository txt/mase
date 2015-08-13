[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


<a href="sa.py"><img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/py.png"></a>

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
````python
   1:   from __future__ import division
   2:   import sys
   3:   sys.dont_write_bytecode = True
   4:   
   5:   from models import *
````
<a href="sa.py#L23-L27"><img align=right src="http://www.hypercosm.com/google_code/images/source_code_icon.jpg"></a><br clear=all>

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

````python
   6:   def sa(m):
   7:     def more(k,e):
   8:       if k > The.sa.patience:
   9:         if e > 1/The.misc.epsilon:
  10:           return False
  11:       return True
  12:     def energy(m,it): 
  13:       m.depIT(it)
  14:       return sum(it.y) 
  15:     def maybe(old,new,temp): 
  16:       return math.e**((new - old)/temp) < rand()  
  17:     base = Num([energy(m, m.indepIT()) 
  18:                for _ in xrange(The.sa.baseline)])
  19:     sb = s = m.indepIT()
  20:     eb = e = mron(energy(m,s), base.lo, base.hi)
  21:     k = 0
  22:     while k <  The.sa.kmax and more(k,eb):
  23:       if not k % The.misc.era: 
  24:         burp("\n", str(k).zfill(4),x(eb), ' ') 
  25:       k += 1
  26:       mark = "."
  27:       sn = m.aroundIT(s,p=1)
  28:       en = mron(energy(m,sn), base.lo, base.hi)
  29:       if en >  (e * The.misc.epsilon):
  30:         s,e = sn,en
  31:         mark = "+"
  32:       elif maybe(e,en, 
  33:                  k/The.sa.kmax**The.sa.cooling):
  34:         s,e = sn,en
  35:         mark = "?"
  36:       if en > (eb * The.misc.epsilon):
  37:         sb,eb = sn,en
  38:         mark = "!"
  39:       burp(mark)
  40:     return sb,eb    
````
<a href="sa.py#L58-L92"><img align=right src="http://www.hypercosm.com/google_code/images/source_code_icon.jpg"></a><br clear=all>

## Example

Defining a study using _sa_.

````python
  41:   @study
  42:   def saDemo(model='Schaffer'):
  43:     "Basic study."
  44:     The.misc.verbose= True
  45:     The.misc.era = 25
  46:     print "!!!",model
  47:     model = eval(model + '()')
  48:     print "\n",model.name()
  49:     sb,eb = sa(model)
  50:     x= g3(sb.x)
  51:     y= g3(sb.y)
  52:     print "\n------\n:e",eb,"\n:y",y,"\n:x",x
````
<a href="sa.py#L100-L111"><img align=right src="http://www.hypercosm.com/google_code/images/source_code_icon.jpg"></a><br clear=all>

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
````python
  53:   
  54:   if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

