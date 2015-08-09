#!/usr/bin/python

from __future__ import print_function,division

from anywhere import *


seed(1)
for _ in range(10):
  anywhere("../data/housing.csv")
