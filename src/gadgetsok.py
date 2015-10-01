from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
print("""
########################################################################
#                    __                  __                   __         
#                   /\ \                /\ \__               /\ \        
#    __      __     \_\ \     __      __\ \ ,_\   ____    ___\ \ \/'\    
#  /'_ `\  /'__`\   /'_` \  /'_ `\  /'__`\ \ \/  /',__\  / __`\ \ , <    
# /\ \L\ \/\ \L\.\_/\ \L\ \/\ \L\ \/\  __/\ \ \_/\__, `\/\ \L\ \ \ \\`\  
# \ \____ \ \__/.\_\ \___,_\ \____ \ \____\\ \__\/\____/\ \____/\ \_\ \_\ 
#  \/___L\ \/__/\/_/\/__,_ /\/___L\ \/____/ \/__/\/___/  \/___/  \/_/\/_/
#    /\____/                  /\____/                                    
#    \_/__/                   \_/__/                                     
#                                                                  
#########################################################################""")
# This is free and unencumbered software released into
# the public domain.
# (c) Tim Menzies 2015, http://menzies.us
#
# Anyone is free to copy, modify, publish, use,
# compile, sell, or distribute this software, either
# in source code form or as a compiled binary, for any
# purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the
# author or authors of this software dedicate any and
# all copyright interest in the software to the public
# domain. We make this dedication for the benefit of
# the public at large and to the detriment of our
# heirs and successors. We intend this dedication to
# be an overt act of relinquishment in perpetuity of
# all present and future rights to this software under
# copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information, please refer to
# http://unlicense.org
#########################################################

"""

# Test suite for some generic optimizer gadgets

"""
from ok import *
from gadgets import *

@ok
def _seed():
  seed(1)
  assert 0.134364244111 < r() < 0.134364244113 

  
@ok
def _xtileX() :
  import random
  seed(1)
  nums1 = [r()**2 for _ in range(100)]
  nums2 = [r()**0.5 for _ in range(100)]
  for nums in [nums1,nums2]:
    print(xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f"))




@ok
def _log():
  with study("log",
             use(SOMES,size=10)):
    log = Log()
    [log + y for y in
     shuffle([x for x in xrange(20)])]
    assert log.lo==0
    assert log.hi==19
    print(sorted(log.some()))
    print(sorted(log.some()))
    assert sorted(log.some()) == [1, 6, 9, 11, 12,
                                  13, 14, 15, 16, 19]
    
  # after the study, all the defaults are
  # back to zero
  assert the.SOMES.size == 256


@ok
def _fill1():
  b4 = Schaffer([1],[1,2])
  assert str(b4.clone()) ==  \
    "Schaffer{'objs': [None], " + \
    "'aggregated': None, 'decs': [None, None]}"

@ok
def _fill2():
  b4 = Schaffer()
  assert b4.clone().__class__ == Schaffer

@ok
def _want():
  with study("log",
             use(SOMES,size=10)):
    for klass in [Less,More]:
      z = klass("fred",lo=0,hi=10)
      guess = [z.guess() for _ in xrange(20)]
      log = Log(guess)
      assert z.restrain(20) == 10
      assert z.wrap(15) == 5
      assert not z.ok(12)
      assert z.ok(8)
      print("\n"+klass.__name__)
      show(sorted(log.some()))
      show(map(lambda n: z.fromHell(n,log),
               sorted(log.some())))
  
@ok
def _gadgets1(f=Schaffer):
  with study(f.__name__,
             use(MISC,
                 tiles=[0.05,0.1,0.2,0.4,0.8])):
    g=Gadgets(f())
    log = g.logs()
    g.logNews(log, g.news())
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
def _gadgets4(): _gadgets1(ZDT1)

@ok
def _mutate():
  for m in [0.3,0.6]:
    with study("mutate",
               use(GADGETS,mutate=m)):
      g=Gadgets(Kursawe())
      log =g.logs()
      g.logNews(log,
                g.news(100))
      one = g.decs()
      two = g.mutate(one,log,the.GADGETS.mutate)
      print(m, r5(one.decs))
      print(m, r5(two.decs))


            
@ok
def _opt(m=Schaffer,optimizer=sa):
  def show(txt,what,all):
    all = sorted(all)
    lo, hi = all[0], all[-1]
    print("##",txt,xtile(what,lo=lo,hi=hi,width=25,show=" %6.2f"),m.__class__.__name__)
  with study(m.__name__,
             use(GADGETS,
                 verbose=True),
             use(MISC,
                 tiles=[0,   0.1,0.3 ,0.5,0.7,0.99],
                 marks=["0" ,"1", "3","5","7","!"])):
    m = m()
    firsts,lasts=optimizer(m)
    for first,last,name in zip(firsts.objs,
                               lasts.objs,
                               m.objs):
      all = first.some() + last.some()
      print("\n" + name.txt)
      show("FIRST:",first.some(),all)
      show("LAST :",last.some(), all)

def _de(m=Schaffer):
  _opt(m,de)


@ok
def _opt0(): _opt()
@ok
def _de0(): _de(Schaffer)

@ok
def _opt1(): _opt(Fonseca,sa)
@ok
def _de0(): _de(Fonseca)

@ok
def _opt2(): _opt(Kursawe)
@ok
def _de0(): _de(Kursawe)

@ok
def _opt3(): _opt(ZDT1)
@ok
def _de0(): _de(ZDT1)

@ok
def _opt4(): _opt(Viennet4)
@ok
def _de0(): _de(Viennet4)

@ok
def _threeOthers():
  seed(1)
  lst = list('abcdefg')
  print(another3(lst,'a'))


def opts(optimizers,models,n=2):
  def report(lst,what):
     print("",', '.join(map(str,r2(lst))),
           model.__name__,
           what,
           sep=", ")
  tiles=[0.25,0.50,0.75]
  print("#"," "*(n-2),r5(tiles))
  for model in models:
    shown=False
    for opt in optimizers:
      seed()
      firsts = Log()
      lasts  = Log()
      for i in xrange(n):
        say(".")
        m = model()
        g = Gadgets(m)
        baseline = g.news(the.GADGETS.baseline)
        with study(opt.__name__,use(GADGETS,
                                    verbose=False),
                   verbose=False):
          first,last = opt(m,baseline)
          firsts.adds( first.aggregate.some() )
          lasts.adds(  last.aggregate.some() )
      if shown:
        report(firsts.stats(tiles),"baseline")
        say("."*n)
        shown = True
      report(lasts.stats(tiles),opt.__name__)
    print("")

            
@ok
def _opts():
  opts([sa,de],[Schaffer,Fonseca,Kursawe,ZDT1,Viennet4])



unittest.enough()    
