# Metadata Analysis of Data Repositories with OAI-PMH interfaces

This folder provides the source code to harvest and parse metadata from OAI-PMHs interfaces of data repositories and additional material. The script ```metadata_harvester.py``` connects to an OAI-PMH interface and harvests all available metadata. Per metadata file we inspect what elements from the metadata standards are used and save its occurence (1) or non-occurence (0). The result is a csv file per metadata schema that contains the dataset IDs and their available and used metadata elements.

Works on ```Python3+```.

# Structure

* [Examples] (contains example files)
* [Analysis] (Java code to count the metadata data fields used and to generate charts)
* [Charts] (contains the generated charts per repository and metadata schema)
* metadata.tar.gz (compressed full parsed metadata)
* ```metadata_harvester.py``` - source file to harvest and parse metadata (see detailed descriptions below)
* ```split_content.py``` - source file to split each line of the metadata file prodcued by the ```-fs/--fields```- option of ```metadata_harvester.py``` script the  into individual XML files and, optionally, counts used keywords in a specified field (see detailed descriptions below)
* ```random_file_selector.py``` - source file to randomly selected a specified number of files from the pool of XML files created by ```split_content.py script``` (see detailed descriptions below)
* get_topN.py - source file to get the top N number of keywords (sorted by number of counts, descending) in the optional CSV-file created by ```split_content.py``` (see detailed descriptions below)


[Examples]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/examples
[Analysis]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/analysis
[Charts]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/charts

# Prerequisites

To start each script in this package successfully, you need a ```Python3+``` distribution and some other third-party tools.
How to install these tools will be explained in the following section

## Instructions for Windows and Linux

### Python

