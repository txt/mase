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

  33:   def lines(src):
  34:     "Yield each line in a string"
  35:     tmp=''
  36:     for ch in src(): # sneaky... src can evaluate to different ghings
  37:       if ch == "\n":
  38:         yield tmp
  39:         tmp = ''
  40:       else:
  41:         tmp += ch # for a (slightly) faster method,
  42:                   # in Python3, see http://goo.gl/LvgGx3
  43:     if tmp:
  44:       yield tmp
  45:   
  46:   def rows(src):
  47:     """Yield all non-blank lines,joining lines that end in ','.
  48:      Defined using 'lines'."""
  49:     b4 = ''
  50:     for line in lines(src):
  51:       line = re.sub(r"[\r\t ]*","",line)
  52:       line = re.sub(r"#.*","",line)
  53:       if not line: continue # skip blanks
  54:       if line[-1] == ',':   # maybe, continue lines
  55:         b4 += line
  56:       else:
  57:         yield b4 + line
  58:         b4 = ''
  59:         
  60:   def values(src):
  61:     """Coerce row values to floats, ints or strings. 
  62:        Jump over any cols we are ignoring.
  63:        Defined using the 'rows' function. """
  64:     def make(x):
  65:       try   : return int(x)
  66:       except:
  67:         try   : return float(x)
  68:         except: return x
  69:     want = None
  70:     for row in rows(src):
  71:       lst  = row.split(',')
  72:       want = want or [col for col in xrange(len(lst))
  73:                       if lst[col][0] != "?" ]
  74:       yield [ make(lst[col]) for col in want ]
  75:       
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

