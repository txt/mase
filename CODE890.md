[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Code890: Final Project, cs591

Code8 and 9 are worth 6 marks each (plus 1 bonus for completing an extra homework).

Code10 is worth 6 marks.

Total: 20 marks.

## What to Hand in

For each of the following tasks, create a sub-directory called
CODE8, CODE9, CODE10 that includes:

+ All related python code
+ A README.md file containing your report.
+ Sub-directories CODEx/img for images; CODEx/data for data.

Using some URL shortener (e.g. goo.gl), shorten the URL to `hw/code/x`
and paste into [the submission page](https://goo.gl/lZEmEm).


## What to do

For each of the following,  write a Markdown readme.md file(1500 words+)
Note that there will be some overlap in the content
of these reports. Feel free to "borrow" text from
your earlier reports for your later reports-- ideally, improving the borrowed bits each time.

Your report must

+ Explain all algorithms it discussed (so I know that you know what is going on in them)
+ Succinctly describe the results. Not 1000 tables, but key insights relating to a small number of key displayed
  results
  + No figure should be used _unless_ it is discussed in the text;
  + No text should claim a result _unless_ there is an associated future.


Your report should be a [technical report](https://www.cg.tuwien.ac.at/resources/HowToWriteAScientificPaper.html).
For a list of sections of those reports, plus some tips, see

+ [here](http://cs.stanford.edu/people/widom/paper-writing.html)
+ and [here](https://www.cg.tuwien.ac.at/resources/HowToWriteAScientificPaper.html)
+ and [here](http://www.dgp.toronto.edu/~hertzman/advice/writing-technical-papers.pdf)

Two key parts of the reports are "threats to validity" and "future work". For notes on those sections, please see:

+ _[threats to validity](http://www.robertfeldt.net/publications/feldt_2010_validity_threats_in_ese_initial_survey.pdf)_
+ _[future work](https://guidetogradschoolsurvival.wordpress.com/2011/04/15/how-to-write-future-workconclusions-2/)_.
Note that the _better_ your future work section, the _better_ your mark. In future work,
      we really can see what your learned from the experience of this work-- what strange quirks
	  you have observered and what insights those quirks may bring.

## Code8


For DE and MWS and SA, code up the Type1,Type2, Type3 comparison operators and use them to:

+ Find the final era computed by DE, MWS, SA (with early termination)
+ Computer the _loss_ numbers between era0 the final era
     + Important implementation note: repeat the above with 20 different baseline populations. For each baseline, run DE,MWS,SA.

Apply the above for [DTLZ7](http://e-collection.library.ethz.ch/eserv/eth:24696/eth-24696-01.pdf)
with 2 objectives 10 decisions.

Using the statistical machinery discussed in class (Scott-Knott, a12, bootstrap) to decide in any of
DE, MWS, SA is best for this model. TO collect data, 20 times, generate a baseline population and for each
baseline, the run DE, MWS, SA from that baseline.

## Code9: A Simple Standard Genetic Algorithm

GAs mutate by swapping parts of daddy into parts of mummy

+ Defaults for mutation: at probability 5%
+ Defaults for crossover: one point (i.e. pick a random decision, take all dad's decisions up to that point, take alll mum's decisions after that point)
+ Defaults for select: for all pairs in the population, apply binary domination.
+ Defaults for number of candidates: 100
+ Defaults for number of generations: 1000 (but have early termination considered every 100 generations)


Do NOT analyze the result statistically, but offer succinct diagrams comparing the performance results
on 20 repeats of  [DTLZ1,3,5,7](http://e-collection.library.ethz.ch/eserv/eth:24696/eth-24696-01.pdf)
with 2,4,6,8 objectives and 10,20,40 decisions

## Code10: Hyper parameter optimization (hard)

Use DE to tune your defaults for GAs.

Create at least three options for mutation, crossover, select, number of candidates, number of generations.
See if  standard DE (default control settings) can improve on the scores seen in COde9.

Using the statistical machinery discussed in class (Scott-Knott, a12, bootstrap) to decide in any of
tuned or untuned GAs are best for
[DTLZ1,3,5,7](http://e-collection.library.ethz.ch/eserv/eth:24696/eth-24696-01.pdf)
with 2,4,6,8 objectives and 10,20,40 decisions. Remember to repeat your runs of tuned vs untuned using the
same baseline populations.


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

