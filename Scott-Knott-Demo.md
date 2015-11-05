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

### 1. `rdivDemo(data)`
To use `rdivDemo(data)`, format data as a list of lists.

If you have, say, the following 5 treatments to compare:
```
x1 0.34 0.49 0.51 0.60
x2 0.9 0.7 0.8 0.60
x3 0.15 0.25 0.4 0.35
x4 0.6 0.7 0.8 0.90
x5 0.1 0.2 0.3 0.40
```

Format this as:
`data = [['x1', 0.34, 0.49, 0.51, 0.6], ['x2', 0.9, 0.7, 0.8, 0.6], ['x3', 0.15, 0.25, 0.4, 0.35], ['x4', 0.6, 0.7, 0.8, 0.9], ['x5', 0.1, 0.2, 0.3, 0.4]]`

And when you pass this to `rdivDemo(data)`, you'll get the nice ascii charts.

### 2. `fromFile(f='filename.dat')`
You may also save your outputs to a file, like this [one](https://github.com/txt/mase/blob/master/src/doc/data.dat). In that case, all you have to do is run `fromFile(f='filename.dat')` to get the outputs.




_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

