from __future__ import print_function, division
import sys
sys.dont_write_bytecode = True
import random,re,sys

from ok import *
from smote0 import *
from walkcsv import *

@ok
def _eras():
  for chunk in eras(list('abcdefghijklmnop'), size=5):
    print(chunk)

@ok
def _xxx():
  for chunk in eras(cols(lines('weather.csv')),size=3):
    print(chunk)
