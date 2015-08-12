[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



## Basic Stuff

General utils- should be useful for all Python programs.

## Standard Header

````python
<font color=red>   1:</font> from __future__ import division
<font color=red>   2:</font> import sys, random, math, datetime, time,re
<font color=red>   3:</font> sys.dont_write_bytecode = True
````
## Misc Stuff

### Everyone needs a logo

````python
<font color=red>   4:</font> def logo():
<font color=red>   5:</font>   print """       
<font color=red>   6:</font>                                  _.      
<font color=red>   7:</font>                         _.-----'' `\ 
<font color=red>   8:</font>             __..-----'''            `.
<font color=red>   9:</font>            <            `\.           '\ 
<font color=red>  10:</font>            :.              `.           `\ 
<font color=red>  11:</font>             `:.              `.           `-.
<font color=red>  12:</font>               `:\ S  D     e   .             +.
<font color=red>  13:</font>                 `:. e  o  d     `.  __.===::::;)
<font color=red>  14:</font>           r   B   `: c       ___.__>'::::::a:f/'
<font color=red>  15:</font>      e          a   `.  _,===:::=-'-=-\"\"\"''
<font color=red>  16:</font>  s      a  b         '-/:::''
<font color=red>  17:</font>                        ''
<font color=red>  18:</font>           c
<font color=red>  19:</font>   """
<font color=red>  20:</font>   print The.misc.copyleft
````

### Options Handling

Place to store things and stuff.

_IDIOM_: every time you run an optimizer, show a
dump of the options used in that run.  

_TRICK_: store the options in a nested anonymous
container.

````python
<font color=red>  21:</font> class o: 
<font color=red>  22:</font>   "Peter Norvig's trick for anonymous containers."
<font color=red>  23:</font>   def __init__(i,**d): i.__dict__.update(d)
````

For example, here are the options used in this code.

````python
<font color=red>  24:</font> def small(l)  : return (l[0]+l[1])*0.5
<font color=red>  25:</font> def medium(l) : return (l[1]+l[2])*0.5
<font color=red>  26:</font> def large(l)  : return (l[2]+l[3])*0.5
<font color=red>  27:</font> 
<font color=red>  28:</font> The= o(cache = 
<font color=red>  29:</font>           o(keep    = 128  # size of sample sace
<font color=red>  30:</font>            ,pending = 4
<font color=red>  31:</font>           ),
<font color=red>  32:</font>        sa =   
<font color=red>  33:</font>           o(cooling = 0.6  # cooling schedule
<font color=red>  34:</font>            ,kmax    = 1000 # max evals
<font color=red>  35:</font>            ,patience= 2000  # run for at least this long
<font color=red>  36:</font>            ,baseline= 100  # initial sample size 
<font color=red>  37:</font>           ),
<font color=red>  38:</font>        misc = 
<font color=red>  39:</font>           o(verbose = False # show stuff?
<font color=red>  40:</font>            ,epsilon = 1.01 # where is close, close enough
<font color=red>  41:</font>            ,seed    = 1    # random number seed
<font color=red>  42:</font>            ,era     = 100  # pause every end of era
<font color=red>  43:</font>            ,repeats = 30   # repeated run
<font color=red>  44:</font>             ,a12     = [0.56, 0.64, 0.71][0] # a12 threshold 
<font color=red>  45:</font>            ,early   = 5 # early stopping
<font color=red>  46:</font>            ,copyleft= """ SEARCH-BASED SE Tools
<font color=red>  47:</font>  (c) 2014, copyright BSD-3, Tim Menzies"""
<font color=red>  48:</font>           )
<font color=red>  49:</font>        )
````

Here's code to dump nested containers:

````python
<font color=red>  50:</font> def showd(d,lvl=0): 
<font color=red>  51:</font>   d = d if isinstance(d,dict) else d.__dict__
<font color=red>  52:</font>   after, line,gap = [], '', '    ' * lvl
<font color=red>  53:</font>   for k in sorted(d.keys()):
<font color=red>  54:</font>     if k[0] == "_": continue
<font color=red>  55:</font>     val = d[k]
<font color=red>  56:</font>     if isinstance(val,(dict,o)):
<font color=red>  57:</font>        after += [k]
<font color=red>  58:</font>     else:
<font color=red>  59:</font>       if callable(val):
<font color=red>  60:</font>         val = val.__name__
<font color=red>  61:</font>       line += (':%s %s ' % (k,val))
<font color=red>  62:</font>   print gap + line
<font color=red>  63:</font>   for k in after: 
<font color=red>  64:</font>       print gap + (':%s' % k)
<font color=red>  65:</font>       showd(d[k],lvl+1)
````

The above code displays _showd(The)_ as follows:

    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 

### Iterators ######################################

````python
<font color=red>  66:</font> def pairs(lst):
<font color=red>  67:</font>   last=lst[0]
<font color=red>  68:</font>   for i in lst[1:]:
<font color=red>  69:</font>     yield last,i
<font color=red>  70:</font>     last = i
````

### Timing Stuff

````python
<font color=red>  71:</font> def msecs(f):
<font color=red>  72:</font>   import time
<font color=red>  73:</font>   t1 = time.time()
<font color=red>  74:</font>   f()
<font color=red>  75:</font>   return (time.time() - t1) * 1000
````

### Random Stuff

````python
<font color=red>  76:</font> rand=  random.random # generate nums 0..1
<font color=red>  77:</font> any=   random.choice # pull any from list
<font color=red>  78:</font> 
<font color=red>  79:</font> def rseed(seed = None):
<font color=red>  80:</font>   seed = seed or The.misc.seed
<font color=red>  81:</font>   random.seed(seed) 
````

The above example shows a use of a global option.
Note that the following alternative for _rseed()_ 
would be buggy (since this alternate _rseed_ 
could very well use the 
_The.misc.seed_ known at load time and not some
seed you change at run time).

    def rseed(seed = The misc.seed): # do not
      random.seed(seed)              # do this

### Maths Stuff

````python
<font color=red>  82:</font> def log2(num): 
<font color=red>  83:</font>   "Log base 2 of number"
<font color=red>  84:</font>   return math.log(num)/math.log(2)
<font color=red>  85:</font> 
<font color=red>  86:</font> def norm(x,lo,hi):
<font color=red>  87:</font>   "Generate a num 0..1 for lo..hi"
<font color=red>  88:</font>   tmp = (x - lo) / (hi - lo + 0.00001) 
<font color=red>  89:</font>   return max(0,min(tmp,1))
<font color=red>  90:</font> 
<font color=red>  91:</font> def mron(x,lo,hi):
<font color=red>  92:</font>   "Generate a num 1..0 for lo..hi"
<font color=red>  93:</font>   return 1 - norm(x,lo,hi)
````

### Printing stuff

````python
<font color=red>  94:</font> def burp(*lst):  
<font color=red>  95:</font>   "If verbose enabled, print a list of things."
<font color=red>  96:</font>   The.misc.verbose and say(
<font color=red>  97:</font>     ', '.join(map(str,lst)))
<font color=red>  98:</font> 
<font color=red>  99:</font> nl="\n"
<font color=red> 100:</font> def says(*lst):
<font color=red> 101:</font>   say(' '.join(map(str,lst)))
<font color=red> 102:</font> 
<font color=red> 103:</font> def say(x): 
<font color=red> 104:</font>   "Print something with no trailing new line."
<font color=red> 105:</font>   sys.stdout.write(str(x)); sys.stdout.flush()
<font color=red> 106:</font> 
<font color=red> 107:</font> def gn(lst,n):
<font color=red> 108:</font>   "Function to print floats in short form"
<font color=red> 109:</font>   fmt = '%.' + str(n) + 'f'
<font color=red> 110:</font>   return ', '.join([(fmt % x) for x in lst])
<font color=red> 111:</font> 
<font color=red> 112:</font> def x(n):
<font color=red> 113:</font>   "Shorthand for short floats"
<font color=red> 114:</font>   return ':%3.1f' % n
````

The following convenience functions print a list
of floats to  0, 2, or 3 decimal places (useful for condensing old reports).

````python
<font color=red> 115:</font> def g0(lst): return gn(lst,0)
<font color=red> 116:</font> def g2(lst): return gn(lst,2)
<font color=red> 117:</font> def g3(lst): return gn(lst,3)
````

### Printing a xtile chart.

````python
<font color=red> 118:</font> def xtile(lst,lo=0,hi=0.001,width=50,
<font color=red> 119:</font>              chops=[0.1 ,0.3,0.5,0.7,0.9],
<font color=red> 120:</font>              marks=["-" ," "," ","-"," "],
<font color=red> 121:</font>              bar="|",star="*",show=" %3.0f"):
<font color=red> 122:</font>   """The function _xtile_ takes a list of (possibly)
<font color=red> 123:</font>   unsorted numbers and presents them as a horizontal
<font color=red> 124:</font>   xtile chart (in ascii format). The default is a 
<font color=red> 125:</font>   contracted _quintile_ that shows the 
<font color=red> 126:</font>   10,30,50,70,90 breaks in the data (but this can be 
<font color=red> 127:</font>   changed- see the optional flags of the function).
<font color=red> 128:</font>   """
<font color=red> 129:</font>   def pos(p)   : return ordered[int(len(lst)*p)]
<font color=red> 130:</font>   def place(x) : 
<font color=red> 131:</font>     return int(width*float((x - lo))/(hi - lo))
<font color=red> 132:</font>   def pretty(lst) : 
<font color=red> 133:</font>     return ', '.join([show % x for x in lst])
<font color=red> 134:</font>   ordered = sorted(lst)
<font color=red> 135:</font>   lo      = min(lo,ordered[0])
<font color=red> 136:</font>   hi      = max(hi,ordered[-1])
<font color=red> 137:</font>   what    = [pos(p)   for p in chops]
<font color=red> 138:</font>   where   = [place(n) for n in  what]
<font color=red> 139:</font>   out     = [" "] * width
<font color=red> 140:</font>   for one,two in pairs(where):
<font color=red> 141:</font>     for i in range(one,two): 
<font color=red> 142:</font>       out[i] = marks[0]
<font color=red> 143:</font>     marks = marks[1:]
<font color=red> 144:</font>   out[int(width/2)]    = bar
<font color=red> 145:</font>   out[place(pos(0.5))] = star 
<font color=red> 146:</font>   return ''.join(out) +  "," +  pretty(what)
````

For example, the example displays 1000 random numbers as follows:

    ---   *     |------      , 0.01,  0.15,  0.26,  0.52,  0.79

````python
<font color=red> 147:</font> def _tileX() :
<font color=red> 148:</font>   import random
<font color=red> 149:</font>   random.seed(1)
<font color=red> 150:</font>   nums = [random.random()**2 for _ in range(100)]
<font color=red> 151:</font>   print xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f")
````

## Coercion

````python
<font color=red> 152:</font> def atom(x):
<font color=red> 153:</font>   "String to number."
<font color=red> 154:</font>   try : return int(x)
<font color=red> 155:</font>   except ValueError:
<font color=red> 156:</font>     try : return float(x)
<font color=red> 157:</font>     except ValueError: return x
````

### Command line processing ########################

The following code lets you call any function with keyword
defaults.

For example, consider the following function:

````python
<font color=red> 158:</font> 
<font color=red> 159:</font> def cmdDemo(who='Tim', when=2015, where='Raleigh'):
<font color=red> 160:</font>   says(':who',who,':when',when,':where',where,nl)
<font color=red> 161:</font> 
````
If this function is in a file with the last line:

    if __name__ == "__main__": eval(cmd())

Then this function can be called as follows:

    % python base.py  when 2010 who Jane

this would print 

    $ python base.py cmdDemo when 1990 who Jane
    :who Jane :when 1990 :where Raleigh 

Note that the arguments are supplied in a different
order to those seen in the function header.  Also,
if you do not mention some argument, it is filled in
from the function defaults.

````python
<font color=red> 162:</font> def cmd(com='logo()'):
<font color=red> 163:</font>   "Convert command line to a function call."
<font color=red> 164:</font>   if len(sys.argv) < 2: return com
<font color=red> 165:</font>   def strp(x): return isinstance(x,basestring)
<font color=red> 166:</font>   def wrap(x): return "'%s'"%x if strp(atom(x)) else str(x)  
<font color=red> 167:</font>   thing=None; chars=""; sep=""; keyp=True
<font color=red> 168:</font>   for word in sys.argv[2:]:
<font color=red> 169:</font>     if keyp:
<font color=red> 170:</font>       thing = word
<font color=red> 171:</font>     else:
<font color=red> 172:</font>       chars = chars+sep+thing+' = '+wrap(word)+' '
<font color=red> 173:</font>       sep = ","
<font color=red> 174:</font>     keyp = not keyp
<font color=red> 175:</font>   chars = sys.argv[1] + '( **dict(' + chars + '))'
<font color=red> 176:</font>   return chars
<font color=red> 177:</font> 
<font color=red> 178:</font> def cmdDemo(who='Tim', when=2015, where='Raleigh'):
<font color=red> 179:</font>   says(':who',who,':when',when,':where',where,nl)
<font color=red> 180:</font> 
<font color=red> 181:</font> if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

