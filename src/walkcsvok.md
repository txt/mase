[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Testing WalkCsv

<a href="walkcsvok.py#L11-L49"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   
   2:   from walkcsv import *
   3:   
   4:   weather="""
   5:   
   6:   outlook,
   7:   temperature,
   8:   humidity,?windy,play
   9:   sunny    , 85, 85, FALSE, no  # an interesting case
  10:   sunny    , 80, 90, TRUE , no
  11:   overcast , 83, 86, FALSE, yes
  12:   rainy    , 70, 96, FALSE, yes
  13:   rainy    , 68, 80, FALSE, yes
  14:   rainy    , 65, 70, TRUE , no
  15:   overcast , 64, 65, TRUE , 
  16:   yes
  17:   sunny    , 72, 95, FALSE, no
  18:   
  19:   sunny    , 69, 70, FALSE, yes
  20:   rainy    , 75, 80, FALSE, yes
  21:   sunny    , 75, 70, TRUE , yes
  22:   overcast , 72, 90, TRUE , yes
  23:   overcast , 81, 75, FALSE, yes
  24:   rainy    , 71, 91, TRUE , no"""
  25:   
  26:   @ok
  27:   def _line():
  28:     for line in lines(weather):
  29:       print("[",line,"]",sep="")
  30:   
  31:   @ok
  32:   def _row():
  33:     for row in rows(lines('weather.csv')):
  34:       print("[",row,"]",sep="")
  35:   
  36:   @ok
  37:   def _col():
  38:     for cells in cols(lines(weather)):
  39:       print(cells)
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

