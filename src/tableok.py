#!/usr/bin/python
from __future__ import print_function, division

from table import *

@ok
def _tableok():
  t = readcsv("data/housing.csv")
  for row in t.rows:
    c= closest(row,t.rows,t)
    f= furthest(row,t.rows,t)
    say(".")
    assert dist(row,c,t) /  dist(row,f,t) < 0.3
  print("")
    