To install ```Python3+```, go to the [Python website](https://www.python.org/), go to the ```Downloads``` button and install the current ```Python``` version.
To check if ```Python``` was successfully installed, open your Command Prompt (called ```shell``` from now on) and type:

```shell
python
```

or

```shell
py
```

and check the displayed version in the ```Python``` shell. Type:

```shell
exit()
```

to exit the ```Python``` shell.

```Pip``` - a package management system used to install ```Python``` software packages - is already installed in all ```Python``` versions >= 3.4.
```Pip``` is used in this instruction to install the ```Requests``` and ```XmlToDict``` packages.


### Requests: HTTP for Humans

```Requests: HTTP for Humans``` is a third party ```Python``` tool with which you can easily POST and GET data of HTTP connections without the need for manual labor. To install the ```Requests``` module, simple type:

```shell
python -m pip install requests
```

or

```shell
py -m pip install requests
```

(whichever uses the correct ```Python``` version).


### XmlToDict

```XmlToDict``` is a third party [Python] tool that is able to transform XML trees into dictionary for a easier parsing. To install the ```XmlToDict``` module, simple type:

```shell
python -m pip install xmltodict
```

or

```shell
py -m pip install xmltodict
```

(again, whichever uses the correct ```Python``` version).


### YAML

```YAML``` is a third party [Python] tool that is able to load and read so called [YAML]-files and transform its content into a dictionary for easy parsing. To install the ```YAML``` module, simple type:

```shell
python -m pip install yaml
```

or

```shell
py -m pip install yaml
```

(again, whichever uses the correct ```Python``` version).

### pandas

```pandas``` is a third party [Python] tool that is able to efficiently load and access data in CSV files. to install the ```pandas``` module, simple type:

```shell
python -m pip install pandas
```

or

```shell
py -m pip install pandas
```

(again, whichever uses the correct ```Python``` version).


# Script

## metadata_harvester.py

```metadata_harvester.py``` is an easy to use Command Line Interface (CLI) tool to harvest and extract metadata information from the digital data portals. The scripts is able to read the settings for a data portal from a [YAML]-file (YAML Ain't Markup Language) and are commonly used for configuration. This way new data portals can be added with little effort. For more information see section 'Configuring data portal(s)/Adding new dataportal(s)'. By default the script returns a CSV that shows which record (one line) used which metadata information (marked by ```1``` (used) or ```0``` (not used)) and their corresponding dates. If now date was specified or a record didn't have a date, no date was taken (marked with ```None```). The script has ten options as input, ```-cf```, ```-dp```, ```-mf```, ```-fs```, ```-lm```, ```-fl```, ```-hx```, ```-sf```, ```-sw``` and ```-ew```.
 * ```-cf``` specifies the path to the config.yaml file that contains the settings for the data portals
 * ```-dp``` specifies from which dataportal the metadata should be harvested. If a dataportal is specified that isn't part of the list of data portals, an error is thrown.
 * ```-mf``` specifies from which metadata format of the corresponding dataportal the metadata information will be harvested. If a metadata format is specified that isn't part of the specified dataportal, an error is thrown. If no metadata format is specified, the metadata information of all metadata formats of the corresponding dataportal will be harvested.
 * ```-fs``` specifies whether the content of specific fields should be saved in an extra CSV file or not. Multiple fields are separated by commas. See the website of the corresponding dataportal for information about avaiable fields. Every field that was specified but did not appear in at least one record is printed at the end of the harvest.
 * ```-lm``` specifies the maximum number of harvested records. For example if set to 200, only the metadata information of the first 200 records are harvested. If set to 0, all records will be harvested (default).
 * ```-fl``` specifies if the full path to each metadata field should be saved instead of just the field itself.
 * ```-hx``` specifies a directory in which the raw metadata from the dataportal is saved in XML format.
 * ```-sf``` prints the avaiable metadata formats for the specified dataportal.
 * ```-sw``` specifies how long the program will wait between the harvesting of each metadata format in seconds. By default it is set to 60 seconds.
 * ```-ew``` specifies how long the program will wait before it restarts if an exception occurs in seconds. By default it is set to 30 seconds.

The results are saved in a directory called ```metadata``` that is automatically created in the directory from which the script is called. The name of the resulting CSV files are the date the harvest finished. An example of the first 550 records for each dataportal and metadata format can be found in the 'examples' directory.


### Resumption tokens

All five data portals use the ```Open Archives Initiative Protocol for Metadata Harvesting``` (```OAI-PMH```) service to manage their metadata information. Records can't be harvested all at once but are structured in pages. Each page contains 100 records and an index, called a resumption token, that is used to access the next page. Therefore, it is to note that each page has to be accessed individually which can take a long time if no or a high limit for the number of records is specified. The script also waits for several seconds (specified by ```-sw```) between each harvest of a metadata format to prevent connection issues. Furthermore, if a connection issue (or similiar) happens during the harvest, the script will wait for several seconds (specified by ```-ew```) and resume from the last resumption token.


### Configuring/Adding data portal(s)

Data portals can easily be configured or added by accessing the 'config.yaml' file in a few steps. The format of the file is as follows:

```
{dataportal_1}
  url: {dataportal_url}
  resumption_url: {dataportal_resumption_url}
  metadata_formats:
    {metadata_format_1}: {date_field}
    {metadata_format_2}: {date_field}
    {metadata_format_3}: {date_field}
{dataportal_2}
  url: {dataportal_url}
  resumption_url: {dataportal_resumption_url}
  metadata_formats:
    {metadata_format_1}: {date_field}
    {metadata_format_2}: {date_field}
    {metadata_format_3}: {date_field}
    ...
    ...
    ...
```


Strings surrounded by '{}' are specified by the user. {dataportal} specifies the name of each data portal and is used by the ```-dp``` option of the script. This can be any string the user wants but has to be specific for the each data portal. {dataportal_url] specifies the 'first' page of the harvesting and should look something like this:

```www.your_dataportal.org/oai/request?verb=ListRecords&metadataPrefix=```

It is important that the 'metadataPrefix=' token is be empty. The metadata format is later added to it by the script. {dataportal_resumption_url} specifies all following pages of the harvesting and shoud look something like this:

```www.your_dataportal.org/oai/request?verb=ListRecords&resumptionToken=```

Again, it is important that the 'resumptionToken=' is empty since the script will later add it to the string. For more information see the 'Resumption tokens' section for more information. The {metadata_format_} specifies the metadata formats for the given data portal and is used by the ```-mf``` option. Each line is a new metadata format. Lastly, {date_field} specifies the field containing the desired date that should be saved for each record for the given metadata format.

Important to note is that the given URLs are able to use the OAI-PMH protocol or else the data harvesting won't work. For examples see the 'config.yaml' file containing the five data repositories 'Dryad', 'GBIF', 'Pangaea', 'Zenodo' and 'Figshare'.


### Example usage:

```shell
python metadata_harvester.py -dp dryad -lm 550 -fl
```

## split_content.py

```split_content.py``` is an easy to use Command Line Interface (CLI) tool that splits each line of the CSV file created by the ```-fs/--fields```- option of ```metadata_harvester.py``` into individual (pseudo-)XML-files. Furthermore, it also can count the used keywords in the first field that contains a specified string and saves it in a CSV file with the added string 'keyword_counts'. The script has two options a input, ```-c``` and ```-f```.
 * ```-c``` specifies the path to the fields CSV file produced by the ```-fs/--fields``` option ```metadata_harvester.py```
 * ```-f``` specifies what field should be counted as a string, i.e. 'subjects'
 
 
 ### Example usage
 
 ```shell
 python split_content.py -c fields//dryad/oai_dc/24_08_2019.csv -f subjects
 ```
 
 ## random_file_selector.py
 
 ```random_file_selector.py``` is an easy to use Command Line Interface (CLI) to randomly choose a number of XML-files produced by the ```split_content.py``` script. The results will be saved in a folder in the directory of the XML-files called 'selected_files'. Important to note is that the script can take a long time if the ```-f``` option is used and a lot of XML-files are in the directory since each file has to be access individually to check for the specified filters. The script has five options as input, ```-fs```, ```-p```, ```-s```, ```-f``` and ```-d```.
 * ```-fs``` specifues the path to the directory where the XML-files are
 * ```-p``` specifies the number of files that should be randomly taken from the pool
 * ```-s``` specifies the seed for the ```-p``` option; with the same files and the same seed the same results can be obtained; if no seed is specified, a random one will be chosen between 0 and 2147483647; however,the seed doesn't have to be a number but can also be a string of any kind; at the end of the run the used seed will be saved in a file called 'seed.txt' in the 'selected_files' folder
 * ```-f``` specifies a filter for keywords to only consider files that contain them in a specified field; the input is a list of strings separated by commas; the first string is the field the should be filtered, all following strings are the keywords to filter (i.e. 'subjects,Biodiversity,Temperature,Insetcs')
 * ```-d``` deletes the 'selected_files' folder if it already exists in the directory; f the option wasn't set but the 'selected_files' folder exists, an error is thrown
 
 
 ### Example usage
 
 ```shell
 python random_file_selector.py fields/dryad/oai_dc/ -p 10000 -f subjects,Biodiversity,Temperature,Insetcs
 ```
 
 ## get_topN.py
 
 ```get_topN.py``` is an easy to use Command Line Interface (CLI) tool to get the top N number of keywords in the 'keyword_counts' CSV-file produced by the ```-f``` option of the ```split_content.py``` script. This can be helpful if you want ,for example, only the top 50 used keywords and the 'keyword_counts' CSV-file is very large and can't be opened/takes to long to open with an ordinary program (i.e. Excel or LibreOffice). The results will be saved in a CSV-file called 'getTopN' in the same directory as the 'keyword_counts' CSV-file. The script has two options as input, ```-c``` and ```-n```.
 * ```-c``` specifies the path to the 'keyword_counts' CSV-file
 * ```-n``` specifies the top <n> number of used keywords you want to extract; set <n> to -1 to retrieve all keywords sorted by counts in descending order
 
 
 ### Example usage
 
 ```shell
 python get_topN.py fields/dryad/oai_dc/24_08_2019_keyword_counts.csv -n 50
 ```
