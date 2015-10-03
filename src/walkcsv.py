from __future__ import print_function, division
from ok import *
import zipfile,re,sys
sys.dont_write_bytecode = True

"""

# Iterators for Walking CSV Data

Can handing raw strings, files, zip files.

Assumes if lines end in ',' then that line continues to the next.

Also assumes first line is column names. 


## Handing Raw String, Files, Zip Files.

The function `FROM` returns iterators that can handle different kinds of data.

"""
def lines(x):
  def strings(str):
    tmp=""
    for ch in str: 
      if ch == "\n":
        yield tmp
        tmp = ''
      else:
        tmp += ch 
    if tmp:
      yield tmp
  def zips((zipfile,file)):
    with zipfile.ZipFile(zipfile,'r') as z:
      with z.open(file) as f:
        for line in f:
          yield line
  def files(filename):
    with open(filename) as f:
      for line in f:
        yield line.replace("\n", "") 
  # ---------------------------------
  if   isinstance(x,tuple) : f=zips
  elif x[-4:]==".csv"      : f=files
  else                     : f=strings
  for line in f(x):
    yield line
"""

## Iterators

"""
def rows(src):
  "Yield all non-blank lines,joining lines that end in ','."
  b4 = ''
  for line in src:
    line = re.sub(r"[\r\t ]*","",line)
    line = re.sub(r"#.*","",line)
    if not line: continue # skip blanks
    if line[-1] == ',':   # maybe, continue lines
      b4 += line
    else:
      yield b4 + line
      b4 = ''
      
def cols(src):
  """Coerce row values to floats, ints or strings. 
     Jump over any cols we are ignoring."""
  def make(x):
    try   : return int(x)
    except:
      try   : return float(x)
      except: return x
  want = None
  for row in rows(src):
    lst  = row.split(',')
    want = want or [col for col in xrange(len(lst))
                    if lst[col][0] != "?" ]
    yield [ make(lst[col]) for col in want ]
    
