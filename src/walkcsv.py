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
def FROM(x):
  if isinstance(x,tuple):
    return ZIP(zipped,file)
  return FILE(x) if x[-4:] == ".csv" else STRING(x)
  
def STRING(str):
  def wrapper():
    for c in str: yield c
  return wrapper

def ZIP(zipped,file): 
  def wrapper():
    with zipfile.ZipFile(zipfile,'r') as z:
      with z.open(file) as f:
        for line in f:
          for ch in line:
            yield ch
          yield "\n"
  return wrapper

def FILE(filename, buffer_size=4096):
  def chunks(filename):
    with open(filename, "rb") as fp:
      chunk = fp.read(buffer_size)
      while chunk:
        yield chunk
        chunk = fp.read(buffer_size)
  def wrapper():
    for chunk in chunks(filename):
      for char in chunk:
        yield char
  return wrapper
"""

## Iterators

"""
def lines(src):
  "Yield each line in a string"
  tmp=''
  for ch in src(): # sneaky... src can evaluate to different ghings
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch # for a (slightly) faster method,
                # in Python3, see http://goo.gl/LvgGx3
  if tmp:
    yield tmp

def rows(src):
  """Yield all non-blank lines,joining lines that end in ','.
   Defined using 'lines'."""
  b4 = ''
  for line in lines(src):
    line = re.sub(r"[\r\t ]*","",line)
    line = re.sub(r"#.*","",line)
    if not line: continue # skip blanks
    if line[-1] == ',':   # maybe, continue lines
      b4 += line
    else:
      yield b4 + line
      b4 = ''
      
def values(src):
  """Coerce row values to floats, ints or strings. 
     Jump over any cols we are ignoring.
     Defined using the 'rows' function. """
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
    
