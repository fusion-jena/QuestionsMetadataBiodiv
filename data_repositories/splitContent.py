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
import traceback

csv.field_size_limit(100000000)

# path to csv files
#root = 'test'

parser = argparse.ArgumentParser(description="Splits the csv content file of a data repository into individual files.")
parser.add_argument("-c", "--csv", help="Set path to the data repository fields CSV file", required=True)
parser.add_argument("-f", "--field", help="Specify what field should be counted", type=str)
args = parser.parse_args()

keyword_counts = {}
field_index = -1
# open file
csvFile = open(args.csv, encoding="utf8")
headers = csvFile.readline()
xmlTags = headers.split(',')
#print(xmlTags)
# for each line in the csv file
reader = csv.reader(csvFile, delimiter=',')
for tag in xmlTags:
	inner_tag = tag.strip().split("/")[-1]
	if(args.field != None and field in inner_tag):
		field_index = xmlTags.index(tag)
		break

for row in reader:
	try:
		if(not row[0].startswith('id')):
			try:
				#print(row[0])
				# create the file structure
				data = ET.Element('data')
				for i, entry in enumerate(xmlTags):
					#print(row[i])
					tag_structure = entry.strip().split("/")
					parent_tag = data
					for tag in tag_structure:
						if(data.find(tag) == None):
							parent_tag = ET.SubElement(parent_tag, tag)
						else:
							parent_tag = data.find(tag)

					text = row[i].replace(';', ',')
					parent_tag.text = text
					if(args.field != None and field_index == i):
						content = row[i].split("|")
						for sub_content in content:
							sub_content = sub_content.split(";")
							for sub_sub_content in sub_content:
								stripped_sub_sub_content = sub_sub_content.strip()
								if(not stripped_sub_sub_content in keyword_counts):
									keyword_counts[stripped_sub_sub_content] = 1
								else:
									keyword_counts[stripped_sub_sub_content] += 1

				# create a new XML file with the results
				mydata = ET.tostring(data)
				filename = row[0]
				if('/' in filename):
					filenameSplit = row[0].split('/')
					filename = filenameSplit[1]
				if(':' in filename):
					filenameSplit = row[0].split(':')
					filename = filenameSplit[2]
				tree = ET.ElementTree(data)
				tree.write(args.csv+'/'+filename+".xml")
				print(filename +'.xml')
			except IndexError as ex:
				maxColumn = str(len(xmlTags))
				print("ERROR: file %s doesn't contain %s colums" % (row[0],maxColumn))
	except Exception: #catch all other exceptions
		e = sys.exc_info()[0]
		print( row[0])
		print("ERROR: %s" % e)
		print(traceback.format_exc())

csvFile.close()
if(args.field != None):
	with open(args.csv + "/" + file.split(".csv")[0] + "_keyword_counts.csv", "w", encoding="utf-8") as keyword_writer:
		keyword_list = []
		for sub_content, count in keyword_counts.items():
			keyword_list.append(sub_content + "," + str(count))

		keyword_writer.write(args.field + ",count" + "\n" + "\n".join(keyword_list))

del keyword_list[:]
