[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


<a href="base.py"><img width=100 align=right src="https://raw.githubusercontent.com/txt/mase/master/img/py.png"></a>

## Basic Stuff

General utils- should be useful for all Python programs.

## Standard Header

````python
   1:   from __future__ import division
   2:   import sys, random, math, datetime, time,re
   3:   sys.dont_write_bytecode = True
````
## Misc Stuff

### Everyone needs a logo

````python
   4:   def logo():
   5:     print """       
   6:                                    _.      
   7:                           _.-----'' `\ 
   8:               __..-----'''            `.
   9:              <            `\.           '\ 
  10:              :.              `.           `\ 
  11:               `:.              `.           `-.
  12:                 `:\ S  D     e   .             +.
  13:                   `:. e  o  d     `.  __.===::::;)
  14:             r   B   `: c       ___.__>'::::::a:f/'
  15:        e          a   `.  _,===:::=-'-=-\"\"\"''
  16:    s      a  b         '-/:::''
  17:                          ''
  18:             c
  19:     """
  20:     print The.misc.copyleft
````

### Options Handling

Place to store things and stuff.

_IDIOM_: every time you run an optimizer, show a
dump of the options used in that run.  

_TRICK_: store the options in a nested anonymous
container.

````python
  21:   class o: 
  22:     "Peter Norvig's trick for anonymous containers."
  23:     def __init__(i,**d): i.__dict__.update(d)
````

For example, here are the options used in this code.

````python
  24:   def small(l)  : return (l[0]+l[1])*0.5
  25:   def medium(l) : return (l[1]+l[2])*0.5
  26:   def large(l)  : return (l[2]+l[3])*0.5
  27:   
  28:   The= o(cache = 
  29:             o(keep    = 128  # size of sample sace
  30:              ,pending = 4
  31:             ),
  32:          sa =   
  33:             o(cooling = 0.6  # cooling schedule
  34:              ,kmax    = 1000 # max evals
  35:              ,patience= 2000  # run for at least this long
  36:              ,baseline= 100  # initial sample size 
  37:             ),
  38:          misc = 
  39:             o(verbose = False # show stuff?
  40:              ,epsilon = 1.01 # where is close, close enough
  41:              ,seed    = 1    # random number seed
  42:              ,era     = 100  # pause every end of era
  43:              ,repeats = 30   # repeated run
  44:               ,a12     = [0.56, 0.64, 0.71][0] # a12 threshold 
  45:              ,early   = 5 # early stopping
  46:              ,copyleft= """ SEARCH-BASED SE Tools
  47:    (c) 2014, copyright BSD-3, Tim Menzies"""
  48:             )
  49:          )
````

Here's code to dump nested containers:

````python
  50:   def showd(d,lvl=0): 
  51:     d = d if isinstance(d,dict) else d.__dict__
  52:     after, line,gap = [], '', '    ' * lvl
  53:     for k in sorted(d.keys()):
  54:       if k[0] == "_": continue
  55:       val = d[k]
  56:       if isinstance(val,(dict,o)):
  57:          after += [k]
  58:       else:
  59:         if callable(val):
  60:           val = val.__name__
  61:         line += (':%s %s ' % (k,val))
  62:     print gap + line
  63:     for k in after: 
  64:         print gap + (':%s' % k)
  65:         showd(d[k],lvl+1)
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
  66:   def pairs(lst):
  67:     last=lst[0]
  68:     for i in lst[1:]:
  69:       yield last,i
  70:       last = i
````

### Timing Stuff

````python
  71:   def msecs(f):
  72:     import time
  73:     t1 = time.time()
  74:     f()
  75:     return (time.time() - t1) * 1000
````

### Random Stuff

````python
  76:   rand=  random.random # generate nums 0..1
  77:   any=   random.choice # pull any from list
  78:   
  79:   def rseed(seed = None):
  80:     seed = seed or The.misc.seed
  81:     random.seed(seed) 
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
  82:   def log2(num): 
  83:     "Log base 2 of number"
  84:     return math.log(num)/math.log(2)
  85:   
  86:   def norm(x,lo,hi):
  87:     "Generate a num 0..1 for lo..hi"
  88:     tmp = (x - lo) / (hi - lo + 0.00001) 
  89:     return max(0,min(tmp,1))
  90:   
  91:   def mron(x,lo,hi):
  92:     "Generate a num 1..0 for lo..hi"
  93:     return 1 - norm(x,lo,hi)
````

### Printing stuff

````python
  94:   def burp(*lst):  
  95:     "If verbose enabled, print a list of things."
  96:     The.misc.verbose and say(
  97:       ', '.join(map(str,lst)))
  98:   
  99:   nl="\n"
 100:   def says(*lst):
 101:     say(' '.join(map(str,lst)))
 102:   
 103:   def say(x): 
 104:     "Print something with no trailing new line."
 105:     sys.stdout.write(str(x)); sys.stdout.flush()
 106:   
 107:   def gn(lst,n):
 108:     "Function to print floats in short form"
 109:     fmt = '%.' + str(n) + 'f'
 110:     return ', '.join([(fmt % x) for x in lst])
 111:   
 112:   def x(n):
 113:     "Shorthand for short floats"
 114:     return ':%3.1f' % n
````

The following convenience functions print a list
of floats to  0, 2, or 3 decimal places (useful for condensing old reports).

````python
 115:   def g0(lst): return gn(lst,0)
 116:   def g2(lst): return gn(lst,2)
 117:   def g3(lst): return gn(lst,3)
````

### Printing a xtile chart.

````python
 118:   def xtile(lst,lo=0,hi=0.001,width=50,
 119:                chops=[0.1 ,0.3,0.5,0.7,0.9],
 120:                marks=["-" ," "," ","-"," "],
 121:                bar="|",star="*",show=" %3.0f"):
 122:     """The function _xtile_ takes a list of (possibly)
 123:     unsorted numbers and presents them as a horizontal
 124:     xtile chart (in ascii format). The default is a 
 125:     contracted _quintile_ that shows the 
 126:     10,30,50,70,90 breaks in the data (but this can be 
 127:     changed- see the optional flags of the function).
 128:     """
 129:     def pos(p)   : return ordered[int(len(lst)*p)]
 130:     def place(x) : 
 131:       return int(width*float((x - lo))/(hi - lo))
 132:     def pretty(lst) : 
 133:       return ', '.join([show % x for x in lst])
 134:     ordered = sorted(lst)
 135:     lo      = min(lo,ordered[0])
 136:     hi      = max(hi,ordered[-1])
 137:     what    = [pos(p)   for p in chops]
 138:     where   = [place(n) for n in  what]
 139:     out     = [" "] * width
 140:     for one,two in pairs(where):
 141:       for i in range(one,two): 
 142:         out[i] = marks[0]
 143:       marks = marks[1:]
 144:     out[int(width/2)]    = bar
 145:     out[place(pos(0.5))] = star 
 146:     return ''.join(out) +  "," +  pretty(what)
````

For example, the example displays 1000 random numbers as follows:

    ---   *     |------      , 0.01,  0.15,  0.26,  0.52,  0.79

````python
 147:   def _tileX() :
 148:     import random
 149:     random.seed(1)
 150:     nums = [random.random()**2 for _ in range(100)]
 151:     print xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f")
````

## Coercion

````python
 152:   def atom(x):
 153:     "String to number."
 154:     try : return int(x)
 155:     except ValueError:
 156:       try : return float(x)
 157:       except ValueError: return x
````

### Command line processing ########################

The following code lets you call any function with keyword
defaults.

For example, consider the following function:

````python
 158:   
 159:   def cmdDemo(who='Tim', when=2015, where='Raleigh'):
 160:     says(':who',who,':when',when,':where',where,nl)
 161:   
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
 162:   def cmd(com='logo()'):
 163:     "Convert command line to a function call."
 164:     if len(sys.argv) < 2: return com
 165:     def strp(x): return isinstance(x,basestring)
 166:     def wrap(x): return "'%s'"%x if strp(atom(x)) else str(x)  
 167:     thing=None; chars=""; sep=""; keyp=True
 168:     for word in sys.argv[2:]:
 169:       if keyp:
 170:         thing = word
 171:       else:
 172:         chars = chars+sep+thing+' = '+wrap(word)+' '
 173:         sep = ","
 174:       keyp = not keyp
 175:     chars = sys.argv[1] + '( **dict(' + chars + '))'
 176:     return chars
 177:   
 178:   def cmdDemo(who='Tim', when=2015, where='Raleigh'):
 179:     says(':who',who,':when',when,':where',where,nl)
 180:   
 181:   if __name__ == "__main__": eval(cmd())
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

