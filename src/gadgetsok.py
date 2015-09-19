from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# Test suite for a generic optimizer

"""
from ok import *
from gadgets import *

@ok
def _seed():
  seed(1)
  assert 0.134364244111 < r() < 0.134364244113 

@ok
def _log():
  with study("log",
             use(SOMES,size=10)):
    log = Log()
    [log + y for y in
     shuffle([x for x in xrange(20)])]
    assert log.lo==0
    assert log.hi==19
    assert log.some() == [9, 11, 13, 15, 6,
                          19, 12, 14, 16, 1]
  # after the study, all the defaults are
  # back to zero
  assert the.SOMES.size == 256

@ok
def _fill():
  b4 = Candidate([1,2],[2,4])
  assert str(canCopy(b4)) ==  \
         "o{'aggregate': None, "  + \
         "'objs': [None, None], " + \
         "'decs': [None, None]}"

@ok
def _want():
  with study("log",
             use(SOMES,size=10)):
    for klass in [Less,More]:
      w = klass("fred",lo=0,hi=10)
      guess = [w.guess() for _ in xrange(20)]
      log = Log(guess)
      assert w.restrain(20) == 10
      assert w.wrap(15) == 5
      assert not w.ok(12)
      assert w.ok(8)
      show(sorted(log.some()))
      show(map(lambda n: w.fromHell(n,log),
               sorted(log.some())))

@ok
def _gadgets1(f=Schaffer):
  with study(f.__name__,
             use(MISC,
                 tiles=[0.05,0.1,0.2,0.4,0.8])):
    g=Gadgets(f())
    log = g.logs()
    g.baseline(log)
    print("aggregates:",
          log.aggregate.tiles())
    for whats in ['decs', 'objs']:
      print("")
      for n,what in enumerate(log[whats]):
        print(whats, n,what.tiles())

@ok
def _gadgets2(): _gadgets1(Fonseca)

@ok
def _gadgets3(): _gadgets1(Kursawe)

@ok
def _mutate():
  for m in [0.3,0.7]:
    with study("mutate",
               use(GADGETS,mutate=m)):
      g=Gadgets(Kursawe())
      one = g.decs()
      two = g.mutate(one)
      print(m, r5(one.decs))
      print(m, r5(two.decs))
