from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from ok import *

import random
r   = random.random
isa = isinstance

class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def has(i)             : return i.__dict__
  def keys(i)            : return i.has().keys()
  def items(i)           : return i.has().items()
  def __init__(i,**d)    : i.has().update(d)
  def __setitem__(i,k,v) : i.has()[k] = v
  def __getitem__(i,k)   : return i.has()[k]
  def __repr__(i)        : return 'o'+str(i.has())
  def copy(i): 
      j = o()
      for k in i.has(): j[k] = i[k]
      return j
  def asList(i,keys=[]):
    keys = keys or i.keys()
    return [i[k] for k in keys]

def lt(i,j): return i < j
def gt(i,j): return i > j

class Has:
  def __init__(i,txt,init,lo=0,hi=100,):
    i.txt,i.init,i.lo,i.hi = txt,init,lo,hi
  def restrain(i,x):
    return max(i.lo, 
               min(i.hi, x))
  def __repr__(i):
    return str(dict(what=i.__class__.__name__,
                name= i.name,init= i.init,
                 lo  = i.lo,  hi  = i.hi))

class Model:
  def candidate():
    return o(decs=[], objs=[],
             scores=[], energy = None)
  def eval(i,c):
    if not c.scores:
      c.scores = [obj(c) for obj in i.objectives()] 
    if c.energy == None
      c.energy = i.energy(c.scores)
    return c

class Schaffer(Models):
  def f1(i,c):
    x=c.decs[0]
    return x**2
  def f2(i,c):
    x=c.decs[0]
    return (x-2)**2
  def objectives(i):
    return [i.f1,i.f2]
  
class ZDT1(Function):
  def f1(i,it):
    return it[0]
  def f2(i,it):
    g = 1 + 9 * sum(it[x] for x in range(30))/30
    return g * round(1- sqrt(it[0]/g))
  def objectives(i):
    return [i.f1,i.f2]
  def cells(i):
    d = dict(f1 = Has("f1",obj=i.f1,goal=lt,lo=0,hi=1),
             f2 = Has("f2",obj=i.f2,goal=lt,lo=0,hi=10))
    for x in xrange(30):
      d[str(x)] =  Aux(str(x),lo=0,hi=1,touch=True)
    return Have(**d)
