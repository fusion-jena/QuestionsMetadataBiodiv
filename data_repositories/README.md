# Download metadata information of digital dataportals

Python scripts for downloading metadata information of digital dataportals. Works on [Python3+].




# Prerequisites

To start each script in this package successfully, you need a [Python3+] distribution and some other third-party tools.
How to install these tools, will be explained in the following lines:

## Instructions for Windows and Linux

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
[Pip] is used in this instruction to install the [Pandas] package.ons/data_repositories/README.md


### Requests: HTTP for Humans™

[Requests: HTTP for Humans™] is a third party [Python] tool with which you can easily POST and GET data of HTTP connections without the need for manual labor. To install the [Requests] module, simple type:

```shell

python -m pip install requests
```

or

```shell

python -m pip install requests
```

(whichever uses the correct [Python] version).


### XmlToDict

[XmlToDict] is a third party [Python] tool that is able to transform XML trees into dictionary for a easier parsing. To install the [XmlToDict] module, simple type:

```shell

python -m pip install xmltodict
```

or

```shell

python -m pip install xmltodict
```

(again, whichever uses the correct [Python] version).




# Script

## download_metadata.py

[download_metadata.py] is a simple to use Command Line Interface (CLI) tool to download and extract metadata information from the five digital dataportals Dryad, GBIF, Pangaea, Zenodo and Figshare. By default the script returns a CSV that shows which record (one line) used which metadata information (marked by '1' (used) or '0' (not used)) and their corresponding dates. The script has six options as input, '-dp', '-mf', '-fs', '-lm', '-fl' and '-sf'. '-dp' specifies from which dataportal the metadata should be downloaded. If a dataportal is specified that isn't part of the list of dataportals, an error is thrown. '-mf' specifies from which metadata format of the corresponding dataportal the metadata information will be downloaded. If a metadata format is specified that isn't part of the specified dataportal, an error is thrown. If no metadata format is specified, the metadata information of all metadata formats of the corresponding dataportal will be downloaded. '-fs' specifies whether the content of specific fields should be saved in an extra CSV file or not. Multiple fields are separated by commas. See the website of the corresponding dataportal for information about avaiable fields. Every field that was specified but did not appear in at least one record is printed at the end of the download. '-lm' specifies the maximum number of downloaded records. For example if set to 200, only the metadata information of the first 200 records are downloaded. '-fl' specifies if the full path to each metadata field should be saved instead of just the field itself. And '-sf' prints the avaiable metadata formats for the specified dataportal. The results are saved in a directory called 'metadata' that is automaticilly created in the directory from which the script is called. The name of the result CSV files are the date the download finished. An example of the first 550 records for each dataportal and metadata format can be found in the 'examples' directory.
Note: All five dataportals use the [Open Archives Initiative Protocol for Metadata Harvesting] ([OAI-PMH]) service to manage their metadata information. Records can't be downloaded all at once but are structured in pages. Each page contains 100 records and an index, called a resumption token, that is used to access the next page. Therefore, it is to note that each page has to be accessed individually which can take a long time if no or a high limit for the number of records is specified. The script also waits 60 seconds between each download of a metadata format to prevent connection issues. Furthermore, if a connection issue (or similiar) happens during the download, the script will wait for 30 seconds and resume from the last resumption token.


### Example usage:

```shell
#Go to the directoy where the python download_metadata.py script is saved and type:

python download_metadata.py -dp dryad -lm 550 -fl
```
