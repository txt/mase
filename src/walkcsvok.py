from __future__ import print_function, division
from ok import *
import sys
sys.dont_write_bytecode = True

"""

# Testing WalkCsv

"""

from walkcsv import *

weather="""

outlook,
temperature,
humidity,?windy,play
sunny    , 85, 85, FALSE, no  # an interesting case
sunny    , 80, 90, TRUE , no
overcast , 83, 86, FALSE, yes
rainy    , 70, 96, FALSE, yes
rainy    , 68, 80, FALSE, yes
rainy    , 65, 70, TRUE , no
overcast , 64, 65, TRUE , 
yes
sunny    , 72, 95, FALSE, no

sunny    , 69, 70, FALSE, yes
rainy    , 75, 80, FALSE, yes
sunny    , 75, 70, TRUE , yes
overcast , 72, 90, TRUE , yes
overcast , 81, 75, FALSE, yes
rainy    , 71, 91, TRUE , no"""

@ok
def _line():
  for line in lines(weather):
    print("[",line,"]",sep="")

@ok
def _row():
  for row in rows(lines('weather.csv')):
    print("[",row,"]",sep="")

@ok
def _col():
  for cells in cols(lines(weather)):
    print(cells)
