# ChartCreator

This folder contains the source code to analyze the generated metadata csv files. The output are charts that display the elements utilized and how they match the search categories.

# Structure

* main.ChartCreator
	* main method, contains the location of the CSV files and defines which charts to plot
	* contains the methods to create the charts
	
* charts (contains the files to create BarCharts and LineCharts)
	* BarChart: metadata elements used per schema
	* LineChart: timeline of datasets per year
	* chart characteristics can be changed in the files

* data (folder that contains domain and data specific files)
	* category - describes the 14 search categories
	* CategoryToColorMap - defines which color to use for which category
	* TermToCategoryMap - mapping file that maps metadata elements to search categories
	* RepositorySummary und DatasetSummary - internal data structure to read csv files
		* RepositorySummary - Repository-Name, available metadata schemes and the actual data in DatasetSummary
		* DatasetSummary - saves Dataset-IDs, available elements, publication date, element filling (used/ not used)

* processors.io (package for data processing)
	* RepositorySummaryReader - loads the CSV files into an internal data structure (RepositorySummary and DatasetSummary)

# Prerequisites

requires Java 8 and Maven

# Usage

resolve all dependencies (chart libraries) and run 
```
maven install
```

set the path to the csv files

```
public static String path = "C:\\Daten\\data_repositories\\metadata";
```

then run the main method of ChartCreator.java, a new folder 'charts' is created in the same level where the pom.xml file is located
