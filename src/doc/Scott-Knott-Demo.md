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
You may also save your outputs to a file, like this [one]()
