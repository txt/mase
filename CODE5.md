[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Code5: coding homework 

## What to Hand in

After doing all the following, you should 
be able to write one source files into  `hw/code/5` along with
screen snaps of your work (if relevant).

Using some URL shortener (e.g. goo.gl), shorten the URL to `hw/code/5`
and paste into [the submission page](https://goo.gl/lZEmEm).


# Basic Max Walk Sat

Read the [lecture](MWS.md) on Max Walk Sat.

Code  MaxWalkSat  for the
[Osyczka2](models/moeaProblems.pdf) model.

Do not be clever. This is throw away code. As quick
and as dirty as you like.


Use the same energy calcs as for SA.

Try and make a report that looks like the output from SA.

## Tips

### Not everything is "ok".


Note that this model has constraints-- so after you
_mutate_ a solution, you must check if it is _ok_
(I.e. does not violate the constraints-- otherwise,
mutate again until ok).


### Local Search



#### When

Use p=0.5

#### How

Given min to max values for every value, try steps of _(max - min)/steps_ for, say, _steps=10_.

### Watch those evals

Note that now, when you report evals, then you are reporting _steps * evals_. So when you report how long it takes to reach a
solution, remember to reports _steps * evals_.





_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

