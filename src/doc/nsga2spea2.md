# NSGA-II, SPEA2

Problem: How to find cull many solutions, with multiple objectives

History: 1990s: NSGA, NPGA, MOGA

+ Sort according how often not dominated (nondominating sort)
+ Preserve diversity of solutions.
  + If a crowded part of the space, delete some
  + Elitism (to improve convergence)

All had some high computation times.


## NSGA-II (fast, approximate, non-dominating sort)

K. Deb, A. Pratap, S. Agarwal, and
T. Meyarivan. 2002.
[A fast and elitist multiobjective genetic algorithm: NSGA-II](http://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf). Trans. Evol. Comp
6, 2 (April 2002),
182-197. DOI=http://dx.doi.org/10.1109/4235.996017

Cited by: 15,300+ papers

A standard genetic algorithm (Crossover, mutation) with a state-of-the art selection operator for multi-objectives.

+ Divide candidates into _frontiers_:
+ For some small number:
  + Keep the top i-frontiers until we reach that number
  + If you fill up half way through a frontier,
  + Delete some using crowd-pruning

BUt how do you finds the bands? And what is crowd-pruning?

+ Patience. First, do you get the general idea?
+ Some fast primary ranking method to generate frontier1, frontier2, frontier3...
+ Keep frontier1, frontier2, frontier3... till frontieri gives you too many items
+ Sort frontieri by secondary ranking method, prune the lower ones

![nsgaii](img/nsgaii.png)

Primary rankings: sort by how many things you dominate:

+ Part one: find....
  + _n<sub>p</sub>_: number of candidates that dominate _p_ (the upstream counter)
  + _S<sub>p</sub>_: candidates dominated by _p_ (the downstream set)
  + _F<sub>1</sub>_: frontier 1 (the frontier of things dominated by no one) 
+ Part two...
   + For _P_ in frontier i
     + For everything _Q_ dominated by _P_
        + decrease the upstream counter by 1
	 + If upstream counter == 0
   	    + then _Q_ belongs in frontier i

![sort](img/sort.png)

Secondary ranking (only applied to the "too much"
frontier that cross "over the line").

Find an approximation to the cuboid space around around each
 candidate:

+ For each objective,
   + Sort the candidates on that objective
   + For each candidate _p_ in that "too much" frontier,
      + Find the _gap_ equal to the sum of the space
        _up_ and _down_ to the next candidate
      + Normalize _gap_  by the max-min in that objective.
      + Add _gap_ to _I<sub>p</sub>_
+ Sort candidates by _I<sub>p</sub>_
  + Discard the smaller ones. 

![cubioid](img/cuboid.png)
  

Officially faster. Strange to say, no runtimes in the famous
[NSGA-II paper](http://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf)

BYW, NSGA-II's author has recently released NSGA-II for _many_ objective problems

+ multi: 2,3,4
+ many: 5+

## SPEA2: Improving the Strength Pareto Evolutionary Algorithm

(The following notes come for the excellent website [Clever Algorithms](http://www.cleveralgorithms.com/nature-inspired/evolution/spea.html).)

SPEA2:
[Improving the Strength Pareto Evolutionary Algorithm for Multiobjective Optimization](http://e-collection.library.ethz.ch/eserv/eth:24689/eth-24689-01.pdf)
Eckart Zitzler, Marco Laumanns, Lothar Thiele,
Evolutionary Methods for Design, Optimization and
Control with Applications to Industrial
Problems. Proceedings of the
EUROGEN'2001. Athens. Greece, September 19-21

Cited by 4774.


Again, a genetic algorithm (crossover, mutate) with a novel select operator.

+ Worried about individuals dominated by the same candidate.
+ All individuals scored by the number of other people they dominate.
+ If individuals have identical score, resolve via reflection on local density.

Data structures:

+ _Population_: space of current mutants (build, somewhat, from the _Archive_).
+ _Archive_: a space of good ideas (usually smaller than _Population_; e.g. size/2).

Functions:


+ _CalculateRawFitness()_  number of solutions that a give solution dominate.
+ _CandidateDensity()_ estimates the density of local Pareto front
   +  Euclidean distance of the objective values to  the _K_ nearest neighbors (in objective space)
   + _K_ = sqrt( size(_Archive_) + size(_Population_) ) 
+ _PopulateWithRemainingBest()_  fills in  _Archive_  with remaining candidate solutions in order of fitness.
+ _RemoveMostSimilar()_  truncates _Archive_, removing  members with the smallest difference in their objective scores.
+ _SelectParents_: all pairs comparison, remove dominated ones


Algorithm:

![spea2](img/spea2.png)


## And which is Better?

![img](img/sayyad13.png)

