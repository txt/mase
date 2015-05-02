[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[About](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Contact](http://menzies.us) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md)  (for NcState students)

# Download sites for MOEA problems

## General models

+ Classic problems, now considered somewhat quaint, but good for debugging: [moeaProblems](models/moeaProblems.pdf),
+ CEC 2005  Special Session on  [REal-Parameter optimization](models/2005-25problems.pdf);
     + Example of their use in  a <a href="hansen08.pdf">parametric optimizer</a>
+ DTLZ and ZDT  are widely used. See 
  [http://jmetal.sourceforge.net/problems.html](http://jmetal.sourceforge.net/problems.html)

## SE models:

+ Next release problem
     + Assuming all requirements are independent [Section 4.1 and start of Section 7](http://crest.cs.ucl.ac.uk/fileadmin/crest/sebasepaper/ZhangHM07.pdf)
     + Otherwise: [See section 3,4,5.1](http://dl.acm.org/citation.cfm?id=2042264)
+ [Modeller](https://github.com/nave91/modeller)
     + [XOMOk](http://menzies.us/pdf/05xomo101.pdf): software project defects,
	          effort, time ,risk;
     + POM3: agile development:
	   <a href="models/pomNotes.pdf">notes</a>,
		   <a href="models/pomSampleOutput.pdf">sample output</a>
+ UML (warning- may be usable for search sicne they often lack constrainit
  or opinion or goal knowledge):
    + [Repository for Model Driven Development (ReMoDD)](http://remodd.org/): requires free registration)
    + [GenMyModel](https://repository.genmymodel.com/public/0) 
+ Feature map product lines (usually contain constraint knowledge).
    + [S.P.L.O.T.](http://www.splot-research.org/)
+ Constraint models
    + [Clafer](http://t3-necsis.cs.uwaterloo.ca:8091/)
+ Test suite generation:
     + Via [mutation operators](https://www.st.cs.uni-saarland.de/publications/files/fraser-issta-2010.pdf)
+ Roll your own:
    + Use evolutionary programs to tune params of 
      some auto-generated model; e.g. from a machine learner.
    + e.g. [Effort estimation tuning](models/icse14-v5-min.py)
         + Usage: _python icse14-v5-min.py N X M1 M2 M2..._
             + _N_: how many times to loop; e.g. 10
             + _X_: experiment; e.g. locOrNot
             + _M1, M2_: models; e.g. coc81
         + Test case (relative fast, just to see if it works)  
           _python icse14-v5-min.py 1 locOrNot coc81_
    


_________

<img src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">  

Copyright © 2015 [Tim Menzies](http://menzies.us).


This is free and unencumbered software released into the public domain.

For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

