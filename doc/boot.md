
[Home](https://github.com/txt/mase/blob/master/README.md) | [Contents](https://github.com/txt/mase/blob/master/TOC.md) | [About](https://github.com/txt/mase/blob/master/ABOUT.md) | [Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) | [Code](https://github.com/txt/mase/tree/master/src) [Contact](http://menzies.us)   
[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner.png">](https://github.com/txt/mase/blob/master/README.md)



# Boot: Core utilities

````python

import traceback

class o:
  def __init__(i,**d)    : i.add(**d)
  def d(i)               : return i.__dict__
  def add(i,**d)         : i.d().update(d);return i
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k] 

the = o()

def setting(f):
  name = f.__name__
  def wrapper(**d):
    tmp = the[name] = f().add(**d)
    return tmp
  wrapper()
  return wrapper

def ok(*lst):
  for one in lst: unittest(one)
  return one

class unittest:
  tries = fails = 0  #  tracks the record so far
  @staticmethod
  def score():
    t = unittest.tries
    f = unittest.fails
    return "# TRIES= %s FAIL= %s %%PASS = %s%%"  % (
      t,f,int(round(t*100/(t+f+0.001))))
  def __init__(i,test):
    unittest.tries += 1
    try:
      test()
    except Exception,e:
      unittest.fails += 1
      i.report(e,test)
  def report(i,e,test):
    print(traceback.format_exc())
    print(unittest.score(),':',test.__name__, e)
    
````

__________


![lic](img/license.png)

Copyright © 2015 [Tim Menzies](http://menzies.us), email: <tim.menzies@gmail.com>.

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

