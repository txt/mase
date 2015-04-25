#!/usr/bin/python
from __future__ import print_function
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
