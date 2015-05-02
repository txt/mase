[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[About](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Contact](http://menzies.us) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) 


# Boot test routines.

````python

from boot import * # get the test engine

@ok # run+test something at load time
def noop(): return True # never fails

@ok # ditto
def oops(): 1/0  # always fails

@ok # eg3: test the test engine
def unittestok():
  ok(oops,       # "ok" accepts multiple arguments
    noop,        # can be named functions
    lambda: 1+1, # or anonymous functions
    lambda: 1/0
    )
  ok(oops)       # ok can also run with 1 test
  ok(oops,noop)
  # note that, when runm we never see 'unitest fail'
  assert unittest.tries == 10, 'unit test fail'
  assert unittest.fails == 5,  'unit test fail'

print("\n"+"EXPECT...... # TRIES= 10 FAIL= 5 %PASS = 67%")
print("GOT.........",unittest.score())
````


_________

<img src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">  

Copyright © 2015 [Tim Menzies](http://menzies.us).


This is free and unencumbered software released into the public domain.

For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

