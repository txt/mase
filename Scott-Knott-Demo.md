[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Scott-Knott Charts

To enable you to print acii quartile charts like

```
rank ,         name ,    med   ,  iqr
----------------------------------------------------
   1 ,           x5 ,    0.25  ,  0.20 (   ----*---    |              ), 0.20,  0.30,  0.40
   1 ,           x3 ,    0.30  ,  0.15 (     ----*-    |              ), 0.25,  0.35,  0.40
   2 ,           x1 ,    0.50  ,  0.11 (              -*--            ), 0.49,  0.51,  0.60
   3 ,           x2 ,    0.75  ,  0.20 (               |      ----*-- ), 0.70,  0.80,  0.90
   3 ,           x4 ,    0.75  ,  0.20 (               |      ----*-- ), 0.70,  0.80,  0.90
```

We have a script called [sk.py](https://github.com/txt/mase/blob/master/src/doc/sk.py)

## Using `sk.py`

To use sk, you need to know 2 main functions:
  - `rdivDemo(data)`
  - `fromFile(f="filename.dat")`


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

