[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[At a glance...](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Lecturer](http://menzies.us) 



# Syllabus

CSC 591-001 (13007)   
CSC 791-001 (7046)

NcState, ComSci
Fall 2015

EE I, Roon 1007, Tuesday, Thursday, 5:20 to 6:35.

### Overview

**Synopsis:** What is the next "big thing" after "big data"? Well, after "data collection" comes "model construction" so the next big thing after big data will be "big modeling". In this subject, students will learn how to represent, execute, and reason about models. Our case studies will come from software engineering but the principles of this subject could be applied to models in general.

**Objectives:** By the end of the course, students should be able to:
 
+ Read and understand the state of the art in research on Automated Software Engineering
+ Analyze and critique core principles of software engineering.
+ Build models that execute those core principles. 
+ Predict and explain and optimize the behavior of those models.
+ Build and evaluate SBSE tools.
+ Analyze, critique, and communicate clearly the core theory and algorithms of multi-objective optimization


**Lecturer:** Tim Menzies <img
src="http://www.csc.ncsu.edu/enews/images/1770.jpg"
align=right
width=100>

+ Office Hours: Thursday, 3:30-5:00 and by request
+ Location of Office Hours: EE II room 3298 
+ E-Mail: tim.menzies@gmail.com 
  + Only use this email for private matters. All other class communication should be via the class news group,    listed below.
+ Phone: 304-376-2859
       + **Do not use** this number, except in the most dire of 
          circumstances (best way to contact me is via email).

**GTA:** Rahul Krishna <img
src="https://media.licdn.com/mpr/mpr/shrinknp_400_400/p/1/005/0a4/3d6/04b9ea9.jpg"
align=right
width=100>

+ E-mail: rkrish11@ncsu.edu
  + Only use this email for private matters. All other class communication should be via the class news group,    listed below.
+ Office mours: Friday 12pm to 2pm
+ Office location: rm 3231, EE II


**Group mailing list:** During term time, a group
mailing list will be established:

+ [https://groups.google.com/forum/#!forum/csx91](https://groups.google.com/forum/#!forum/csx91)
+ Which you can email at [csx91@googlegroups.comcsx91](mailto:csx91@googlegroups.com). Students are strongly encouraged to contribute their questions and answers to that shared resource.
+ Note that, for communication of a more private nature, contact the lecturer on the email shown above.

**Topics:** Overview, state of the research, automated software engineering; AI and software engineering; principles of model-based reasoning with a heavy focus on models about software engineering; search-based and evolutionary inference; representing and reasoning about models; handling uncertainty; decision making and model-based reasoning.



**Project:** Students will implement and reason about a large model of their own choosing (ideally, some model relating to software engineering). Note that:

+ CSC 791 Ph.d. student will each develop a   large model-based  SE application.
+ CSC 591 masters students will work in groups of three and may either do a large SE model-based app or
  three not-so-small mini-projects.

**Prerequisite:** Note that this is a
**programming-intensive** subject. A programming
background is required in a contemporary language
such as Java or C/C++ or Python. Hence,he
prerequisite for this class is 510, Software
Engineering. Significant software industry
experience may be substituted, at the instructor’s
discretion.  Students in this class will work in
Python, but no background knowledge of that language
will be assumed.

**Suggested texts:** (optional)
  [Think Python: How to Think Like a Computer Scientist](http://www.greenteapress.com/thinkpython/html/index.html)

+ Note: for low-level systems reasons, we will use
  Python 2.7 for this subject. So do not get the
  absolute latest version of this book.

**Expected Workload:** Some lectures will be pre-recorded, then discussed in the class
room. It is the responsibility of each student to:

+ View those recordings;
+ Come to class with notes on 
  + The concepts in those lecturers;
  + Plus their questions that arise from that material.

Sometimes, the lecturer/tutor will require you to attend a review session during their consultation  time. There, students may be asked to review
code, concepts, or comment on the structure of the course. Those sessions are mandatory and failure to attend will result in marks being deducted.

Also, this is tools-based subject
and it is required that students learn and use those
tools (Python, repositories, etc).  Students MUST be
prepared to dedicate AT LEAST 5-8 working hours a
week to this class (excluding the time spent in the
classroom). Laboratory instruction is not included
in this subject (but the first three weeks will be
spent on some in-depth programming tutorials). Note
that the workload for masters and Ph.D. students
will be different (see above).

**Grading:** The following grade scale will be used: 

+ A+  (97-100), A (93-96), A-(90-92)
+ B+ (87-89), B (83-86), B-(80-82)
+ C+ (77-79), C (73-76), C-(70-72)
+ D+ (67-69), D (63-66), D-(60-62)
+ F (below 60).

Grades will be added together using:

+ Homeworks: 18
+ Mid-term/final exam: 22/25
+ Paper (on the ASE literature): 15
+ Big programming project (on model-based SE): 20

### Homeworks 

+ All deliverables are group-based (one deliverable per group)
  + 591 students: groups of three
  + 791 students: groups of one
+ Homeworks will be written into a public Github repo which students will create.
+ Students will shorten the url (using something like goo.gl) of the the main file of each homework submission
    + That url wull be pasted into the spreadsheet https://goo.gl/qj3Akp. 
+ All homeworks will be marked ``1'', or ``0'';
+ Students cannot do homework <em>i+1</em> till  homework <em>i</em> gets at least a ``1''.
+ Homeworks can be submitted multiple times
  + No late penalties
  + No points taken off for repeat submissions
+ We will not mark more than four (coding) homeworks plus four (lit review) homeworks per month.


### Attendance

Attendance is extremely important for your learning
experience in this class. Once you reach three
unexcused absences, each additional absence will
reduce your attendance grade by 10%.

### Academic Integrity

Cheating will be punished to the full extent permitted. Cheating
includes plagerism of other people's work. All students will be working
on public code repositories and **informed reuse** is encouraged where
someone else's product is:

+ Imported and clearly acknowledged (as to where it came from);
+ The imported project is understood, and
+ The imported project is significantly extended.

Students are encouraged to read each others code and repor **uninformed reuse**
to the lecturer. The issue will be explored and, if uncovered,
cheating will be reported to the university
and marks will be deducted if the person who is doing the reuse:

+ Does not acknowledge the source of the product;
+ Does not exhibit comprehension of the product when asked about it;
+ Does not significantly extend the product.

All students are expected to maintain traditional
standards of academic integrity by giving proper
credit for all work.  All suspected cases of
academic dishonesty will be aggressively pursued.
You should be aware of the University policy on
academic integrity found in the Code of Student
Conduct.
 
The  exams will be done individually.  Academic integrity is important.  Do not work together on the exams: cheating on either will be punished to the full extent permitted.  

### Disabilities

Reasonable accommodations will be made for students
with verifiable disabilities. In order to take
advantage of available accommodations, students must
register with Disability Services for Students at
1900 Student Health Center, Campus Box 7509,
919-515-7653. For more information on NC State's
policy on working with students with disabilities,
please see the Academic Accommodations for Students
with Disabilities Regulation(REG 02.20.01).

Students are responsible for reviewing the PRRs
which pertain to their course rights and
responsibilities. These include:
http://policies.ncsu.edu/policy/pol-04-25-05 (Equal
Opportunity and Non-Discrimination Policy
Statement), http://oied.ncsu.edu/oied/policies.php
(Office for Institutional Equity and
Diversity),http://policies.ncsu.edu/policy/pol-11-35-01
(Code of Student Conduct), and
http://policies.ncsu.edu/regulation/reg-02-50-03
(Grades and Grade Point Average).

### Non-Discrimination Policy

NC State University provides equality of opportunity
in education and employment for all students and
employees. Accordingly, NC State affirms its
commitment to maintain a work environment for all
employees and an academic environment for all
students that is free from all forms of
discrimination. Discrimination based on race, color,
religion, creed, sex, national origin, age,
disability, veteran status, or sexual orientation is
a violation of state and federal law and/or NC State
University policy and will not be
tolerated. Harassment of any person (either in the
form of quid pro quo or creation of a hostile
environment) based on race, color, religion, creed,
sex, national origin, age, disability, veteran
status, or sexual orientation also is a violation of
state and federal law and/or NC State University
policy and will not be tolerated.

+ Note that, as a lecturer, I am legally required to
  **report** all such acts to the campus policy.

Retaliation
against any person who complains about
discrimination is also prohibited. NC State's
policies and regulations covering discrimination,
harassment, and retaliation may be accessed at
http://policies.ncsu.edu/policy/pol-04-25-05 or
http://www.ncsu.edu/equal_op/. Any person who feels
that he or she has been the subject of prohibited
discrimination, harassment, or retaliation should
contact the Office for Equal Opportunity (OEO) at
919-515-3148.

### Other Information

Non-scheduled class time for field trips or
out-of-class activities are NOT required for this
class. No such trips are currently planned. However,
if they do happen then students are required to
purchase liability insurance. For more information,
see http://www2.acs.ncsu.edu/insurance/



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE.md).

