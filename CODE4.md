[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Code4: coding homework 

## What to Hand in

After doing all the following, you should 
be able to write one source files into  `hw/code/3` along with
screen snaps of your work (if relevant).

Using some URL shortener (e.g. goo.gl), shorten the URL to `hw/code/4`
and paste into [the submission page](https://goo.gl/lZEmEm).


# Basic Simulated Annealing

Read the [lecture](SA.md) on simulated annealing.

Hack up a simulated annealer for the
[Schaffer](models/moeaProblems.pdf) model.

Do not be clever. This is throw away code. As quick
and as dirty as you like.

To create neighbors, just mutate the single
independent variable at each run.

To compute energy, add the sum of the two _f1_, _f2_
 variables. Note that for the [lecture](SA.md) code to
 work, that sum has to be normalized 0..1. So
 conduct a _baseline_ study where you run the
 [Schaffer](models/moeaProblems.pdf) 100 times to
 find the min and max values for _f1 + f2_ . Take
 those numbers then hardwire the following
 normalization function:
 
     energy(f1,f2) = ((f1 + f2) - min) / (max - min)

(Note also, you will need that maximum energy figure to implement _emax_).

Try and make a report that looks like the follow. Do
not sweat the details (near enough is good enough but the idea is that every
25 evaluations, we print a new line and the current energy)/
Also,  the idea here is that every try to make the crazy jumps (_"?"_) less
frequent later on (and don't worry if you cannot).


````
### saDemo ##################################################
# 2015-08-09 00:23:35
# Basic study.
!!! Schaffer

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
, 0250, :1.0,  .....+...+....?+.+..+....
, 0275, :1.0,  ........................?
, 0300, :1.0,  .++.+.............?+.+..+
, 0325, :1.0,  .........................
, 0350, :1.0,  .........................
, 0375, :1.0,  .........................
, 0400, :1.0,  ?++++............+.......
, 0425, :1.0,  .........................
, 0450, :1.0,  .........................
, 0475, :1.0,  ........?+.?+............
, 0500, :1.0,  ....?+.++.....+..........
, 0525, :1.0,  ..........?.+............
, 0550, :1.0,  .....................?++.
, 0575, :1.0,  .++......................
, 0600, :1.0,  .........................
, 0625, :1.0,  .........................
, 0650, :1.0,  ...........?+++.?+.+.+...
, 0675, :1.0,  .........................
, 0700, :1.0,  .....?+..................
, 0725, :1.0,  .........................
, 0750, :1.0,  .............?+..+.......
, 0775, :1.0,  .........................
, 0800, :1.0,  .........................
, 0825, :1.0,  .........................
, 0850, :1.0,  .........................
, 0875, :1.0,  ...................?.+...
, 0900, :1.0,  .....?+++...?++..+....+..
, 0925, :1.0,  ?++.+.+..................
, 0950, :1.0,  ....?.+...+.....+........
, 0975, :1.0,  .........................
------
:e 0.997611905488
:y 0.490, 1.690
:x 0.700

------------------------------------------------------------------------

:cache
    :keep 128 :pending 4
:misc
    :a12 0.56 :copyleft  SEARCH-BASED SE Tools
 (c) 2014, copyright BSD-3, Tim Menzies :early 5 :epsilon 1.01 :era 25 :repeats 30 :seed 1 :verbose True
:sa
    :baseline 100 :cooling 0.6 :kmax 1000 :patience 2000

# Runtime: 0.023 secs
```

## Tips

### Write, no new line

In olde Python, to print something without a new line:

```python
import sys

def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()
```

In new Python:

```python
from __future__ import print

def say(x): print(x, end="")
```

### (Optional) Baselines

In the above, it was needed to pre-run the model a
hundred times or so to learn min,max and _emax_.
That is a simple enough process to automate.


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

