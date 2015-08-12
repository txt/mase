[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Examples of Unit tests  in Python

````python
<font color=red>   1:</font> import time
<font color=red>   2:</font> from ok import *
<font color=red>   3:</font> 
<font color=red>   4:</font> print time.strftime("%H:%M:%S\n")
<font color=red>   5:</font> 
<font color=red>   6:</font> @ok
<font color=red>   7:</font> def _ok1():
<font color=red>   8:</font>   assert 1==1
<font color=red>   9:</font> 
<font color=red>  10:</font> @ok
<font color=red>  11:</font> def _ok2():
<font color=red>  12:</font>   assert 2==1
<font color=red>  13:</font> 
<font color=red>  14:</font> @ok
<font color=red>  15:</font> def _ok3():
<font color=red>  16:</font>   assert 3==3 
<font color=red>  17:</font> 
<font color=red>  18:</font> @ok
<font color=red>  19:</font> def _ok4():
<font color=red>  20:</font>   assert unittest.tries==4
<font color=red>  21:</font>   assert unittest.fails==1
<font color=red>  22:</font>   print unittest.score() 
````


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

