[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Review2: Week of Sept 5

##  Practice

### 1. Iterators

1a. The following code has a bug. The countdown stops at 10 (no 9,8,7...). Why?

```python
def countdown(n):
   while n >= 0:
     return  n
     n -= 1

print("We are go for launch")
for x in countdown(10):
   print(x)
print("lift off!")
```

1b. Modify the following code such that the final `out` list
only contains numbers over 20

```python
def items(x, depth=-1):
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y, depth+1):
        yield z
  else:
  yield _,x

out = []
for _,x in items(  [10,[ 20,30],
                        40,
                        [   (  50,60,70),
                            [  80,90,100],110]]):
   out += [x]
return out
``` 

1c. Repeat the above, this time using _list comprehensions_.

1d. Using list comprehensions, write a function that returns only non-whitespace
in a string. Hint:

```python
import string
string.whitespace # <== contains all whitespace chars
```

1e. Using list comprehensions and the following code,
return all lines in a multi-line
strings that  are (a) non-blanks and (b) longer than 20
lines. Hints: `not str` returns `True` for non empty strings.

```python
def lines(string):
  tmp=''
  for ch in string: 
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch 
  if tmp:
  yield tmp
```
  
### 2. Dunders

2a. What is a dunder method?

2b. What are the dunders in the following code? For each one,
use them in a code snippet.

```
class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
```

2c. What would happen if the _last line_ in the following `__iadd__` method
was deleted?

```python
r = random.random
rseed = random.seed

class Some:
  def __init__(i, max=8): 
    i.n, i.any, i.max = 0,[],max
  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:    
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x 
    return i
```	


2d. In English, explain what the above code does. 



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

