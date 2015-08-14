from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from ok import *
import random

r   = random.random
isa = isinstance
"""
 
# Compartmental Modeling


## Diapers

 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 
C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers

"""
class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def has(i)             : return i.__dict__
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
      
class Has:
  def __init__(i,init,lo=0,hi=100):
    i.init,i.lo,i.hi = init,lo,hi
  def restrain(i,x):
    return max(i.lo, 
               min(i.hi, x))
  def rank(i):
    if isa(i,Flow) : return 3
    if isa(i,Stock): return 1
    if isa(i,Aux)  : return 2
  def __repr__(i):
    return str(dict(what=i.__class__.__name__,
                name= i.name,init= i.init,
                 lo  = i.lo,  hi  = i.hi))
                 

class Flow(Has) : pass
class Stock(Has): pass
class Aux(Has)  : pass

F,S,A=Flow,Stock,Aux

class Model:
  def about(i):
    tmp=i.have()
    for k,v in tmp.has().items():
      v.name = k
    return tmp 
  def run(i,dt=1,tmax=100): 
    print(r())
    t,u, keep  = 0, o(), []
    about = i.about()
    keys  = sorted(about.keys, 
                   key=lambda z:z.rank())
    print(keys)
    for k,a in about.items(): 
      u[k] = a.init
    keep = [["t"] +  keys,
            [0] + about.asList(u,keys)]
    while t < tmax:
      v = copy(u)
      i.step(dt,t,u,v)
      for k in about: 
        v[k] = about[k].restrain(v[k])
      keep += [[dt] + about.asList(u,keys)]
      t += dt
    return keep
      
class Diapers(Model):
  def have(i):
    return o(C = S(20), D = S(0),
             q = F(0),  r = F(8), s = F(0))
  def step(i,dt,t,u,v):
    def saturday(x): return int(x) % 7 == 6
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70  if saturday(t) else 0 
    v.s  =  u.D if saturday(t) else 0
    if t == 27: # special case (the day i forget)
      v.s = 0

@ok
def _diapers1():
  print(Diapers().about())