"""

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

"""
def ok(*lst):
  print "### ",lst[0].__name__
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
      i.report(test)
  def report(i,test):
    import traceback
    print traceback.format_exc()
    print unittest.score(),':',test.__name__
