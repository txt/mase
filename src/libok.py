#!/usr/bin/python
from __future__ import print_function,division
from lib import *

 
@ok
def _misc():
  assert isa({},dict)
  seed(1)
  assert round(r(),5) == 0.13436
  lst = list('abcdefghijklmnopqrstuvwxyz')
  assert 'w' == any(lst)         
  assert ['x','n','e','u'] == shuffle(lst)[:4]

@ok
def _meta():
  class Emp():
    def __init__(i,n,a):
      i.name,i.age = n,a
  def aFun(): return True
  assert not fun(1)
  assert fun(aFun)
  assert {'o': {'name':
                [1.222,
                 {'a': 1, 'b': 2},
                 {'Emp':
                  {'age': [3.143, 2.718],
                   'name': 1}},
                 {'o': {'b': 'tim', 'f': 22}}]}
          } == has(o(name=
                    [1.2222,dict(a=1,b=2),
                     Emp(1,
                         [22/7,1264/465]),
                     o(b='tim',f=22)]))

def fib(n):
  return n if n < 2 else fib(n-1) + fib(n-2)
      
@ok
def _duration():
  with study("fib",use(LIB, seed=5,decs=10)):
    fib(30)
  assert the.LIB.seed == 1
