[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# demos 101

<a href="ntiles.py#L10-L29"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   
   2:   def isSorted(lst):
   3:     one=lst[0]
   4:     for two in lst[1:]:
   5:       if one >= two:
   6:         return False
   7:       one = two
   8:     return True
   9:   
  10:   def ntiles(lst, tiles=None,ordered=True):
  11:     "Return percentiles in a list"
  12:     tiles = tiles or [0.1,0.3,0.5,0.7,0.9]
  13:     if not ordered:
  14:       print("sorting!")
  15:       lst = sorted(lst)
  16:     at  = lambda x: lst[ int(len(lst)*x) ]
  17:     return [ at(tile) for tile in tiles ]
  18:   
  19:   
  20:   
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

