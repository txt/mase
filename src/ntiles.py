from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# demos 101

"""

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
  "Return percentiles in a list"
  at  = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]
