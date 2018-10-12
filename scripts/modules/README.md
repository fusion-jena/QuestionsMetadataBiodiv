# Fleiss' Kappa, GWET and other statistical calculations

Computation of several statistics needed for the evaluation of survey data, including calculations of the [Fleiss' Kappa] and [GWET] values.

Based on the caluclations by [Joseph L. Fleiss](https://en.wikipedia.org/wiki/Fleiss%27_kappa) and [Kilem Li Gwet](http://www.agreestat.com/research_papers/bjmsp2008_interrater.pdf). Works on Python 3+.




# Prerequisites

To install this module successfully, you need a [Python3+] distribution and an other third-party tool, called [NumPy].
How to install these tools, will be explained in the following lines:

## Instructions for Windows

### Python

To install [Python3+], go to the [Python website](https://www.python.org/), go to the "Downloads" button and install
the current [Python] version.
To check if [Python] was successfully installed, open your Command Prompt (called "shell" from now on) and type:

```shell

python
```

or

```shell

py
```

and check the displayed version in the [Python] shell. Type:

```shell

exit()
```

to exit the [Python] shell.

[Pip] - a package management system used to install [Python] software packages - is already installed in all [Python] versions >= 3.4.
[Pip] is used in this instruction to install the [NumPy] package.


### NumPy

[NumPy] is a [Python] package for efficiently computing array objects and other algebra calculations. To install [NumPy], type:

```shell

python -m pip install numpy
```

or

```shell

py -m pip install numpy
```

(whichever uses the correct [Python] version).



## Instructions for Linux

### Python

To install [Python3+], open your Command Prompt (called "shell" from now on) and type:

```shell

sudo apt-get install python3
```

To check if [Python] was successfully installed, type:

```shell

python
```

or

```shell

py
```

[Pip] - a package management system used to install [Python] software packages - is already installed in all [Python] versions >= 3.4.
[Pip] is used in this instruction to install the [NumPy] package.


### NumPy

[NumPy] is a [Python] package for efficiently computing array objects and other algebra calculations. To install [NumPy], type:

```shell

python -m pip install numpy
```

or

```shell

py -m pip install numpy
```

(whichever uses the correct [Python] version).




# Installation

```shell
#Go to the 'modules' directory with the 'setup.py' script and type:

python setup.py install

#or

py setup.py install

#whichever uses the correct Python version
```




# Code usage

```python
import fleisskappa as kp


-----------------------------
#Calculation of the sum over all n(ij)
#Given a list or dictionary containing the scores of each category for one noun (e.g. dict[category1]=5, dict[category2]=2, dict[category3]=9, etc.), run:

kp.calculateSumN(score_list)


-----------------------------
#Calculation of the P(i) value
#Given the sum over all n(ij) and the number of participants, run:

kp.calculatePI(participantNumber, sumN)


-----------------------------
#Caluclation of the P value
#Given a list of P(i) values and the number of nouns used in the survey, run:

kp.caluclateP(pi_value_list, nounNumber)


-----------------------------
#Calculation of the Pe value, the Pe(I) value, the p(j) values for each category and the p(j)(I) values for each category
#Given a list or dictionary containing the overall scores of each category for all nouns, the number of nouns, the number of categories and the number of participants, run:

kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)

#The method returns a list containing all four values:

Pe value: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[0]
Pe(I) value: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[1]
p(j) values: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[2]
p(j)(I) values: kp.calculatePE_PEI(overall_score_list, participantNumber, nounNumber, categoryNumber)[3]


-----------------------------
#Non-matrix calculation of the Fleiss' Kappa and GWET values
#Given the P and the Pe or Pe(I) values, run:

kp.calculateFleissKappa_GWET(p_value, pei_value)

#Depending on the second parameter the method calculates the Fleiss' Kappa or GWET value:
Fleiss' Kappa: kp.calculateFleissKappa_GWET(p_value, pe_value)
GWET: kp.calculateFleissKappa_GWET(p_value, peI_value)


-----------------------------
#Matrix calculation fo the Fleiss' Kappa and GWET values.
#Given a two-dimensional matrix containing each score of each category for all nouns, run:

kp.calculateFleissKappa_GWET_Matrix(dataMatrix)

#The method returns a list containing the Fleiss' Kappa and GWET values:

Fleiss' Kappa: calculateFleissKappa_GWET_Matrix(dataMatrix)[0]
GWET: calculateFleissKappa_GWET_Matrix(dataMatrix)[1]

#Example matrix with five categories, three nouns and four participants:

dataMatrix = [[2,2,0,0,0],[1,0,1,1,1],[0,1,0,1,2]]
```
