#
# Split the content of a csv file
# input: expects a file in csv format (xml based column headers, comma-separated) in a dataportal/metadataformat folder
#
# output: xml files per <FileID>, header columns are used as xml tags
#
# @author: Felicitas Loeffler, 2019

import os
import csv
import argparse
import xml.etree.ElementTree as ET
import sys
import xml.dom.minidom

csv.field_size_limit(100000000)

# path to csv files
#root = 'test'

parser = argparse.ArgumentParser(description="Splits the csv content file of a data repository into individual files.")
parser.add_argument("-dp", "--dataportal", help="Select a dataportal(options: dryad, gbif, pangaea, zenodo, figshare)", required=True)
parser.add_argument("-mf", "--metadataFormat", help="Select a format(options: oai_dc, eml, pan_md, datacite)", required=True)

args = parser.parse_args()

dataportal = args.dataportal
metadataFormat = args.metadataFormat
path = dataportal+'/'+metadataFormat

subject_counts = {}
subject_index = -1
for subdir, dirs, filenames in os.walk(path):
	for file in filenames:
		#consider only csv files
		if file.endswith('.csv') and not file.endswith('_subject_counts.csv'):
			# open file
			csvFile = open(os.path.join(path,file), encoding="utf8")
			headers = csvFile.readline()
			xmlTags = headers.split(',')
			#print(xmlTags)
			# for each line in the csv file
			reader = csv.reader(csvFile, delimiter=',')
			for tag in xmlTags:
				inner_tag = tag.split("/")[-1]
				if("subject" in inner_tag):
					subject_index = xmlTags.index(tag)
					break

			for row in reader:
				try:
					if not row[0].startswith('id'):
						try:
							#print(row[0])
							# create the file structure
							data = ET.Element('data')
							for i, entry in enumerate(xmlTags):
								#print(row[i])
								item = ET.SubElement(data, entry.strip() )
								text = row[i].replace(';', ',')
								item.text = text
								if(subject_index == i):
									subjects = row[i].split("|")
									for subject in subjects:
										if(not subject in subject_counts):
											subject_counts[subject] = 1
										else:
											subject_counts[subject] += 1

							# create a new XML file with the results
							mydata = ET.tostring(data)
							filename = row[0]
							if '/' in filename:
								filenameSplit = row[0].split('/')
								filename = filenameSplit[1]
							if ':' in filename:
								filenameSplit = row[0].split(':')
								filename = filenameSplit[2]
							tree = ET.ElementTree(data)
							tree.write(dataportal+'/'+metadataFormat+'/'+filename+".xml")
							print(filename +'.xml')
						except IndexError as ex:
							maxColumn = str(len(xmlTags))
							print("ERROR: file %s doesn't contain %s colums" % (row[0],maxColumn))
				except Exception: #catch all other exceptions
					e = sys.exc_info()[0]
					print( row[0])
					print( "ERROR: %s" % e )

			csvFile.close()
			with open(path + "/" + file.split(".csv")[0] + "_subject_counts.csv", "w") as subject_writer:
				subject_list = []
				for subject, count in subject_counts.items():
					subject_list.append(subject + "," + str(count))

				subject_writer.write("subject,count" + "\n" + "\n".join(subject_list))
				del subject_list[:]
				written = True
