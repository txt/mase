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
````python
<font color=red>   1:</font> from __future__ import division
<font color=red>   2:</font> import sys
<font color=red>   3:</font> sys.dont_write_bytecode = True
<font color=red>   4:</font> 
<font color=red>   5:</font> from models import *
````

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
<font color=red>   6:</font> def sa(m):
<font color=red>   7:</font>   def more(k,e):
<font color=red>   8:</font>     if k > The.sa.patience:
<font color=red>   9:</font>       if e > 1/The.misc.epsilon:
<font color=red>  10:</font>         return False
<font color=red>  11:</font>     return True
<font color=red>  12:</font>   def energy(m,it): 
<font color=red>  13:</font>     m.depIT(it)
<font color=red>  14:</font>     return sum(it.y) 
<font color=red>  15:</font>   def maybe(old,new,temp): 
<font color=red>  16:</font>     return math.e**((new - old)/temp) < rand()  
<font color=red>  17:</font>   base = Num([energy(m, m.indepIT()) 
<font color=red>  18:</font>              for _ in xrange(The.sa.baseline)])
<font color=red>  19:</font>   sb = s = m.indepIT()
<font color=red>  20:</font>   eb = e = mron(energy(m,s), base.lo, base.hi)
<font color=red>  21:</font>   k = 0
<font color=red>  22:</font>   while k <  The.sa.kmax and more(k,eb):
<font color=red>  23:</font>     if not k % The.misc.era: 
<font color=red>  24:</font>       burp("\n", str(k).zfill(4),x(eb), ' ') 
<font color=red>  25:</font>     k += 1
<font color=red>  26:</font>     mark = "."
<font color=red>  27:</font>     sn = m.aroundIT(s,p=1)
<font color=red>  28:</font>     en = mron(energy(m,sn), base.lo, base.hi)
<font color=red>  29:</font>     if en >  (e * The.misc.epsilon):
<font color=red>  30:</font>       s,e = sn,en
<font color=red>  31:</font>       mark = "+"
<font color=red>  32:</font>     elif maybe(e,en, 
<font color=red>  33:</font>                k/The.sa.kmax**The.sa.cooling):
<font color=red>  34:</font>       s,e = sn,en
<font color=red>  35:</font>       mark = "?"
<font color=red>  36:</font>     if en > (eb * The.misc.epsilon):
<font color=red>  37:</font>       sb,eb = sn,en
<font color=red>  38:</font>       mark = "!"
<font color=red>  39:</font>     burp(mark)
<font color=red>  40:</font>   return sb,eb    
````

## Example

Defining a study using _sa_.

````python
<font color=red>  41:</font> @study
<font color=red>  42:</font> def saDemo(model='Schaffer'):
<font color=red>  43:</font>   "Basic study."
<font color=red>  44:</font>   The.misc.verbose= True
<font color=red>  45:</font>   The.misc.era = 25
<font color=red>  46:</font>   print "!!!",model
<font color=red>  47:</font>   model = eval(model + '()')
<font color=red>  48:</font>   print "\n",model.name()
<font color=red>  49:</font>   sb,eb = sa(model)
<font color=red>  50:</font>   x= g3(sb.x)
<font color=red>  51:</font>   y= g3(sb.y)
<font color=red>  52:</font>   print "\n------\n:e",eb,"\n:y",y,"\n:x",x
````

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
<font color=red>  53:</font> 
<font color=red>  54:</font> if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

