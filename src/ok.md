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

<a href="ok.py#L19-L42"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def ok(*lst):
   2:     print "### ",lst[0].__name__
   3:     for one in lst: unittest(one)
   4:     return one
   5:   
   6:   class unittest:
   7:     tries = fails = 0  #  tracks the record so far
   8:     @staticmethod
   9:     def score():
  10:       t = unittest.tries
  11:       f = unittest.fails
  12:       return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
  13:         t,f,int(round(t*100/(t+f+0.001))))
  14:     def __init__(i,test):
  15:       unittest.tries += 1
  16:       try:
  17:         test()
  18:       except Exception,e:
  19:         unittest.fails += 1
  20:         i.report(test)
  21:     def report(i,test):
  22:       import traceback
  23:       print traceback.format_exc()
  24:       print unittest.score(),':',test.__name__
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

