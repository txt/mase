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

<a href="walkcsv.py#L21-L46"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

   1:   def lines(x):
   2:     def strings(str):
   3:       tmp=""
   4:       for ch in str: 
   5:         if ch == "\n":
   6:           yield tmp
   7:           tmp = ''
   8:         else:
   9:           tmp += ch 
  10:       if tmp:
  11:         yield tmp
  12:     def zips((zipfile,file)):
  13:       with zipfile.ZipFile(zipfile,'r') as z:
  14:         with z.open(file) as f:
  15:           for line in f:
  16:             yield line
  17:     def files(filename):
  18:       with open(filename) as f:
  19:         for line in f:
  20:           yield line.replace("\n", "") 
  21:     # ---------------------------------
  22:     if   isinstance(x,tuple) : f=zips
  23:     elif x[-4:]==".csv"      : f=files
  24:     else                     : f=strings
  25:     for line in f(x):
  26:       yield line
```

## Iterators

<a href="walkcsv.py#L52-L86"><img align=right src="http://www.hungarianreference.com/i/arrow_out.gif"></a><br clear=all>
```python

  27:   def rows(src):
  28:     "Yield all non-blank lines,joining lines that end in ','."
  29:     b4 = ''
  30:     for line in src:
  31:       line = re.sub(r"[\r\t ]*","",line)
  32:       line = re.sub(r"#.*","",line)
  33:       if not line: continue # skip blanks
  34:       if line[-1] == ',':   # maybe, continue lines
  35:         b4 += line
  36:       else:
  37:         yield b4 + line
  38:         b4 = ''
  39:         
  40:   def cols(src):
  41:     """Coerce row values to floats, ints or strings. 
  42:        Jump over any cols we are ignoring."""
  43:     def make(x):
  44:       try   : return int(x)
  45:       except:
  46:         try   : return float(x)
  47:         except: return x
  48:     want = None
  49:     for row in rows(src):
  50:       lst  = row.split(',')
  51:       want = want or [col for col in xrange(len(lst))
  52:                       if lst[col][0] != "?" ]
  53:       yield [ make(lst[col]) for col in want ]
  54:   
  55:   def headBody(src):
  56:     head=None
  57:     for cells in cols(src):
  58:       if head:
  59:         return head,cells
  60:       else:
  61:         head = cells
```


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

