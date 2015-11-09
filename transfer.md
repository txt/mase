[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 


# Transfer Learning for Defect Prediction 

 * What's defect prediction? 
 * How to predict? 
 * Why transfer?
 * How to transfer? 
 
## What's defect prediction?

Human programmers are clever, but not flawless. Coding adds functionality, but also defects. Since prograrmning inherently introduces defects into program, it's important to test them before releasing.
![](https://github.com/txt/mase/blob/master/img/defect/bugs.png)

For software developers(bug creators), there're several tools to help you get rid of some bugs:
  * pylint (static code defect predictors)
  * py.test(unit test)
  * nose(unit test)
  * unittest(unit test)
  
For quality assurance(QA) team, software assessment budgets are finite while assesment effort increases exponentionally wrt. assesment effectiveness. For example, for black-box testing methods, a linear increase in the confidence C of finding defects can take expoentntially more effort. __So the standard practice is to apply the available resources on code sections that seem most critical(most bug-prone).__ 

We need a rig to predict which files, modules or classes are (probably) bug-prone before testing. (This is where) HERE defect predictor comes in!

## How to predict?

Menzies, T.; Greenwald, J.; Frank, A., ["Data Mining Static Code Attributes to Learn Defect Predictors,"](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4027145&tag=1) in Software Engineering, IEEE Transactions on , vol.33, no.1, pp.2-13, Jan. 2007

__What does prediction mean?__ Use historical data as the training data to train(fit) the data mining algorithm . When the new testing data comes in, we pass the data into the model to get the estimated label for this data.

![](https://github.com/txt/mase/blob/master/img/defect/attributes.png)

Here's a data set example.

![](https://github.com/txt/mase/blob/master/img/defect/data.png)


Example:

* training data set: ivy-1.1
* learner: CART, randomForests, Logistic Regresssion and so on.
* predicting data set: ivy-1.4

![](https://github.com/txt/mase/blob/master/img/defect/WPDP.png)

Such defect predictors are easy to use, widely-used, and useful.

* easy to use: static code attributes can be automatically collected, even for very large systems.
* widely used: researchers and industrial practitioners use static attibutes to guide software quality predictors(NASA).
* useful: defect precitors often find the location of 70% (or more) defects in the code.


## Why transfer?

The above paradigm is useful when the training and testing(predition) datasets are available within the same project. 

__What if we want to predict defects on a new project with few/no historical information? How to get training data sets.__ Can we use:

* data sets from different projects (within the same organization) with the same attributes
* or data sets from different projects with different attributes
* or data sets from different organization

What is the relationship between training and testing data?

## How to transfer?

Nam, Jaechang, and Sunghun Kim. "[Heterogeneous defect prediction](http://lifove.net/research/files/HDP_FSE2015.pdf)." Proceedings of the 2015 10th Joint Meeting on Foundations of Software Engineering. ACM, 2015.


Key idea: __Synonym discovery__
Given a target(testing) data set, we have to find the appropriate traning set to build the learner. Here "__appropiate__" means the distribution of the source(training) set should be "the __most__ simialr" to the target(testing) data set.


Assumption: Training and testing data sets are from different projects with different attributes.

![](https://github.com/txt/mase/blob/master/img/defect/framework.png)



STEPS:

* Metric(attribute) selection: applying metric selection technique to the source.
	* feature selection is a common method used in data minning for selecting a subset of features by removing redundant and irrelevant features
	* e.g. grain ratio, chi-square, relief-F methods
	* Top 15% metrics are selected
* Metirc(attribute) matching
	* metrics based on their similarity such as distribution or correlation between source and taret metrics are mached together.
	* Percentile based matching
	* Kolmogorov-Smirnov Test based matching
	* Spearman's correlation based matching
	 	
* Prediction: after we get best matched source and target metric sets, we can build learners with the source data set and predict the label of target data sets.

![](https://github.com/txt/mase/blob/master/img/defect/datasets.png)

Details:
  
  * KS test is a non-parameteric two sample test that can be applicable when we are not sure abou the normality of two samples. In defect prediction data sets, some features have exponential distribution and others are unkown. using KS test, we can find the best matched source-target attributes.
  * For each target data set, we compare all the source data sets except for itself and the source data set with the highest score will be selected as the training data for this testing data.


## How about Performance?

![](https://github.com/txt/mase/blob/master/img/defect/result.png)


_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

