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


### YAML

```YAML``` is a third party [Python] that is able to load and read so called [YAML]-files and transform its content into a dictionary for easy parsing. To install the ```YAML``` module, simple type:

```shell
python -m pip install yaml
```

or

```shell
python -m pip install yaml
```

(again, whichever uses the correct ```Python``` version).



# Script

## metadata_harvester.py

```metadata_harvester.py``` is a simple to use Command Line Interface (CLI) tool to harvest and extract metadata information from the digital data portals. The scripts is able to read the settings for a data portal from a [YAML]-file (YAML Ain't Markup Language) and are commonly used for configuration. This way new data portals can be added with little effort. For more information see section 'Adding new dataportals'. By default the script returns a CSV that shows which record (one line) used which metadata information (marked by ```1``` (used) or ```0``` (not used)) and their corresponding dates. If now date was specified or a record didn't have a date, no date was taken (marked with ```None```). The script has ten options as input, ```-cf```, ```-dp```, ```-mf```, ```-fs```, ```-lm```, ```-fl```, ```-hx```, ```-sf```, ```-sw``` and ```-ew```.
 * ```-cf``` specifies the path to the config.yaml file that contains the settings for the data portals
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


### Resumption tokens

All five dataportals use the ```Open Archives Initiative Protocol for Metadata Harvesting``` (```OAI-PMH```) service to manage their metadata information. Records can't be harvested all at once but are structured in pages. Each page contains 100 records and an index, called a resumption token, that is used to access the next page. Therefore, it is to note that each page has to be accessed individually which can take a long time if no or a high limit for the number of records is specified. The script also waits for several seconds (specified by ```-sw```) between each harvest of a metadata format to prevent connection issues. Furthermore, if a connection issue (or similiar) happens during the harvest, the script will wait for several seconds (specified by ```-ew```) and resume from the last resumption token.


### Adding new dataportal

New dataportals can easily be added by configuring the 'config.yaml' file in a few steps. The format of the file is as follows:

{dataportal_1}
  url: {dataportal_url}
  resumption_url: {dataportal_resumption_url}
  metadata_formats:
    {metadata_format_1}: {data_field}
    {metadata_format_2}: {data_field}
    {metadata_format_3}: {data_field}
{dataportal_2}
  url: {dataportal_url}
  resumption_url: {dataportal_resumption_url}
  metadata_formats:
    {metadata_format_1}: {data_field}
    {metadata_format_2}: {data_field}
    {metadata_format_3}: {data_field}
    ...
    ...
    ...


Strings surrounded by '{}' are user-specific. {dataportal} specifies the name of each data portal and is used by the ```-dp``` option of the script. This can be any string the user wants but has to be specific for the each data portal. {dataportal_url] specifies the 'first' page of the harvesting and should look something like this:

www.your_dataportal.org/oai/request?verb=ListRecords&metadataPrefix=

It is important that the 'metadataPrefix=' token is be empty. The metadata format is later added to it by the script. {dataportal_resumption_url} specifies all following pages of the harvesting and shoud look something like this:

www.your_dataportal.org/oai/request?verb=ListRecords&resumptionToken=

Again, it is important that the 'resumptionToken=' is empty since the script will later add it to the string. For more information see the 'Resumption tokens' section for more information. The {metadata_format_*} specifies the metadata formats for the given data portal and is ised by the ```-mf``` option. Each line is a new metadata format. Lastly, {date_field} specifies the the field containing the desired date that should be saved for each record for the given metadata format.
Important to note is that the given URLs are able to use the OAI-PMH protocol or else the data harvesting won't work. For examples see the 'config.yaml' file containing the five data repositories 'Dryad', 'GBIF', 'Pangaea', 'Zenodo' and 'Figshare'.


### Example usage:

```shell
python metadata_harvester.py -dp dryad -lm 550 -fl
```
