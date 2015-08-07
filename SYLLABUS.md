[<img width=900 src="https://raw.githubusercontent.com/txt/mase/master/img/banner1.png">](https://github.com/txt/mase/blob/master/README.md)   
[Contents](https://github.com/txt/mase/blob/master/TOC.md) |
[At a glance](https://github.com/txt/mase/blob/master/OVERVIEW.md) |
[About](https://github.com/txt/mase/blob/master/ABOUT.md) |
[Models](https://github.com/txt/mase/blob/master/MODELS.md) |
[Code](https://github.com/txt/mase/tree/master/src) |
[Contact](http://menzies.us) |
[Syllabus](https://github.com/txt/mase/blob/master/SYLLABUS.md) 


# Syllabus: T

[[etc/img/leftarrow.png]]   [Back   to SBSE'14](Home)

# CSC 791-001 (14135)

## Fall 2014 

Search-Based Software Engineering:  Tu/Th  2:20-3:35

EE III, Roon 2220.

+ Lecturer: Tim Menzies
+ E-Mail: tim.menzies@gmail.com
+ Phone: 304-376-2859
       + **Do not use** this number, except in the most dire of 
          circumstances (best way to contact me is via email).
+ Office Hours: Thursday, 1:00-2:20 and by request
+ Location of Office Hours: EE II room 3298 

## Course Description 

This course introduces students to 	the growing field of search-based software engineering (SBSE). Like other engineering disciplines, SE is all about multi-objective optimization. We seek to build software systems that are better, faster, cheaper, more reliable, flexible, scalable, responsive, adaptive, maintainable, testable; the list of objectives for the software engineer is a long and diverse one, reflecting the breadth and diversity of applications to which software is put. The space of possible choices is enormous and the objectives many and varied. In such situations, software engineers, like their peers in other engineering disciplines have turned to multi-objective optimization techniques in general and to search based optimization in particular. 	

## Objectives

By the end of the course, students should be able to:
 
+ Analyze and critique core principles of software engineering.
+ Build models that execute those core principles. 
+ Predict and explain and optimize the behavior of those models.
+ Build and evaluate SBSE tools.
+ Analyze, critique, and communicate clearly the core theory and algorithms of multi-objective optimization

## Prerequisites

The prerequisite for this class is 510, Software Engineering. Significant software industry experience may be substituted, at the instructor’s discretion. 

Note that this is a **programming-intensive** subject.  

## Expected Workload

In the experience
of the lecturer, optimizers can be
 complex to
construct- particularly if the goal is to build them,
test them, and compare them against other methods.

However, if the right design patterns are applied
to that construction, then it is relatively easier
to build better optimizers. 

So  while this subject is about search for SE, it is also SE about software that searchers.
Hence, this is 
tools-based subject and it is required that students learn and use those tools (Python, repositories, etc).
Students  MUST be prepared to dedicate AT LEAST 5-8 working hours a week to this class (excluding the time spent in the classroom). Laboratory instruction is not included in this subject. 



## Required Materials

There are no required books for this class.

## Course Structure

Lectures presenting core theory; small weekly homeworks that build into a large project (on a model of the student’s own choosing); one mid-term  exams (mostly on terminology). Outside of class, students will work on their own class homework assignments. 

## Group mailing list

During term time, a group mailing list will be established. Students are strongly encouraged to contribute their questions and answers to that shared resource.

Note that, for communication of a more private nature, contact the lecturer on the email shown above.

## Topics

(Subject to change depending on student feedback.)

+ Week 1:  Intro to modeling
+ Week 2:  Intro to model-based programming in Python
+ Week 3:  Elite sampling
+ Week 4:  Simulated annealing, MaxWalkSat
+ Week 5:  SE applications1: USC suite
+ Week 6:  Statistical analysis  
+ Week 7:  Differential evolution, niching, GALE
+ Week 8:  Mid-session exam
+ Week 9:  SE applications2: Automatic debugging
+ Week 10: Particle swarm optimization,  NSGA-II, SPEA2, tabu search, Mocell
+ Week 11: SE application3: Requirements optimization
+ Week 12: SE applications 4 
+ Week 13: SE applications 5
+ Week 14: Student presentations
+ Week 15: Student presentations

## Grading Information

A weighted grade average will be calculated as follows:

<table>
<tr><td>Graded Elements
<td>Description
<td>Weight
</tr>
<tr><td>Mid-term
<td>Any unexcused absence from the mid-term exam will result in a grade of 0 for the exam.
<td>20%
</tr>
<tr>
<td>Attendance and Participation
<td>Attendance and active participation in class is essential.
<td>20%
</tr>
<tr><td>Weekly homeworks
<td>Students many resubmit homeworks multiple times.
<td>40%
</tr>
<tr>
<td>Presentation
<td>At the end of the semester, students will present slides on their independent project.  
<td>20%
</tr>
<tr><td>Code Reviews
<td>Conduct random one-on-one code reviews by lecturer with individual students (to gauge the extent to which the understand the code)
<td>Max number of reviews= 3 marks. <br>
maximum loss of grades per review= 4 marks).
</tr>
</table>

To check for attendance, the lecturer may require students to hand-in, at start of class:

+ A one-page (or more) summary of the some web page related to SBSE (specified by the lecturer)
  at bottom, _handwritten_ in _pen_.
+ With the name and student ID (last 4 digits) written at top.  

Students with authorized absences will be exempt from this requirement.

The following grade scale will be used: 

+ A+  (97-100), A (93-96), A-(90-92)
+ B+ (87-89), B (83-86), B-(80-82)
+ C+ (77-79), C (73-76), C-(70-72)
+ D+ (67-69), D (63-66), D-(60-62)
+ F (below 60).

Note that an "A" is an exceptional grade, not an
expected one, and it is based on the superior
quality of the final product.  A “B” is an above
average grade. In addition to meeting the minimum
requirements, the work is executed with a high
degree of competency and quality. A “C” is awarded
for work that meets all minimum requirements, but
may be of variable quality. Ds and Fs are reserved
for for clearly substandard or incomplete work.

Students are expected to conduct themselves in a respectful and professional manner at all times. Grades will be adjusted if students do not handle themselves in a respectful and professional manner with all members of the teaching staff and with others in the class, including message board posts.

### Attendance

Attendance is extremely important for your learning experience in this class. Once you reach three unexcused absences, each additional absence will reduce your attendance grade by 10%.

### Homeworks

Homework i+1 will not be marked till homework i has been successfully submitted. You may resubmit homeworks as many times as you like until they are successful. Exceptions:

I will not mark more than five homeworks from you in each calendar month (so you cannot let them back up). No homework will be marked after April 30, 2014.
Home works are due at start of class Tuesdays, except for mid-term. Homeworks will not be accepted unless:

+ They are stapled together.
+ The header of each sheet has a header saying "csc710sbse: hwX: YourLastName"
+ All pages are numbered (in ink) as "page M of N".
+ The pages have a minimum (even, no) lines wrapped.
+ Source code listings, or listings of any text output, are shown succinctly.

To generate succinct output, use something like the following:

    # note that in this example, all files begin 
    # with a multi-line comment showing file name
    Title="csc710sbse: hw1:Menzies"
    a2ps --center-title="$Title" -qr2gC -o ~/tmp/listing.ps files*
    ps2pdf ~/tmp/listing.ps ~.tp/listing.pdf
 
See [a sample output](etc/pdf/listing.pdf).

### Re-grading

Homeworks are graded pass, fail (and each pass is worth four marks). Students may resubmit failed homeworks multiple times (but not more than five homeworks will be marked in any month from any student).

Should you discover what you think is an error in grading, you have only TWO WEEKS after the grades are returned to you to request a re-grade. After that point, you cannot appeal your grade.  

## Code Sharing and "Informed" Reuse

For this subject, **informed reuse**  of the work of other students (or of the lecturer)
is strongly encouraged. That is if you understand someone else's code, you can use it on condition that:

+ You add comments to the code saying "From XYZ person", plus a few lines on how you adapted it.
+ You email the author advising that you are using code segments XYZ. Note: 
     + Do not ask for permission, just tell them you are using it.
     + The email should include a URL showing where they can see how you are using their code.
+ During code reviews (described above), students can offer an informed explanation of that code.

To facilitate informed reuse:

+ The lecturer and the students will store their code for this subject on some on-line code repository (where that code is easily read and downloaded).
+ In week2, students will offer the URL for that repo to the lecturer. This will be listed on the home
page of the subject.
+ Students are strongly encouraged to watch the code base of others who are using their code.



## Academic Integrity

Cheating will be punished to the full extent permitted. Note that **uniformed reuse** is cheating (for notes on how the lecturer will detect **uniformed reuse**, see the remarks above on code reviews).

All students are expected to maintain traditional standards of academic integrity by giving proper credit for all work.  All suspected cases of academic dishonesty will be aggressively pursued.  You should be aware of the University policy on academic integrity found in the Code of Student Conduct.
 
The  exams will be done individually.  Academic integrity is important.  Do not work together on the exams: cheating on either will be punished to the full extent permitted.  

## Disabilities

Reasonable accommodations will be made for students with verifiable disabilities. In order to take advantage of available accommodations, students must register with Disability Services for Students at 1900 Student Health Center, Campus Box 7509, 919-515-7653. For more information on NC State's policy on working with students with disabilities, please see the Academic Accommodations for Students with Disabilities Regulation(REG 02.20.01).

Students are responsible for reviewing the PRRs which pertain to their course rights and responsibilities. These include: http://policies.ncsu.edu/policy/pol-04-25-05 (Equal Opportunity and Non-Discrimination Policy Statement), http://oied.ncsu.edu/oied/policies.php (Office for Institutional Equity and Diversity),http://policies.ncsu.edu/policy/pol-11-35-01 (Code of Student Conduct), and http://policies.ncsu.edu/regulation/reg-02-50-03 (Grades and Grade Point Average).



## Non-Discrimination Policy

NC State University provides equality of opportunity in education and employment for all students and employees. Accordingly, NC State affirms its commitment to maintain a work environment for all employees and an academic environment for all students that is free from all forms of discrimination. Discrimination based on race, color, religion, creed, sex, national origin, age, disability, veteran status, or sexual orientation is a violation of state and federal law and/or NC State University policy and will not be tolerated. Harassment of any person (either in the form of quid pro quo or creation of a hostile environment) based on race, color, religion, creed, sex, national origin, age, disability, veteran status, or sexual orientation also is a violation of state and federal law and/or NC State University policy and will not be tolerated. Retaliation against any person who complains about discrimination is also prohibited. NC State's policies and regulations covering discrimination, harassment, and retaliation may be accessed at http://policies.ncsu.edu/policy/pol-04-25-05 or http://www.ncsu.edu/equal_op/. Any person who feels that he or she has been the subject of prohibited discrimination, harassment, or retaliation should contact the Office for Equal Opportunity (OEO) at 919-515-3148.


## Other Information

Non-scheduled class time for field trips or out-of-class activities are NOT required for this class. No such trips are currently planned. However, if they do happen then  students are required to purchase liability insurance. For more information, see http://www2.acs.ncsu.edu/insurance/



_________

<img align=right src="https://raw.githubusercontent.com/txt/mase/master/img/pd-icon.png">Copyright © 2015 [Tim Menzies](http://menzies.us).
This is free and unencumbered software released into the public domain.   
For more details, see the [license](https://github.com/txt/mase/blob/master/LICENSE).

