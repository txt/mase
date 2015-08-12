[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## Optimize

### Standard Header

````python
<font color=red>   1:</font> from __future__ import division
<font color=red>   2:</font> import sys, random, math, datetime, time,re
<font color=red>   3:</font> sys.dont_write_bytecode = True
<font color=red>   4:</font> 
<font color=red>   5:</font> from log  import *
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
<font color=red>   6:</font> def study(f):
<font color=red>   7:</font>   def wrapper(**lst):
<font color=red>   8:</font>     rseed() # reset the seed to our default
<font color=red>   9:</font>     what = f.__name__# print the function name
<font color=red>  10:</font>     doc  = f.__doc__ # print the function doc
<font color=red>  11:</font>     if doc:
<font color=red>  12:</font>       doc= re.sub(r"\n[ \t]*","\n# ",doc)
<font color=red>  13:</font>     # print when this ran
<font color=red>  14:</font>     show = datetime.datetime.now().strftime
<font color=red>  15:</font>     print "\n###",what,"#" * 50
<font color=red>  16:</font>     print "#", show("%Y-%m-%d %H:%M:%S")
<font color=red>  17:</font>     if doc: print "#",doc
<font color=red>  18:</font>     t1 = time.time()
<font color=red>  19:</font>     f(**lst)          # run the function
<font color=red>  20:</font>     t2 = time.time() # show how long it took to run
<font color=red>  21:</font>     print "\n" + ("-" * 72)
<font color=red>  22:</font>     showd(The)       # print the options
<font color=red>  23:</font>     print "\n# Runtime: %.3f secs" % (t2-t1)
<font color=red>  24:</font>   return wrapper
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
<font color=red>  25:</font> class Model:
<font color=red>  26:</font>   def name(i): 
<font color=red>  27:</font>     return i.__class__.__name__
<font color=red>  28:</font>   def __init__(i):
<font color=red>  29:</font>     "Initialize the generators and loggers."
<font color=red>  30:</font>     i.of = i.spec()
<font color=red>  31:</font>     i.log= o(x= [of1.log() for of1 in i.of.x],
<font color=red>  32:</font>              y= [Num()     for _   in i.of.y])
<font color=red>  33:</font>   def better(news,olds):
<font color=red>  34:</font>     def worsed():
<font color=red>  35:</font>       return  ((same     and not betterIqr) or 
<font color=red>  36:</font>                (not same and not betterMed))
<font color=red>  37:</font>     def bettered():
<font color=red>  38:</font>       return not same and betterMed
<font color=red>  39:</font>     out = False
<font color=red>  40:</font>     for new,old in zip(news.log.y, olds.log.y):
<font color=red>  41:</font>       betterMed, same, betterIqr = new.better(old)
<font color=red>  42:</font>       if worsed()  : return False # never any worsed
<font color=red>  43:</font>       if bettered(): out= out or True # at least one bettered
<font color=red>  44:</font>     return out
<font color=red>  45:</font>   def cloneIT(i):
<font color=red>  46:</font>     return i.__class__()
<font color=red>  47:</font>   def indepIT(i):
<font color=red>  48:</font>     "Make new it."
<font color=red>  49:</font>     return o(x=[generate() for generate in i.of.x])
<font color=red>  50:</font>   def depIT(i,it):
<font color=red>  51:</font>     "Complete it's dep variables."
<font color=red>  52:</font>     it.y = [generate(it) for generate in i.of.y]
<font color=red>  53:</font>     return it
<font color=red>  54:</font>   def logIT(i,it):
<font color=red>  55:</font>     "Remember what we have see in it."
<font color=red>  56:</font>     for val,log in zip(it.x, i.log.x): log += val
<font color=red>  57:</font>     for val,log in zip(it.y, i.log.y): log += val
<font color=red>  58:</font>   def aroundIT(i,it,p=0.5):
<font color=red>  59:</font>     "Find some place around it."
<font color=red>  60:</font>     def n(val,generate): 
<font color=red>  61:</font>       return generate() if rand() < p else val
<font color=red>  62:</font>     old = it.x
<font color=red>  63:</font>     new = [n(x,generate) for 
<font color=red>  64:</font>                        x,generate in zip(old,i.of.x)]
<font color=red>  65:</font>     return o(x=new)
<font color=red>  66:</font>   def ish(i,it):
<font color=red>  67:</font>     return o(x= [of1.ish() for of1 in i.of.x])
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
<font color=red>  68:</font> class Watch(object):
<font color=red>  69:</font>   def __iter__(i): 
<font color=red>  70:</font>     return i
<font color=red>  71:</font>   def __init__(i,model,history=None):
<font color=red>  72:</font>     i.early   = The.misc.early  
<font color=red>  73:</font>     i.history = {} if history == None else history
<font color=red>  74:</font>     i.log     = {}
<font color=red>  75:</font>     i.most, i.model = The.sa.kmax, model
<font color=red>  76:</font>     i.step, i.era  = 1,1
<font color=red>  77:</font>   def logIT(i,result):
<font color=red>  78:</font>     """ Each recorded result is one clock tick.
<font color=red>  79:</font>         Record all results in log and history"""
<font color=red>  80:</font>     both = [i.history, i.log]     
<font color=red>  81:</font>     for log in both:
<font color=red>  82:</font>       if not i.era in log:
<font color=red>  83:</font>         log[i.era] = i.model.cloneIT()
<font color=red>  84:</font>     i.step += 1
<font color=red>  85:</font>     for log in both:
<font color=red>  86:</font>       log[i.era].logIT(result)
<font color=red>  87:</font>   def stop(i):
<font color=red>  88:</font>     """if more than two eras, suggest
<font color=red>  89:</font>        stopping if no improvement."""
<font color=red>  90:</font>     if len(i.log) >= The.misc.early:
<font color=red>  91:</font>       #print 3
<font color=red>  92:</font>       now = i.era
<font color=red>  93:</font>       before = now - The.misc.era
<font color=red>  94:</font>       beforeLog = i.log[before]
<font color=red>  95:</font>       nowLog    = i.log[now]
<font color=red>  96:</font>       if not nowLog.better(beforeLog):
<font color=red>  97:</font>         #print 4
<font color=red>  98:</font>         return True
<font color=red>  99:</font>     return False
<font color=red> 100:</font>   def next(i):
<font color=red> 101:</font>     "return next time tick, unless we need to halt."
<font color=red> 102:</font>     if i.step > i.most: # end of run!
<font color=red> 103:</font>       raise StopIteration()
<font color=red> 104:</font>     if i.step >= i.era:   # pause to reflect
<font color=red> 105:</font>       #print 1, i.step, i.era
<font color=red> 106:</font>       if i.early > 0:     # maybe exit early
<font color=red> 107:</font>         #print 2
<font color=red> 108:</font>         if i.stop():        
<font color=red> 109:</font>            raise StopIteration()
<font color=red> 110:</font>       i.era += The.misc.era   # set next pause point
<font color=red> 111:</font>     return i.step,i
<font color=red> 112:</font> 
<font color=red> 113:</font> def optimizeReport(m,history):
<font color=red> 114:</font>   for z,header in enumerate(m.log.y):
<font color=red> 115:</font>     print "\nf%s" % z
<font color=red> 116:</font>     for era in sorted(history.keys()):
<font color=red> 117:</font>       log = history[era].log.y[z]
<font color=red> 118:</font>       log.has()
<font color=red> 119:</font>       print str(era-1).rjust(7),\
<font color=red> 120:</font>             xtile(log._cache,
<font color=red> 121:</font>                   width=33,
<font color=red> 122:</font>                   show="%5.2f",
<font color=red> 123:</font>                   lo=0,hi=1)
<font color=red> 124:</font> 
<font color=red> 125:</font> if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

