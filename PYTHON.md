[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Overview](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Why Not Use Python3?

This code is based on Python 2.7. Why not use the latest Python3 and all
the amazing associated tools like PyPy, etc? Well...

Like many people, I have not jumped to Python3
since there are certain key libraries that have yet
to make it there. For me, its ScikitLearn which, in
turn, ias based on NumPy. At the time of this
writing, *some* parts of NumPy have made it to
Python3 but, sadly, not enough to let me use it
there.

But, to increase the odds of a successful future migration,
it is advised to use Python3 constructs in Python2. So the following
is highly recommended:

## Import from the Fugure.

Start your code with:

     from __future__ import print_function, unicode_literals
     from __future__ import absolute_import, division

Which changes a whole bunch of stuff such as:

+ Now we use `print(5)` and not `print 5`.
+ When we divide `5/2` we get 2.5 and not 2 (as in the old days).

## Avoid Older Idioms

E.g.

+ Use `k in d` instead of `d.has_key(k)`;
+ Use `d.values()` instead of `d.itervalues()`;
+ Use `hasattr(o, '__call__')` instead of `callable(o)`.

## Use `range` not `xrange`

Also, after including the above `import`s then...

     try:
        xrange = xrange # We have Python 2
     except:
        xrange = range # We have Python 3

## Check for Old Constructs

When running Python2 code, use:

     python -3

to check for code that may cause problems under Python3.

_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

