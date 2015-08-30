from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True

"""

# demos 101

"""

def isSorted(lst):
  one=lst[0]
  for two in lst[1:]:
    if one >= two:
      return False
    one = two
  return True

def ntiles(lst, tiles=None,ordered=True):
  "Return percentiles in a list"
  tiles = tiles or [0.1,0.3,0.5,0.7,0.9]
  if not ordered:
    print("sorting!")
    lst = sorted(lst)
  at  = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]



