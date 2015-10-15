from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
from ok import *
import random,re,sys
sys.dont_write_bytecode = True


class o:
  """Emulate Javascript's uber simple objects.."""
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)

the = o()

def setting(f):
  name = f.__name__
  def wrapper(**d):
    tmp = f()
    tmp.__dict__.update(d) 
    the[name] = tmp  
    return tmp
  wrapper() 
  return wrapper

r     = random.random
rseed = random.seed
gt    = lambda x,y: x > y
lt    = lambda x,y: x < y

def shuffle(lst):
  random.shuffle(lst)
  return lst


def eras(src, size=64):
  n=0
  size = size or 64
  lst = []
  for cells in src:
    lst += [cells]
    if len(lst) >= size:
      yield n,shuffle(lst)
      lst = []
      n += 1
  if lst:
    yield n,shuffle(lst)

class Some:
  "Keep some things."
  def __init__(i, keep=None): # note, usually 256 or 128 or 64 (if brave)
    i.keep = keep or the.COL.cache
    i.n, i.any  = 0,[]
  def add(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.keep:       
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x 
