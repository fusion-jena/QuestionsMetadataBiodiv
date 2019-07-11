# Metadata Analysis of Data Repositories with OAI-PMH interfaces

This folder provides the source code to harvest and parse metadata from OAI-PMHs interfaces of data repositories and additional material. The script ```metadata_harvester.py``` connects to an OAI-PMH interface and harvests all available metadata. Per metadata file we inspect what elements from the metadata standards are used and save its occurence (1) or non-occurence (0). The result is a csv file per metadata schema that contains the dataset IDs and their available and used metadata elements.

Works on ```Python3+```.

# Structure

* [Examples] (contains example files)
* [Analysis] (Java code to count the metadata data fields used and to generate charts)
* [Charts] (contains the generated charts per repository and metadata schema)
* metadata.tar.gz (compressed full parsed metadata)
* metadata_harvester.py - source fill to harvest and parse metadata (see detailed descriptions below)


[Examples]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/examples
[Analysis]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/analysis
[Charts]: https://github.com/fusion-jena/QuestionsMetadataBiodiv/tree/master/data_repositories/charts

# Prerequisites

To start each script in this package successfully, you need a ```Python3+``` distribution and some other third-party tools.
How to install these tools will be explained in the following:

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
python -m pip install requests
```

(whichever uses the correct ```Python``` version).


### XmlToDict

```XmlToDict``` is a third party [Python] tool that is able to transform XML trees into dictionary for a easier parsing. To install the ```XmlToDict``` module, simple type:

```shell
python -m pip install xmltodict
```

or

```shell
python -m pip install xmltodict
```

(again, whichever uses the correct ```Python``` version).



# Script

## metadata_harvester.py

```metadata_harvester.py``` is a simple to use Command Line Interface (CLI) tool to harvest and extract metadata information from the five digital dataportals Dryad, GBIF, Pangaea, Zenodo and Figshare. By default the script returns a CSV that shows which record (one line) used which metadata information (marked by ```1``` (used) or ```0``` (not used)) and their corresponding dates. If now date was specified or a record didn't have a date, no date was taken (marked with ```None```). The script has nine options as input, ```-dp```, ```-mf```, ```-fs```, ```-lm```, ```-fl```, ```-hx```, ```-sf```, ```-sw``` and ```-ew```.
 * ```-dp``` specifies from which dataportal the metadata should be harvested. If a dataportal is specified that isn't part of the list of dataportals, an error is thrown.
 * ```-mf``` specifies from which metadata format of the corresponding dataportal the metadata information will be harvested. If a metadata format is specified that isn't part of the specified dataportal, an error is thrown. If no metadata format is specified, the metadata information of all metadata formats of the corresponding dataportal will be harvested.
 * ```-fs``` specifies whether the content of specific fields should be saved in an extra CSV file or not. Multiple fields are separated by commas. See the website of the corresponding dataportal for information about avaiable fields. Every field that was specified but did not appear in at least one record is printed at the end of the harvest.
 * ```-lm``` specifies the maximum number of harvested records. For example if set to 200, only the metadata information of the first 200 records are harvested. If set to 0, all records will be harvested (default).
 * ```-fl``` specifies if the full path to each metadata field should be saved instead of just the field itself.
 * ```-hx``` specifies a directory in which the raw metadata from the dataportal is saved in XML format.
 * ```-sf``` prints the avaiable metadata formats for the specified dataportal.
 * ```-sw``` specifies how long the program will wait between the harvesting of each metadata format in seconds. By default it is set to 60 seconds.
 * ```-ew``` specifies how long the program will wait before it restarts if an exception occurs in seconds. By default it is set to 30 seconds.

The results are saved in a directory called ```metadata``` that is automatically created in the directory from which the script is called. The name of the resulting CSV files are the date the harvest finished. An example of the first 550 records for each dataportal and metadata format can be found in the 'examples' directory.


### Warning

All five dataportals use the ```Open Archives Initiative Protocol for Metadata Harvesting``` (```OAI-PMH```) service to manage their metadata information. Records can't be harvested all at once but are structured in pages. Each page contains 100 records and an index, called a resumption token, that is used to access the next page. Therefore, it is to note that each page has to be accessed individually which can take a long time if no or a high limit for the number of records is specified. The script also waits for several seconds (specified by ```-sw```) between each harvest of a metadata format to prevent connection issues. Furthermore, if a connection issue (or similiar) happens during the harvest, the script will wait for several seconds (specified by ```-ew```) and resume from the last resumption token.


### Adding new dataportals, metadata formats or dates

New dataportals, metadata formats or metadata dates can easily be added to the script with a few steps. If a new dataportal should be added, open the python script with an text editor of your choice, and go to the line

```'python
def requestMetadata(prefix, resumptionToken, firstPage=False):
```

This method specifies the URLs from which the metadata will be harvested. Now, go to the line

```python
if(firstpage):
```

and add at the bottom of that section the line

```python
elif(dataportal == your_dataportal):
  metadata_url = "dataportal_url" + prefix
```

(replace ```your_dataportal``` with the name of your dataportal and ```dataportal_url``` with the OAI-PMH URL of your dataportal without the metadata format). Your dataportal URL should look something like this:

```www.your_dataportal.org/oai/request?verb=ListRecords&metadataPrefix=```.

Now, in the section below (marked with ```else```) add at the bottom, again, the line

```python
elif(dataportal == your_dataportal):
  metadata_url = "dataportal_url_resumption_token" + prefix
```

(replace ```dataportal_url_resumption_token``` with the OAI-PMH resumption URL of your dataportal without the resumption token). Your dataportal resumption URL should look something like this:

```www.your_dataportal.org/oai/request?verb=ListRecords&resumptionToken=```.

Important to note is that your dataportal needs to use the ```OAI-PMH``` service or else it will not work. The necessary URLs are now added but the script still needs to be told to actually use the dataportal. Go to the line

```python
def downloadMetadata():
```

This is the ```main``` method that starts the harvest. There are two dictionaries, ```prefixDic``` and ```dateDic```. ```prefixDic``` contains the name of the dataportals and their corresponding metadata formats. ```dateDic``` contains the used date field for each metadata format and dataportal. Now, add at the bottom of the ```prefixDic``` dictionary the line

```python
prefixDic[your_dataportal] = (metadataformat1, metadataformat2, metadataformat3, ...)
```

(replace ```metadataformat1/2/3``` with the metadata formats of your dataportal; the dataportal and metadata formats have to be in parentheses and separated by commas). After that, go to the bottom of the ```dateDic``` dictionary and add the line for each of your metadata formats:

```python
dateDic[your_dataportal][metadataformat] = "no_date"
```

If you want to use a specific field for the date, just replace ```no_date``` with the field of your choice. If you want to add a new metadata format to an existing dataportal, follow the previous instructions starting after adding the dataportal URLs. However, instead of creating a new dictionary, just add your metadata format to the existing list. The same goes if you want to change the date field of an existing metadata format. Simply go to the ```dateDic``` dictionary and replace the currently used date field with yours.



### Example usage:

```shell
python metadata_harvester.py -dp dryad -lm 550 -fl
```

