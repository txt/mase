
from table import *

def model0(name, x=[],y=[]):
  def ok(row): return True
  return o(name=name,x=x,y=y,ok=ok)


def schaffer():
  def f1(row): x=row[0]; return x**2
  def f2(row): x= row[0]; return (x-2)**2
  return model('Schaffer',
               x=[Num('x1',lo = -10**5,hi = 10**5)],
               y=[f1,f2])

def fonseca():
  def f1(row): 1-e**
