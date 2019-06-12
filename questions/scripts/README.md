# Creation/building and evaluation of 'LimeSurvey' surveys

Python scripts for creating and evaluating [LimeSurvey surveys](https://www.limesurvey.org/). Works on ```Python3+```.



# Prerequisites

To start each script in this package successfully, you need a ```Python3+``` distribution and some other third-party tools.
How to install these tools, will be explained in the following lines:

## Instructions for Windows and Linux

### Python

To install ```Python3+```, go to the [Python website](https://www.python.org/), go to the ```Downloads``` button and install
the current ```Python``` version.
To check if ```Python``` was successfully installed, open your Command Prompt (called ```shell``` from now on) and type:

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

to exit the ```Python``` shell.

```Pip``` - a package management system used to install [Python] software packages - is already installed in all ```Python``` versions >= 3.4.
```Pip``` is used in this instruction to install the [Pandas] package.


### FleissKappa

To install the ```Fleisskappa``` module - that is delivered with the main scripts - go to the "modules" folder (shell) and type:

```shell
python setup.py install
```

or

```shell
py setup.py install
```

(whichever uses the correct ```Python``` version). For further information, look at the ```README.md``` file in the "modules" folder.


### Pandas

```Pandas``` is a third-party ```Python``` tool for efficiently reading CSV files column by column. To install the ```Pandas``` module, simple type:

```shell
python -m pip install pandas
```

or

```shell
py -m pip install pandas
```

(again, whichever uses the correct ```Python``` version).



# Scripts

## create_survey.py:

```create_survey.py``` is a simple Command Line Interface (CLI) tool to read and extract data from a semicolon-separated CSV file and to
write it into the ```LimeSurvey-XML-format```. The script has three options as input, ```-f```, ```-d``` and ```-ct```.
* The ```-f``` option takes the path to the CSV file as input. A folder named ```lsg_files``` - in which all LimeSurvey-XML files are saved - is automatically created in the same directory as the CSV file during the process.
 * The ```-d``` option deletes this ```lsg_files``` folder if it already exist. If a folder named ```lsg_files``` already exists but the ```-d``` option isn't set, the program will print an error message to remove this folder from this directory or set the ```-d``` option and abort.
 * The ```-ct``` option takes the path to a simple text file containing the categories and their descriptions. Each line has one category and its description separated by a vertical line ```|```. For more information see
the ```Example categories files``` section.

### Example usage:

```shell
python create_survey.py -f biodiv_questions.csv -ct creation_categories.txt -d
```

The ```LimeSurvey-XML``` file can have a maximum of 20 questions. If a CSV file has more than 20 questions it will separated in two, three,
four, etc. number of ```LimeSurvey-XML``` files that will be saved in the ```lsg_files``` folder. So, if a CSV file has 55 questions, the first
20 questions will be saved in a ```LimeSurvey-XML``` file, the next 20 questions will be saved in another ```LimeSurvey-XML``` file and the last
15 questions will be saved, again, in another ```LimeSurvey-XML``` file (-> three ```LimeSurvey-XML``` files).

The CSV file should be semicolon-separated and have the following format:

* 1st column: Title
    -> each question has to have an unique title
    -> each title longer than 18 characters will be trimmed to 18 characters

* 2nd column: Question/statement

* 3rd column: custom usage

* 4th column: custom usage

* 5th and all following columns: Terms to be annotated


## analyze_result.py:

```analyze_result.py``` is a simple CLI tool to read and extract data from a ```LimeSurvey-Result```-CSV file and to write and evaluate its
results into a new CSV file, called ```lsg__/survey_names/.csv```. The script has six options as input, ```-f```, ```-o```, ```-c```, ```-ct```, ```-cu``` and ```thres```.
 * The ```-f``` option takes the paths of multiple ```LimeSurvey-Result```-CSV files and combine the results into a single CSV file. However, each of these
files have to have the same questions and nouns, i.e. have to be identical except for their question order. Most participants won't, most likely, answer each question and noun (especially in particulary long surveys). Therefore, it can be useful to let each participant run through one survey multiple times - each time with a different question order -, to make sure that each noun is actually annotated
at least once.
 * The ```-o``` option sets the output folder where the resulting evaluation file.
 * The ```-c``` option let's you choose at which column in the ```LimeSurvey-Result```-CSV file the actually data starts, so at which column the first question (and noun) and answer is. Only the start column of the first input ```LimeSurvey-Result```-CSV file is needed since the data of all following ```LimeSurvey-Result```-CSV files is extracted by using the question titles and nouns of the first ```LimeSurvey-Result```-CSV file.
 * The ```-ct``` option takes the path to a simple text file containing the categories. The categories should be identical to the categories used in the survey/surveys or else the program will throw an error if a category was chosen as an answer but wasn't written in the ```categories``` file. The descriptions will be ignored. For more information see the ```Example categories file``` section.
 * The ```-cu``` option takes the path to a simple text file containing custom counts for the ```other``` category. If a user chose the ```other``` category and added a description, key words can be specified that will not be counted as ```other``` but as an category you specified. For example, if one of the categories is ```Quality``` and a user chose the ```other``` category with the description ```parameter```, this can be counted as ```Quality``` and not as ```other```. Multiple keywords for one category are seprated by commas. For more information see the ```Example custom file``` section.
 * And the ```-thres``` option sets what rows with a higher P(i) value then specified will be saved in an extra XML file.


### Example usage:

```shell
py analyze_result.py -f first.csv second.csv third.csv -o result_folder -c 9 -ct evaluation_categories.txt -cu custom.txt -thres 0.58
```



# Example 'categories' files

```creation_categories.txt```  
<pre>
|-----------------------------|  
|category1|description1       |  
|category2|description2       |  
|category3|description3       |  
|category4|description4       |  
|category5|description5       |  
|category6|description6       |  
|category7|description7       |  
|category8|description8       |  
|category9|description9       |  
|category10|description10     |  
|                             |  
|                             |  
|                             |  
|                             |  
|-----------------------------|  
</pre>

or for the analyze_result.py specificially

```evaluation_categories.txt```  
<pre>
|-----------------------------|  
|category1                    |  
|category2                    |  
|category3                    |  
|category4                    |  
|category5                    |  
|category6                    |  
|category7                    |  
|category8                    |  
|category9                    |  
|category10                   |  
|                             |  
|                             |  
|                             |  
|                             |  
|-----------------------------|  
</pre>



# Example 'custom' file

```custom.txt```  
<pre>
|--------------------------------------------|  
|category1=keyword1_1,keyword1_2             |  
|category2=keyword2_1,keyword2_2,keyword2_3  |  
|category3=keyword3_1                        |  
|category4=keyword4_1,keyword4_2             |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|                                            |  
|--------------------------------------------|  
</pre>



# Remarks

On some systems the analyze_result.py script has to be in ```modules``` folder to find and use the fleisskappa module, else it will throw
an error that the fleisskappa module can't be found. If that's the case, simply drag the analyze_result.py script in the ```modules``` folder
and run the program as usual.
