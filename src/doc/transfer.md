# Transfer Defect Prediction 

 * What's defect prediction? 
 * How to predict? 
 * Why transfer?
 * How to transfer? 
 
## What's defect prediction?

Human programmers are clever, but flawed. Coding adds functionality, but also defects. Since prograrmning inherently introduces defects into program, it's important to test them before releasing.
![](https://github.com/txt/mase/blob/master/img/defect/bugs.png)

For software developers(bug creators), there're several tools to help you get rid of some bugs:
  * pylint (static code defect predictors)
  * py.test(unit test)
  * nose(unit test)
  * unittest(unit test)
  
For quality assurance(QA) team, software assessment budgets are finite while assessment effeectiveness increases exponentially iwth assessment effort. For example, for black-box testing methods, a linear increase in the confidence C of finding defecgts anca take expoentntially more effort. __So the standard practice is to apply the best available resources on code sections that seem most critical(most bug-prone).__ 

We need a rig to predict which files, modules or classes are bug-prone before testing. HERE defect predictor comes in!

## How to predict?

Menzies, T.; Greenwald, J.; Frank, A., ["Data Mining Static Code Attributes to Learn Defect Predictors,"](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4027145&tag=1) in Software Engineering, IEEE Transactions on , vol.33, no.1, pp.2-13, Jan. 2007

![](https://github.com/txt/mase/blob/master/img/defect/attributes.png)

Here's a data set example.

![](https://github.com/txt/mase/blob/master/img/defect/data.png)

Example:
training data set: ivy-1.1
learner: CART, randomForests, Logistic Regresssion and so on.
predicting data set: ivy-1.4

![](https://github.com/txt/mase/blob/master/img/defect/WPDP.png)

Such defect predictors are easy to use, widely-used, and useful to use.

* easy to use: static code attributes can be automatically collected, even for very large systems.
* widely used: researchers and industrial practitioners use sattic attibutes to guide software quality preditions(NASA).
* useful: defect precitors often find the locaiton of 70% (or more) defects in the code.


## Why transfer?

The above paradigm is useful when the training and testing(predition) data sets are different versions(releases)for the same project. __What if we want to predict defects on a new project with few historical information? How to get training data sets.__ Can we use:

* data sets from different projects with the same attributes
* or data sets form different projects with different attributes
* or data sets form different companies

Before answering that, what's fundamental theory of data mining? When using training data to train a data minign algorithm, what's the assumption here?

So, the answer is YES.

## How to transfer?



Key idea: Synonym discovery. Given a target(testing) data set, we have to find the appropriate traning set to build the learner. Here "__appropiate__" means the distribution of the source(training) set should be "the most simialr" to the target(testing) data set.


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
	 	
* Prediction: after we get matched source and target metric sets, we can build learners with the source data sets and predict the label of target data sets.













