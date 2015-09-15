import sys
sys.dont_write_bytecode = True

class o:
  def __init__(i,**d): i.__dict__.update(d)
  def __repr__(i): return 'o'+str(i.__dict__)

run = o(seed=1)

sa = o(p=0.3)
