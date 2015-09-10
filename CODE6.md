[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Code6: coding homework:  Generic Experiments

NOTE TO STUDENTS: if this homework seems too complex, then reflect a little more on Code4 and Code5. This
code generalizes Code45 to the point where we can quickly write many models and many optimizers. So it
actually _simplifies_ the optimization process.... at the cost of some extra architecture.

## What to Hand in

After doing all the following, you should 
be able to write one source files into  `hw/code/6` along with
screen snaps of your work (if relevant).

Using some URL shortener (e.g. goo.gl), shorten the URL to `hw/code/6`
and paste into [the submission page](https://goo.gl/lZEmEm).

From the following, show the output of running sa, mws on Schaffer, Osyczka2, Kursawe.


# To Do

Rewrite your SA and MWS code such that you can run the following loop:

```python
for model in [Schaffer, Osyczka2, Kursawe]:
  for optimizer in [sa, mws]:
     optimizer(model())
```

This is the _generic experiment loop_ that allows for rapid extension to handle more models and more optimizers.

## Tips

### Another Model

The above loops requires the  [Kursawe](models/moeaProblems.pdf) model.

### Optimizer as function

The above code assumes that _mws_, _sa_ are functions that accept one argument: a description of the model they are processing.

### Model as Class

For the above loop to work, each model (e.g. _Schaffer_) has to be class that produces an instance via _model()_.
That model defines:

+ the number of decisions;
+ the number of objectives;
+ the name of each decision/objective;
+ the min/max range of each decision/objective;
+ the _any_ function that scores a candidate
+ the _ok_ function that checks if a particular candidate is valid (for _Schaffer and Kursawe_, this returns _True_ while
for _Osyczka2_, this does some checking).
+ the _eval_ function that computes the objective scores for each candidate

### Candidate as Instance

While the models are all different, the form of the candidates can be the same. Using the [o](https://github.com/txt/mase/blob/master/src/abstract.py#L246-L261) class, you could define a candidate in a generic way:

```python
def candidate(): return o(decs=[],objs=[], scores=[],energy = None)
```

then use a _model_ to fill in the generic candidate; e.g.

```python
class Model:
def eval(i,c):
  if not c.scores:
      c.scores = [obj(c) for obj in i.objectives()] 
  if c.energy == None
      c.energy = i.energy(c.scores)
  return c
```

Note that _Schaffer, Kursawe, Osyczka2_ (and all other models) could subclass _Model_ and use the same _eval_ method.

Also, _i.objectives_ is some Model property that lists a set of methods to call to evaluate a score. E.g. for Schaffer

```python
class Schaffer(Models):
  def f1(i,c):
    x=c.decs[0]
    return x**2
  def f2(i,c):
	x=c.decs[0]
	return (x-2)**2
  def objectives(i):
    return [i.f1,i.f2] 
```
			 
### Attributes as Ranges

All your models will have to know about the name and range of values for each attribute. This can be stored in yet another
class, which I call _Has_.

Here, in all its complex glory, is my _Has_ class.

+ If _i.touch_ is _True_ then I am allowed to mutate it (by default, I can mutate anything)
+ If _goal_ is not Nil, then this is an objective
   + If non-nil, _goal_ can be one of _lt_ or _gt_ indicating what direction is _better_.

Note that you won't need (yet) a class this complex. But something (simpler) that this should be used inside _Model_ in
a method that defines the decisions and objectives.


```python
import random
r = random.random
def within(lo,hi): return lo + (hi - lo)*r()
def lt(x,t): return x < y # less than
def bt(x,y_: return x > y # better than

class Has(object):
  def __init__(i,name='',lo=0,hi=1e32,init=0,
               goal=None,touch=True):
    i.name,i.lo,i.hi      = name,lo,hi
    i.init,i.goal,i.touch = init,goal,touch
 def restrain(i,x):
    if   x < i.lo: return i.lo
    elif x > i.hi: return i.hi
    else:
      return x
  def any(i):
    return within(i.lo,i.hi)
  def ok(i,x):
    return i.lo <= x <= i.hi
  def __repr__(i):
    return '%s=%s' % (i.name, o(name=i.name,lo=i.lo,hi=i.hi,init=i.init,goal=i.goal,touch=i.touch))
```



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

