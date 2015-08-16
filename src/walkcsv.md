[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Iterators for Walking CSV Data

Can handing raw strings, files, zip files.

Assumes if lines end in ',' then that line continues to the next.

Also assumes first line is column names. 


## Handing Raw String, Files, Zip Files.

The function `FROM` returns iterators that can handle different kinds of data.

<a href="walkcsv.py#L22-L53"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def FROM(x):
   2:     if isinstance(x,tuple):
   3:       return ZIP(zipped,file)
   4:     return FILE(x) if x[-4:] == ".csv" else STRING(x)
   5:     
   6:   def STRING(str):
   7:     def wrapper():
   8:       for c in str: yield c
   9:     return wrapper
  10:   
  11:   def ZIP(zipped,file): 
  12:     def wrapper():
  13:       with zipfile.ZipFile(zipfile,'r') as z:
  14:         with z.open(file) as f:
  15:           for line in f:
  16:             for ch in line:
  17:               yield ch
  18:             yield "\n"
  19:     return wrapper
  20:   
  21:   def FILE(filename, buffer_size=4096):
  22:     def chunks(filename):
  23:       with open(filename, "rb") as fp:
  24:         chunk = fp.read(buffer_size)
  25:         while chunk:
  26:           yield chunk
  27:           chunk = fp.read(buffer_size)
  28:     def wrapper():
  29:       for chunk in chunks(filename):
  30:         for char in chunk:
  31:           yield char
  32:     return wrapper
```

## Iterators

<a href="walkcsv.py#L59-L101"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def lines(src):
   2:     "Yield each line in a string"
   3:     tmp=''
   4:     for ch in src(): # sneaky... src can evaluate to different ghings
   5:       if ch == "\n":
   6:         yield tmp
   7:         tmp = ''
   8:       else:
   9:         tmp += ch # for a (slightly) faster method,
  10:                   # in Python3, see http://goo.gl/LvgGx3
  11:     if tmp:
  12:       yield tmp
  13:   
  14:   def rows(src):
  15:     """Yield all non-blank lines,joining lines that end in ','.
  16:      Defined using 'lines'."""
  17:     b4 = ''
  18:     for line in lines(src):
  19:       line = re.sub(r"[\r\t ]*","",line)
  20:       line = re.sub(r"#.*","",line)
  21:       if not line: continue # skip blanks
  22:       if line[-1] == ',':   # maybe, continue lines
  23:         b4 += line
  24:       else:
  25:         yield b4 + line
  26:         b4 = ''
  27:         
  28:   def values(src):
  29:     """Coerce row values to floats, ints or strings. 
  30:        Jump over any cols we are ignoring.
  31:        Defined using the 'rows' function. """
  32:     def make(x):
  33:       try   : return int(x)
  34:       except:
  35:         try   : return float(x)
  36:         except: return x
  37:     want = None
  38:     for row in rows(src):
  39:       lst  = row.split(',')
  40:       want = want or [col for col in xrange(len(lst))
  41:                       if lst[col][0] != "?" ]
  42:       yield [ make(lst[col]) for col in want ]
  43:       
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

