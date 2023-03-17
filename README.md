<h4 align = "center"> SARA: Code Performance Prediction by Mapping Execution Test Times to Stylometry Features</h4>
<hr>

<p align="center"> <img src="..doc/sara.svg" width="98%"> </p>

Official implementation of ```SARA: Code Performance Prediction by Mapping Execution Test Times to Stylometry Features``` to undergo review. For reviewer(s), please follow the instructions below to reproduce the results presented in the paper. 

## Abstract
> Software development teams establish elaborate continuous integration pipelines containing automated test cases to accelerate the development process of software. Automated tests help to verify the correctness of code modifications decreasing the response time to changing requirements. However, when the software teams do not track the performance impact of pending modifications, they may need to spend considerable time refactoring existing code. 
> 
> This paper presents SARA, a code analysis framework that provides continuous feedback on the performance impact of pending code updates. We design performance microbenchmarks by binding the execution test times of embedded automated test cases given a code update and map the execution test times to numerical statistics and distributional semantic code stylometry features used as input observations to predictive models tasked with code performance predictions. Our experiments achieved state-of-the-art performance in predicting the execution time performance of code updates to the software.

<hr>

> Note: Full paper details will be chronicled post-acceptance. SARA's [feature engineering](#feature-engineering) methods are the most transferable component of this work and are applicable in several other use cases beyond performance research. We leverage knowledge in code (SWE) and language (NLP) understanding to statistically and distributionally extract input features. 

<hr>
Artifact Author: Chidera Biringa
<hr>

## Installation
```
$ git clone https://github.com/biringaChi/SARA 
$ pip install -r requirements.txt 
$ cd src
```

## Problem Definition
<p align="center"> <img src="..doc/motivation.svg" width="95%"> </p>

> Figure 1: Access and manipulation of a Linked-HashMap (LHM) using an Entry-set and Key-set. ESA and ESM denote Entry-set Access and Manipulation. KSA and KSM represent Key-set Access and Manipulation. Lines of code highlighted in green and red are LHM access and manipulation using  Entry-set and Key-set.

In this work, a code snippet or program is mediocre if it introduces a significant performance overhead to software and consequently skews the baseline resulting in an outlier performance. For example, consider the motivating example above. The snippet is a real-world fragment of a Java program, and it calculates the term frequency of more than 2000 elements in a linked hashmap (LHM). An LHM combines a hash table and a linked list. It ensures the predictable maintenance of elements in an iterable object. The peripheral difference between the snippets is in how the linked hashmap is accessed (ESA), (KSA), and manipulated (ESM), (KSM) using an ```entrySet()``` and ```keySet()``` respectively. On a test level, the ESA and ESM, and KSA and KSM versions of the code snippet execute in ```4 seconds``` and ```4 minutes``` as tested in our test environment, which means there is a ```6000% increase``` in ET. The difference decreases by half to ```3000%```, with an increase in the number of elements from 2,000 to 200,000. 

The above-stated performance discrepancy might appear inconsequential for isolated occurrences. However, in scenarios where that low-performing program is deployed and used in multiple areas of a software product or feature, it would significantly increase the overall time of an operation to complete. Finally, the KSA and KSM versions of the program, which are inefficient, are syntactically correct and contain no apparent bugs. This highlights an inherent complexity in the problem, such as employing erroneous data structure selection and manipulation and selecting $O(2^{n})$ time algorithms when there are viable polynomial options.

> Note: we are working under the assumption of an ```ideal``` software development environment, where external variables such as memory usage and network connectivity relatively outside the developer's control are operating at ```optimal``` levels.

## Feature Engineering
This work leverages domain knowledge in software engineering (code stylometry) for feature extraction. Code stylometry is a source code's functional and non-functional characteristics. The table below details features of interest. An indispensable component of building predictive models is the transformation of text-based observations into numerical representations. 

Thus, post-feature extraction, we transform the aforementioned extracted features into numerical data points using our ```FREQSTYLE``` and ```EMBEDSTYLE``` algorithms. FREQSTYLE and EMBEDSTYLE are numerical statistics and distributional semantic representation methods. In FREQSTYLE, we transformed features via frequency distribution, while EMBEDSTYLE constitutes the adoption of unsupervised learning by mapping observations to vector space and deriving feature embeddings. 

---
### Taxonomy of Code Stylometry Features (CSF)
 ```{Statements, Controls, Expressions}``` $\in$ ```Syntactic``` $\land$ ```{Invocations, Declarations}``` $\in$ ```Lexical``` 
| Class | Types | Brief Description | 
| --------------- | --------------- | --------------- |
| Statements | IfStatement, WhileStatement, DoStatement, AssertStatement, SwitchStatement, ForStatement, ContinueStatement, ReturnStatement, ThrowStatement, SynchronizedStatement, TryStatement, BreakStatement, BlockStatement, BinaryOperation, CatchClause | Dictates the behavior of a program under explicitly defined conditions |
| Controls | ForControl, EnhancedForControl 	  | Defines the repetition of instructions dependent on the satisfaction of requirements |
| Expressions | StatementExpression, TernaryExpression, LambdaExpression	  | Independent language entities with unique definitions |
| Invocations | SuperConstructorInvocation, MethodInvocation,  SuperMethodInvocation, SuperMemberReference, ExplicitConstructorInvocation, ArraySelector, AnnotationMethod, MethodReference | Defines the invocation of a program from another program |
| Declarations | TypeDeclaration, FieldDeclaration, MethodDeclaration, ConstructorDeclaration, PackageDeclaration, ClassDeclaration, EnumDeclaration, InterfaceDeclaration, AnnotationDeclaration, ConstantDeclaration, VariableDeclaration, LocalVariableDeclaration, EnumConstantDeclaration, VariableDeclarator  | Declares the existence of an entity in memory and assigns a value to that entity |
--- 

FREQSTYLE: Numerical Statistic Representation of Extracted Code Stylometry Features
<img src="..doc/freqstyle.png" width="40%">
```
$ python3 freqstyle
```
EMBEDSTYLE: Distributional Semantic Representation of Extracted Code Stylometry Features
<img src="..doc/embedstyle.png" width="40%">
```
$ python3 
```