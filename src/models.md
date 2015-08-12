[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


<a href="models.py"><img src="https://raw.githubusercontent.com/txt/mase/master/img/py.png"></a><br clear=all>

## Models

## Standard Header

````python
   1:   from __future__ import division
   2:   import sys
   3:   sys.dont_write_bytecode = True
   4:   
   5:   from optimize import *
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
   6:   
   7:   
   8:   class In:
   9:     def __init__(i,lo=0,hi=1,txt=""):
  10:       i.txt,i.lo,i.hi = txt,lo,hi
  11:     def __call__(i): 
  12:       return i.lo + (i.hi - i.lo)*rand()
  13:     def log(i): 
  14:       return Num()
  15:   
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
  16:   
  17:   class Schaffer(Model):
  18:     def spec(i):
  19:       return o(x= [In(-5,5,0)],
  20:                y= [i.f1,i.f2])
  21:     def f1(i,it):
  22:       x=it.x[0]; return x**2
  23:     def f2(i,it):
  24:       x=it.x[0]; return (x-2)**2
  25:   
  26:   class ZDT1(Model):
  27:     def spec(i):
  28:       return o(x= [In(0,1,z) for z in range(30)],
  29:                 y= [i.f1,i.f2])
  30:     def f1(i,it):
  31:       return it.x[0]
  32:     def f2(i,it):
  33:       return 1 + 9*sum(it.x[1:]) / 29
  34:   
  35:   if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

