[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Unit tests in Python

Python has some great unit testing tools. The one
shown below is a "less-is-more" approach and is
based on [Kent Beck video on how to write a test engine in just a 
few lines of code](https://www.youtube.com/watch?v=nIonZ6-4nuU).

For example usages, see [okok.py](okok.md) which can be loaded via

```
python okok.py
```

Share and enjoy.

````python
<font color=red>   1:</font> 
<font color=red>   2:</font> def ok(*lst):
<font color=red>   3:</font>   print "### ",lst[0].__name__
<font color=red>   4:</font>   for one in lst: unittest(one)
<font color=red>   5:</font>   return one
<font color=red>   6:</font> 
<font color=red>   7:</font> class unittest:
<font color=red>   8:</font>   tries = fails = 0  #  tracks the record so far
<font color=red>   9:</font>   @staticmethod
<font color=red>  10:</font>   def score():
<font color=red>  11:</font>     t = unittest.tries
<font color=red>  12:</font>     f = unittest.fails
<font color=red>  13:</font>     return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
<font color=red>  14:</font>       t,f,int(round(t*100/(t+f+0.001))))
<font color=red>  15:</font>   def __init__(i,test):
<font color=red>  16:</font>     unittest.tries += 1
<font color=red>  17:</font>     try:
<font color=red>  18:</font>       test()
<font color=red>  19:</font>     except Exception,e:
<font color=red>  20:</font>       unittest.fails += 1
<font color=red>  21:</font>       i.report(test)
<font color=red>  22:</font>   def report(i,test):
<font color=red>  23:</font>     import traceback
<font color=red>  24:</font>     print traceback.format_exc()
<font color=red>  25:</font>     print unittest.score(),':',test.__name__
<font color=red>  26:</font> 
<font color=red>  27:</font>     
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

