[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# showing off ntiles

<a href="ntilesok.py#L13-L32"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   
   2:   r = random.random
   3:   rseed = random.seed
   4:   
   5:   
   6:   @ok
   7:   def _ntiles():
   8:     r1  = [ r() for _ in xrange(1000)]
   9:     r2 = [ x**2 for x in r1]
  10:     print("\nlong",ntiles(r1,ordered=False))
  11:     print("\nshort",ntiles(r1,tiles=[0.25,0.5,0.75]))    
  12:     print("\nother",ntiles(r2))
  13:   
  14:   @ok
  15:   def _isSorted2():
  16:     assert isSorted([1,2,3])
  17:     assert isSorted([1,4,3]) 
  18:     
  19:     
  20:     
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

