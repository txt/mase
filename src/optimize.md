[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## Optimize

### Standard Header

<a href="optimize.py#L8-L12"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from __future__ import division
   2:   import sys, random, math, datetime, time,re
   3:   sys.dont_write_bytecode = True
   4:   
   5:   from log  import *
```


## @study: Simulation Experiment Control

The code adds a set of cliches onto
to some optimization call:

+ **TRAP THE SEED**. I cannot stress this enough.
  When debugging or reproducing old code, it is vital
  you can access the old seed.
+ When generating output, add a date stamp and
  any available information about the function being
  called.
+ Show the runtimes of the call.
+ Show the options used by the call.

For example, suppose this was your 
main call to an optimizer:

    @study
    def saDemo(model='Schaffer'):
      "Basic study."
      model = eval(model + '()')
      print "\n",model.name()
      sb,eb = sa(model)
      x= g3(sb.x)
      y= g3(sb.y)
      print "\n------\n:e",eb,"\n:y",y,"\n:x",x

When run, this generates the following output:

    >>>> saDemo(ZDT1())

    ### saDemo ##################################################
    # 2014-09-02 10:40:00
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
    
    # Runtime: 0.020 secs


Code:

<a href="optimize.py#L88-L106"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def study(f):
   2:     def wrapper(**lst):
   3:       rseed() # reset the seed to our default
   4:       what = f.__name__# print the function name
   5:       doc  = f.__doc__ # print the function doc
   6:       if doc:
   7:         doc= re.sub(r"\n[ \t]*","\n# ",doc)
   8:       # print when this ran
   9:       show = datetime.datetime.now().strftime
  10:       print "\n###",what,"#" * 50
  11:       print "#", show("%Y-%m-%d %H:%M:%S")
  12:       if doc: print "#",doc
  13:       t1 = time.time()
  14:       f(**lst)          # run the function
  15:       t2 = time.time() # show how long it took to run
  16:       print "\n" + ("-" * 72)
  17:       showd(The)       # print the options
  18:       print "\n# Runtime: %.3f secs" % (t2-t1)
  19:     return wrapper
```

## Model Definition

Over the years, I've learned to tease apart
several aspects of optimization; specifically:

+ how to make candidate values
+ how to change candidate values
+ how to record the candidate values.
+ and all that is separate to where I store the 
  current candidate. 


The thing that weaves
all those aspects together is the _Model_ class.
Such a  _Model_ 
  does not store an individual candidate. Rather
  it stores information _about_ the candidate
  including how to make, log and change it.

In the following:

+ Those candidates are called _it_.
+ The generators are called _of_,
+ The things that record values are called _log_.

All of _(it, of, log)_ are stored in the same pair of dependent
and independent variables. So many times in the following
code is some container:

     o(x= Independents, y= Dependents)

WARNING: my code is a little nervous about always scoring the dependent
variables every time I change the independent variables (lest that evaluation
makes the whole process too slow). Which means that my _it_ things often
contain nulls for the dependent variables. This can lead to bugs of the form:

    TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'

So, two solutions to this:

+ _Always_ score the dependents when the independents change;
+ But if the evaluation process is slow, then just more code carefully around the null problem.


### Code

That said, say hello to my little friend:

<a href="optimize.py#L158-L200"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   class Model:
   2:     def name(i): 
   3:       return i.__class__.__name__
   4:     def __init__(i):
   5:       "Initialize the generators and loggers."
   6:       i.of = i.spec()
   7:       i.log= o(x= [of1.log() for of1 in i.of.x],
   8:                y= [Num()     for _   in i.of.y])
   9:     def better(news,olds):
  10:       def worsed():
  11:         return  ((same     and not betterIqr) or 
  12:                  (not same and not betterMed))
  13:       def bettered():
  14:         return not same and betterMed
  15:       out = False
  16:       for new,old in zip(news.log.y, olds.log.y):
  17:         betterMed, same, betterIqr = new.better(old)
  18:         if worsed()  : return False # never any worsed
  19:         if bettered(): out= out or True # at least one bettered
  20:       return out
  21:     def cloneIT(i):
  22:       return i.__class__()
  23:     def indepIT(i):
  24:       "Make new it."
  25:       return o(x=[generate() for generate in i.of.x])
  26:     def depIT(i,it):
  27:       "Complete it's dep variables."
  28:       it.y = [generate(it) for generate in i.of.y]
  29:       return it
  30:     def logIT(i,it):
  31:       "Remember what we have see in it."
  32:       for val,log in zip(it.x, i.log.x): log += val
  33:       for val,log in zip(it.y, i.log.y): log += val
  34:     def aroundIT(i,it,p=0.5):
  35:       "Find some place around it."
  36:       def n(val,generate): 
  37:         return generate() if rand() < p else val
  38:       old = it.x
  39:       new = [n(x,generate) for 
  40:                          x,generate in zip(old,i.of.x)]
  41:       return o(x=new)
  42:     def ish(i,it):
  43:       return o(x= [of1.ish() for of1 in i.of.x])
```

Given the above, it is now very succinct to specify
a _Model_. For example, here's a model with 30 independent
variables and 2 dependent ones:

    class ZDT1(Model):
      def spec(i):
        return o(x= [In(0,1,z) for z in range(30)],
                 y= [i.f1,i.f2])
      def f1(i,it):
        return it.x[0]
      def f2(i,it):
        return 1 + 9*sum(it.x[1:]) / 29

Note that to completely understand the above
example you need to read up on the _In_ class
in [models.py](modelspy), But it is easy to get the general
idea: _In_ is something that ranges from zero to one.

## Optimization Control



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

