[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## Models

## Standard Header

````python
<font color=red>   1:</font> from __future__ import division
<font color=red>   2:</font> import sys
<font color=red>   3:</font> sys.dont_write_bytecode = True
<font color=red>   4:</font> 
<font color=red>   5:</font> from optimize import *
````

## Classes

The instance created by (say) _In(0,10)_
can be queried to return numbers in the range 0 to 10.
For example:

    >>> x = In(0,10)
    >>> lst = sorted([x() for _ in xrange(32)])
    >>> print g2(lst)
    >>> 0.00, 0.03, 0.36, 0.75, 0.95, 1.02, 
        1.21, 2.07, 2.38, 2.87, 2.97, 3.19, 
        3.35, 3.50, 3.67, 3.97, 4.33, 4.77, 
        5.72, 5.76, 5.99, 6.14, 6.70, 7.55, 
        7.91, 8.36, 8.42, 8.50, 8.72, 8.79, 
        9.25, 9.48

Code:

````python
<font color=red>   6:</font> 
<font color=red>   7:</font> 
<font color=red>   8:</font> class In:
<font color=red>   9:</font>   def __init__(i,lo=0,hi=1,txt=""):
<font color=red>  10:</font>     i.txt,i.lo,i.hi = txt,lo,hi
<font color=red>  11:</font>   def __call__(i): 
<font color=red>  12:</font>     return i.lo + (i.hi - i.lo)*rand()
<font color=red>  13:</font>   def log(i): 
<font color=red>  14:</font>     return Num()
<font color=red>  15:</font> 
````

Note the brevity of this code. Lesson:
you can write your own variants of the _In_ generator
to handle different distributions.
These variants can be used to create generators for 
model attribute values (see below).

### Models

The following models return generators for attribute values
divided into independent values (in "_x_") and
dependent values (in "_y_").

````python
<font color=red>  16:</font> 
<font color=red>  17:</font> class Schaffer(Model):
<font color=red>  18:</font>   def spec(i):
<font color=red>  19:</font>     return o(x= [In(-5,5,0)],
<font color=red>  20:</font>              y= [i.f1,i.f2])
<font color=red>  21:</font>   def f1(i,it):
<font color=red>  22:</font>     x=it.x[0]; return x**2
<font color=red>  23:</font>   def f2(i,it):
<font color=red>  24:</font>     x=it.x[0]; return (x-2)**2
<font color=red>  25:</font> 
<font color=red>  26:</font> class ZDT1(Model):
<font color=red>  27:</font>   def spec(i):
<font color=red>  28:</font>     return o(x= [In(0,1,z) for z in range(30)],
<font color=red>  29:</font>               y= [i.f1,i.f2])
<font color=red>  30:</font>   def f1(i,it):
<font color=red>  31:</font>     return it.x[0]
<font color=red>  32:</font>   def f2(i,it):
<font color=red>  33:</font>     return 1 + 9*sum(it.x[1:]) / 29
<font color=red>  34:</font> 
<font color=red>  35:</font> if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

