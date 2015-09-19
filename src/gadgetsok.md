[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Test suite for a generic optimizer

<a href="gadgetsok.py#L10-L41"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   from ok import *
   2:   from gadgets import *
   3:   
   4:   @ok
   5:   def _seed():
   6:     seed(1)
   7:     assert 0.134364244111 < r() < 0.134364244113 
   8:   
   9:   @ok
  10:   def _log():
  11:     with study("log",
  12:                use(somes,size=10)):
  13:       log = Log()
  14:       [log + y for y in
  15:        shuffle([x for x in xrange(20)])]
  16:       assert log.lo==0
  17:       assert log.hi==19
  18:       assert log.some() == [9, 11, 13, 15, 6,
  19:                             19, 12, 14, 16, 1]
  20:     # after the study, all the defaults are
  21:     # back to zero
  22:     assert the.somes.size == 256
  23:   
  24:   @ok
  25:   def _fill():
  26:     b4 = Candidate([1,2],[2,4])
  27:     assert str(fill(b4)) ==  \
  28:            "o{'aggregate': None, "  + \
  29:            "'objs': [None, None], " + \
  30:            "'decs': [None, None]}"
  31:   
  32:   print(More('asd'))
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

