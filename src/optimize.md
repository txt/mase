[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


<p><em>View <a href="optimize.py">source code</a>.</em></p>

## Optimize

### Standard Header

````python
   1:   from __future__ import division
   2:   import sys, random, math, datetime, time,re
   3:   sys.dont_write_bytecode = True
   4:   
   5:   from log  import *
````


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

````python
   6:   def study(f):
   7:     def wrapper(**lst):
   8:       rseed() # reset the seed to our default
   9:       what = f.__name__# print the function name
  10:       doc  = f.__doc__ # print the function doc
  11:       if doc:
  12:         doc= re.sub(r"\n[ \t]*","\n# ",doc)
  13:       # print when this ran
  14:       show = datetime.datetime.now().strftime
  15:       print "\n###",what,"#" * 50
  16:       print "#", show("%Y-%m-%d %H:%M:%S")
  17:       if doc: print "#",doc
  18:       t1 = time.time()
  19:       f(**lst)          # run the function
  20:       t2 = time.time() # show how long it took to run
  21:       print "\n" + ("-" * 72)
  22:       showd(The)       # print the options
  23:       print "\n# Runtime: %.3f secs" % (t2-t1)
  24:     return wrapper
````

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

````python
  25:   class Model:
  26:     def name(i): 
  27:       return i.__class__.__name__
  28:     def __init__(i):
  29:       "Initialize the generators and loggers."
  30:       i.of = i.spec()
  31:       i.log= o(x= [of1.log() for of1 in i.of.x],
  32:                y= [Num()     for _   in i.of.y])
  33:     def better(news,olds):
  34:       def worsed():
  35:         return  ((same     and not betterIqr) or 
  36:                  (not same and not betterMed))
  37:       def bettered():
  38:         return not same and betterMed
  39:       out = False
  40:       for new,old in zip(news.log.y, olds.log.y):
  41:         betterMed, same, betterIqr = new.better(old)
  42:         if worsed()  : return False # never any worsed
  43:         if bettered(): out= out or True # at least one bettered
  44:       return out
  45:     def cloneIT(i):
  46:       return i.__class__()
  47:     def indepIT(i):
  48:       "Make new it."
  49:       return o(x=[generate() for generate in i.of.x])
  50:     def depIT(i,it):
  51:       "Complete it's dep variables."
  52:       it.y = [generate(it) for generate in i.of.y]
  53:       return it
  54:     def logIT(i,it):
  55:       "Remember what we have see in it."
  56:       for val,log in zip(it.x, i.log.x): log += val
  57:       for val,log in zip(it.y, i.log.y): log += val
  58:     def aroundIT(i,it,p=0.5):
  59:       "Find some place around it."
  60:       def n(val,generate): 
  61:         return generate() if rand() < p else val
  62:       old = it.x
  63:       new = [n(x,generate) for 
  64:                          x,generate in zip(old,i.of.x)]
  65:       return o(x=new)
  66:     def ish(i,it):
  67:       return o(x= [of1.ish() for of1 in i.of.x])
````

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

````python
  68:   class Watch(object):
  69:     def __iter__(i): 
  70:       return i
  71:     def __init__(i,model,history=None):
  72:       i.early   = The.misc.early  
  73:       i.history = {} if history == None else history
  74:       i.log     = {}
  75:       i.most, i.model = The.sa.kmax, model
  76:       i.step, i.era  = 1,1
  77:     def logIT(i,result):
  78:       """ Each recorded result is one clock tick.
  79:           Record all results in log and history"""
  80:       both = [i.history, i.log]     
  81:       for log in both:
  82:         if not i.era in log:
  83:           log[i.era] = i.model.cloneIT()
  84:       i.step += 1
  85:       for log in both:
  86:         log[i.era].logIT(result)
  87:     def stop(i):
  88:       """if more than two eras, suggest
  89:          stopping if no improvement."""
  90:       if len(i.log) >= The.misc.early:
  91:         #print 3
  92:         now = i.era
  93:         before = now - The.misc.era
  94:         beforeLog = i.log[before]
  95:         nowLog    = i.log[now]
  96:         if not nowLog.better(beforeLog):
  97:           #print 4
  98:           return True
  99:       return False
 100:     def next(i):
 101:       "return next time tick, unless we need to halt."
 102:       if i.step > i.most: # end of run!
 103:         raise StopIteration()
 104:       if i.step >= i.era:   # pause to reflect
 105:         #print 1, i.step, i.era
 106:         if i.early > 0:     # maybe exit early
 107:           #print 2
 108:           if i.stop():        
 109:              raise StopIteration()
 110:         i.era += The.misc.era   # set next pause point
 111:       return i.step,i
 112:   
 113:   def optimizeReport(m,history):
 114:     for z,header in enumerate(m.log.y):
 115:       print "\nf%s" % z
 116:       for era in sorted(history.keys()):
 117:         log = history[era].log.y[z]
 118:         log.has()
 119:         print str(era-1).rjust(7),\
 120:               xtile(log._cache,
 121:                     width=33,
 122:                     show="%5.2f",
 123:                     lo=0,hi=1)
 124:   
 125:   if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

