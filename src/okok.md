[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Examples of Unit tests  in Python

<a href="okok.py#L6-L27"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   import time
   2:   from ok import *
   3:   
   4:   print time.strftime("%H:%M:%S\n")
   5:   
   6:   @ok
   7:   def _ok1():
   8:     assert 1==1
   9:   
  10:   @ok
  11:   def _ok2():
  12:     assert 2==1
  13:   
  14:   @ok
  15:   def _ok3():
  16:     assert 3==3 
  17:   
  18:   @ok
  19:   def _ok4():
  20:     assert unittest.tries==4
  21:     assert unittest.fails==1
  22:     print unittest.score() 
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

