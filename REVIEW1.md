[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Review1: Week of Aug 25

## Theory

Can you define the following?

1. Evolutionary algorithms
   1. Genetic algorithms
   1. Genetic programsming
1. Evolutionary programs 101
   1. Mutation
      1. Can u give examples of GA mutation? of GP mutation?
  1. Crossover
	  1. Can u give examples of GA crossover? of GP crossover
  1. Selection
    1. Binary domination
    1. Pareto frontier (hint a diagram is good here)
      1. spread
      1. hypervolume

____

1. Optimizing optimizers <img align=right width=400 src="http://snag.gy/Cdatd.jpg">
   (not examinable)	  
   1. Writing models: understanding and representing a domain. Very slow
   1. Enabling models: getting them running. Not fast
   1. Running them
      1. _M:_ Mutation cost: making  _M_ mutants
      2. _E_: Evaluating _M_ mutants
	     1. If any random variables in the model, then _E*20_ to _E*100*_
	  3. _S_: Selecting cost: worst case _S=M<sup>2</sup>_ comparisons
	  4. _G_: Generations: _G_ times: mutate, select, crossover, repeat
   1. Verification cost:
      1. 20 (say) repeated runs, for many models,  for many optimizers
   1. Techniques (using data mining!)
      1. _M_ cost is low. just do it,
         1. Then feed into some incremental clustering algorithm ([mini-batch k-means](http://goo.gl/V8BQs),
	        [Genic](http://papers.rgrossman.com/proc-079.pdf): [code](https://github.com/ai-se/timm/blob/ffc7071f133521014e69fc91c99aa9432510ffdb/genic.py#L5))
		 1. <img align=right src="http://snag.gy/41kWD.jpg" width=400>	Then only keep (say) a few examples per cluster, selected randomly,
		    
	   1. _E_ reductions:
	     1. In each cluster, find a handful of most different examples and just evaluate those  	 
	   1. _S_ reduction:
	     1. YOur _M_ reductions have also reduced your 	  _S=M<sup>2</sup>_ effort
	   1. _G_ remains. consider "near enough is good enough"

____

1. Simulated annealing
   1. When to use SA
   1. Why random jumps?
   2. What is the cooling schedule?
      1. Why slow cooling? (when you jump less and less)
   1. When to stop
   1. Aggregation functions
      1. brittle aggregation functions

## Practice

For each of the following, can you offer a 3 line code snippet to demo
the idea?

1. Classes
1. Functions
1. Decorators
1. Static variables, functions
1. Scope
  1. nested scope
1. functions
  1. default params
  1. variable lists args
  1. variable dictionary args
  1. lambda bodies
1. list comprehensions
1. decorators


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

