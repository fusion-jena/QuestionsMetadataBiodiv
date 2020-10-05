This folder contains supplementary material for the metadata standard analysis.

# metadata_standard_2020.csv

This file provides additional information about the selection process. All standards were obtained in September 2020 from re3data (https://www.re3data.org/) and RDA (https://rdamsc.bath.ac.uk/).
In re3data, we filtered  for "Life Sciences" and in RDA, we selecetd all top-level standards labeled with "Science". We merged and cleaned the list according to the following criteria: We ommitted deprecated standards, file formats, standards from clinical trails, astrophysics and astronomy. 


column header | meaning |
-------- | -------- | 
metadata standards  | the name of the metadata standard| 
comment | comment, e.g., reason why the standard was ommitted
website | the standard's website from which we collected all information | 
Number of repositories using the standard | if the standard is listed in re3data, number of repositories using the standard |
Use Case Entries  |if the standard is listed in RDA, number of use case entries|
in RDA Listed under "Sciences" |if the standard is listed in RDA, flag if it has the label "Science"|
Domain |the standard's domain|
Number of Elements |if available, number of elements|
Mandatory Elements |if available, number of mandatory elements|
Semantic Support |information whether the standard supports semantic formats, e.g., RDF, OWL|
Maintenance |information if the standard is still maintained, e.g., when was the last update? dead links? website available?|
Examples |if present, list some repositories/projects using the standard|


# comparison_standards_categories.csv

This file contains the actual comparision between the standards. Per category we analyzed whether one or more fields are available to describe the respective category.

column header | meaning |
-------- | -------- | 
metadata standard |the name of the metadata standards|
Website |the standard's website from which we collected all information| 
Environment |environmental information, e.g., biome, habitat|
Quality |data parameters measured or phenotypes, e.g., growth, length, pH|
Material |materials and chemicals, e.g., sediments, rocks, sand, CO2, N|
Organism |species |
Process |biological and chemical processes a specimen is involved, e.g., carbon cycling, weather|
Location |geographical location, e.g., Europe, Atlantic Ocean, latitude/longitude information|
Data Type |result of a research method, e.g., lidar data, genome data|
Anatomy |anatomical parts, e.g., leaf, root, genes|
Human Intervention |human intervention, e.g., farming, land use|
Event |processes at specific times, e.g., a specific earthquake, oil spill|
Time |temporal information, e.g., collection time|
Person |all person related information, e.g., data collector, funding information, responsible organization|

#### Legend:
* no match - empty cell
* general field - if no explicit metadata field represents the category, we marked that with a general field that could be used instead with a surrounding bracket, e.g., (dc:subject)
* explicit metadata field - at least one or more fields are mentioned that could be used to describe the respective category