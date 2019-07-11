import argparse
import requests
import xmltodict
import datetime
import time
import os
import xml.dom.minidom


#variable specifying the dataportal
dataportal = None
#variable specifying the metadata format (if given)
metadataformat = None
#variable specifying of which fields the content will be saved (if given)
fields_list = None
#variable specifying the maximum number fo records that will be downloaded (if given)
limit = None
#variable specifying if the full path to the field should be saved
full = None
#variable specifying the if the metadata formats for the given data portal should be printed
showformats = None
#dictionary containing the fields of the given metadata format
metadataDic = {}
#dictionary containing the contents of the fields of the given metadata format
fieldsDic = {}
#dictionary containing the metadata format for the given dataportal
prefixDic = {}
#dictionary containing the used dates for the given dataportal and metadata format
dateDic = {}
#variable specifying if a metadata date for the record was found
dateFound = None
#variable counting the number of parsed records for the 'limit' option
limit_counter = None
#list saving the raw metadata
xmlList = list()
#variable specifying the waiting time for a metadata format
startwait = None
#variable specifying the waiting time if an exception occurs
errorwait = None


#method for getting the command line arguments
def commandLine():

    #variable specifying the dataportal
    global dataportal
    #variable specifying the metadata format (if given)
    global metadataformat
    #variable specifying of which fields the content will be saved (if given)
    global fields_list
    #variable specifying the maximum number fo records that will be downloaded (if given)
    global limit
    #variable specifying if the full path to the field should be saved
    global full
    #variable specifying the path to the output XML file
    global harvestxml
    #variable specifying if the metadata formats for the given data portal should be printed
    global showformats
    #variable specifying the waiting time for a metadata format
    global startwait
    #variable specifying the waiting time if an exception occurs
    global errorwait

    #command line arguments
    parser = argparse.ArgumentParser(description="Harvest and check metadata of datasets from a dataportal.")
    parser.add_argument("-dp", "--dataportal", help="Choose from what dataportal the metadata will be harvested (options: dryad, gbif, pangaea, zenodo, figshare)", required=True)
    parser.add_argument("-mf", "--metadataformat", help="Specify from which metadata format the metadata will be harvested (default: metadata from all formats will be downloaded)")
    parser.add_argument("-fs", "--fields", help="Set whether the content of specific fields should also be saved in an extra CSV file (see the website of the respective datarepositories for avaiable fields; multiple fields are separated by comma; default: the content of no field will be saved)")
    parser.add_argument("-lm", "--limit", help="Only the first <limit> metadata sets will be harvested (default: 0 {= all metadata sets})", type=int, default=0)
    parser.add_argument("-fl", "--full", help="Save the whole path of a field", action="store_true")
    parser.add_argument("-hx", "--harvestxml", help="Path to output directory to save the raw metadata in an extra XML file")
    parser.add_argument("-sf", "--showformats", help="Show metadata format for the given dataportal", action="store_true")
    parser.add_argument("-sw", "--startwait", help="Set the time the program waits between the harvesting of each metadata format in seconds (default: 60)", type=int, default=60)
    parser.add_argument("-ew", "--errorwait", help="Set the time the program waits if an exception occurs in seconds (default: 30)", type=int, default=30)

    args = parser.parse_args()

    dataportal = args.dataportal
    metadataformat = args.metadataformat
    fields = args.fields
    limit = args.limit
    full = args.full
    harvestxml = None
    showformats = args.showformats
    startwait = args.startwait
    errorwait = args.errorwait

    #set the list of fields which contents will be saved (if specified by the user)
    if(fields != None):
        fields_list = fields.split(",")

    if(args.harvestxml != None):
        harvestxml = (args.harvestxml + "/").replace("//", "/")
        if(not os.path.exists(harvestxml)):
            os.makedirs(harvestxml)

    if(startwait < 0):
        startwait = 60

    if(errorwait < 0):
        errorwait = 30



#method for download the metadata of a given dataportal and, optionally, a given metadata format
def downloadMetadata():

    global xmlList

    #dictionary containing the fields of the given metadata format
    global metadataDic
    #dictionary containing the contents of the fields of the given metadata format
    global fieldsDic
    #dictionary containing the metadata format for the given dataportal
    global prefixDic
    #dictionary containing the used dates for the given dataportal and metadata format
    global dateDic
    #variable counting the number of the parsed resumption tokens for console output
    global tokenIndex
    #variable counting the number of parsed records for the 'limit' option
    global limit_counter

    #metadata formats
    #dictionary of the avaiable metadata formats of each dataportal
    prefixDic["dryad"] = ("oai_dc", "rdf", "ore")
    prefixDic["gbif"] = ("oai_dc", "eml")
    prefixDic["pangaea"] = ("oai_dc", "pan_md", "dif", "iso19139", "iso19139.iodp", "datacite3")
    prefixDic["zenodo"] = ("oai_dc", "oai_datacite", "datacite", "datacite3", "datacite4", "oai_datacite3")
    prefixDic["figshare"] = ("oai_dc", "oai_datacite", "rdf", "qdc")

    #date fields
    #dictionary of the used dates for each dataportal
    #dryad
    dateDic["dryad"] = dict()
    dateDic["dryad"]["oai_dc"] = "dc:date"
    dateDic["dryad"]["rdf"] = "dc:date"
    dateDic["dryad"]["ore"] = "atom:published"
    #gbif
    dateDic["gbif"] = dict()
    dateDic["gbif"]["oai_dc"] = "dc:date"
    dateDic["gbif"]["eml"] = "pubDate"
    #pangaea
    dateDic["pangaea"] = dict()
    dateDic["pangaea"]["oai_dc"] = "dc:date"
    dateDic["pangaea"]["pan_md"] = "md:dateTime"
    dateDic["pangaea"]["dif"] = "DIF_Creation_Date"
    dateDic["pangaea"]["iso19139"] = "gco:DateTime"
    dateDic["pangaea"]["iso19139.iodp"] = "gco:DateTime"
    dateDic["pangaea"]["datacite3"] = "publicationYear"
    #zenodo
    dateDic["zenodo"] = dict()
    dateDic["zenodo"]["oai_dc"] = "dc:date"
    dateDic["zenodo"]["oai_datacite"] = "publicationYear"
    dateDic["zenodo"]["oai_datacite3"] = "publicationYear"
    dateDic["zenodo"]["datacite"] = "publicationYear"
    dateDic["zenodo"]["datacite3"] = "publicationYear"
    dateDic["zenodo"]["datacite4"] = "publicationYear"
    #figshare
    dateDic["figshare"] = dict()
    dateDic["figshare"]["oai_dc"] = "dc:date"
    dateDic["figshare"]["oai_datacite"] = "publicationYear"
    dateDic["figshare"]["rdf"] = "vivo:datePublished"
    dateDic["figshare"]["qdc"] = "dc:date"

    #check if the given dataportal is avaiable
    if(not dataportal in prefixDic):
        print(" -> Unknown dataportal: " + dataportal)
        return

    #print all metadata formats of the given dataportal
    if(showformats):
        for mformat in prefixDic[dataportal]:
            print(" -- " + mformat)

        return

    #check if the given metadata format is avaiable
    if(metadataformat != None and not metadataformat in prefixDic[dataportal]):
        print(" -> Unknown metadata format '" + metadataformat + "' of dataportal: " + dataportal)
        return

    #create the metadata directory is it doesn't exist
    if(not os.path.exists("metadata")):
        os.makedirs("metadata")

    #create the dataportal directory in the metadata directory if it doesn't exist
    if(not os.path.exists("metadata/" + dataportal)):
        os.makedirs("metadata/" + dataportal)

    #write log file with the IDs of the resumption token of each metadata format
    with open("metadata/" + dataportal + "/" + dataportal + ".log", "w") as logWriter:
        logWriter.write("")

    #loop over each metadata format of the given dataportal
    for prefix in prefixDic[dataportal]:
        del xmlList[:]
        #set index for counting resumption token to 0
        tokenIndex = 0
        #set count for 'limit' option to 0
        limit_counter = 0
        #check if either a metadata format wasn't specified or if the current metadata format
        #is the same as the specified metadata format
        if(metadataformat == None or (metadataformat != None and metadataformat == prefix)):
            #set the metadata dictionary containing the used metadata fields
            metadataDic[prefix] = {}
            #sub-dictionary containing the fields of the metadata format of each record
            metadataDic[prefix]["metadata"] = {}
            #sub-dictionary containing the content of the date field of the metadata format
            metadataDic[prefix]["date"] = {}
            #sub-dictionary containing the combined fields of the metadata format of all records
            metadataDic[prefix]["metadataList"] = list()

            #check if the 'fields' option was used and the list of wanted fields is set
            if(fields_list != None):
                #set the fields dictionary containing the content of the metadata fields
                fieldsDic[prefix] = {}

            #wait 60 seconds between each download of a metadata format to prevent connection issues
            for timer in range(startwait, 0, -1):
                time.sleep(1)
                print("\033[K -- Sleep for " + str(timer) + " second(s)", end="\r")

            print("\033[K -- Sleep finished")

            #write part of log file for current metadata format
            os.system("echo \"- download metadata from metadata format '" + prefix + "'\" >> metadata/" + dataportal + "/" + dataportal + ".log")
            #print current metadata format
            print("  --- download metadata from metadata format '" + prefix + "'")
            #download the first page (first hundred records) of the metadata format and get the next resumption token
            resumptionToken = requestMetadata(prefix, None, True)
            #loop till you reach the last page -> has no resumption token == None
            while(resumptionToken != None):
                try:
                    #download the following pages and get the following resumption tokens
                    resumptionToken = requestMetadata(prefix, resumptionToken)
                except SystemError:
                    #if an error is thrown (error page, connection lost, etc.), wait 10 seconds
                    #and then resume from the last resumption token and try again
                    print()
                    print(" -> Exception was thrown. <-")
                    for timer in range(errorwait, 0, -1):
                        time.sleep(1)
                        print("\033[K  --- Restarting in " + str(timer) + " second(s)", end="\r")

                    print("\033[K  --- Restarted")
                except Exception as ex:
                    print(ex)

            #save the metadata fields of the metadata format
            print()
            print(" -- finished download")
            saveMetadata(prefix)
            #if fields were specified, save the content of the fields
            if(fields_list != None):
                saveFields(prefix)




def requestMetadata(prefix, resumptionToken, firstPage=False):

    global xmlList

    #dictionary containing the fields of the given metadata format
    global metadataDic
    #dictionary containing the contents of the fields of the given metadata format
    global fieldsDic
    #dictionary containing the metadata format for the given dataportal
    global prefixDic
    #dictionary containing the used dates for the given dataportal and metadata format
    global dateDic
    #variable  specifying if a metadata date for the record was found
    global dateFound
    #variable counting the number of the parsed resumption tokens for console output
    global tokenIndex
    #variable counting the number of parsed records for the 'limit' option
    global limit_counter

    try:
        #variable specifying the metadata url that will be requested
        metadata_content = None
        #dataportal urls
        #get the metadata url of the first page
        if(firstPage):
            try:
                #dryad url
                if(dataportal == "dryad"):
                    metadata_url = "http://api.datadryad.org/oai/request?verb=ListRecords&metadataPrefix=" + prefix
                #gbif url
                elif(dataportal == "gbif"):
                    metadata_url = "http://api.gbif.org/v1/oai-pmh/registry?verb=ListRecords&metadataPrefix=" + prefix
                #pangaea url
                elif(dataportal == "pangaea"):
                    metadata_url = "http://ws.pangaea.de/oai/provider?verb=ListRecords&metadataPrefix=" + prefix
                #zenodo url
                elif(dataportal == "zenodo"):
                    metadata_url = "https://zenodo.org/oai2d?verb=ListRecords&metadataPrefix=" + prefix
                #figshare url
                elif(dataportal == "figshare"):
                    metadata_url = "https://api.figshare.com/v2/oai?verb=ListRecords&metadataPrefix=" + prefix

                #request the records of the first page (contains 100 records)
                metadata_request = requests.get(metadata_url).text
                #transform the requested xml tree to a dictionary
                metadata_content = xmltodict.parse(metadata_request.encode("utf-8"))
            except:
                raise Exception("Unexpected error for the first page request! See message below:\n\n" + metadata_request)
        #get the metadata url of all following pages with the resumption token
        else:
            #dryad url
            if(dataportal == "dryad"):
                metadata_url = "http://api.datadryad.org/oai/request?verb=ListRecords&resumptionToken=" + resumptionToken
            #gbf url
            elif(dataportal == "gbif"):
                metadata_url = "http://api.gbif.org/v1/oai-pmh/registry?verb=ListRecords&resumptionToken=" + resumptionToken
            #pangaea url
            elif(dataportal == "pangaea"):
                metadata_url = "http://ws.pangaea.de/oai/provider?verb=ListRecords&resumptionToken=" + resumptionToken
            #zenodo url
            elif(dataportal == "zenodo"):
                metadata_url = "https://zenodo.org/oai2d?verb=ListRecords&resumptionToken=" + resumptionToken
            #figshare url
            elif(dataportal == "figshare"):
                metadata_url = "https://api.figshare.com/v2/oai?verb=ListRecords&resumptionToken=" + resumptionToken

            #request the records of each following page (each page contains 100 records)
            metadata_request = requests.get(metadata_url).text
            xmlFormatter = xml.dom.minidom.parseString(metadata_request)
            prettyXML = xmlFormatter.toprettyxml()
            xmlList.append(prettyXML)
            #transform the requested xml tree to a dictionary
            metadata_content = xmltodict.parse(metadata_request.encode("utf-8"))

        #set the resumption token to None
        resumptionToken = None
        if("ListRecords" in metadata_content["OAI-PMH"].keys()):
            #check if the current page has a resumption token
            #if yes, save the resumption token
            #if no, it's the last page
            if("resumptionToken" in metadata_content["OAI-PMH"]["ListRecords"].keys() and metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"] != None and isinstance(metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"], dict) and "#text" in metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"].keys()):
                resumptionToken = metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]["#text"]

            #increase the resumption index by 1 and print it
            tokenIndex += 1
            print("\033[K   ---- Resumption index: " + str(tokenIndex), end="\r")

            #add resumption token to log file of the metadata format
            os.system("echo \" -- resumptionToken " + str(resumptionToken) + "\" >> metadata/" + dataportal + "/" + dataportal + ".log")
            #loop over each record of the current page
            for record in metadata_content["OAI-PMH"]["ListRecords"]["record"]:
                identifier = None
                try:
                    #check if the limit counter is reached
                    #if yes, save the metadata (and, optionally, the fields) and go to next metadata format or quit
                    if(limit != 0 and limit_counter >= limit):
                        return None
                    #only check the current record if it isn't deleted
                    if(isinstance(record, dict) and not ("@status" in record.keys() and record["@status"] == "deleted")):
                        #only check the metadata fields if the current record contains a metadata section
                        if("metadata" in record.keys()):
                            #save the ID and header date stamp of the current record
                            identifier = record["header"]["identifier"]
                            #save the header date stamp of the current record
                            headerDate = record["header"]["datestamp"]
                            metadataDic[prefix]["date"][identifier] = None
                            #add the current record ID to the sub-dicitionary of the metadata dictionary
                            metadataDic[prefix]["metadata"][identifier] = list()
                            #set the date found variable to False
                            dateFound = False
                            metadata_format = record["metadata"]
                            #loop over each fields of the metadata section
                            for metadata in metadata_format:
                                #check if the field contains further metadata fields
                                #if yes, check if the next field contains further metadata fields (get to last field of the 'branch')
                                #if no, save the field (and, optionally, the full path to the field)
                                if(isinstance(metadata_format[metadata], dict)):
                                    checkKey(metadata_format[metadata], identifier, prefix, metadata)
                                else:
                                    #get the metadata date stamp for the given metadata format
                                    #in case of Dryad, the first one
                                    #in case of Pangaea ISO19139 and ISO19139.iodp, the date that contains the path
                                    ##'identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date'
                                    #in case of Figshare RDF, the attribute with the key 'vivo:datePublished'
                                    if(not dateFound and metadata == dateDic[dataportal][prefix]):
                                        if(isinstance(metadata_format[metadata], list)):
                                            metadataDic[prefix]["date"][identifier] = metadata_format[metadata][0]
                                            #set that the metadata date was found
                                            dateFound = True
                                        else:
                                            if(prefix == "iso19139" or prefix == "iso19139.iodp"):
                                                if("identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date" in path):
                                                    metadataDic[prefix]["date"][identifier] = value
                                                    #set that the metadata date was found
                                                dateFound = True
                                            elif(dataportal == "figshare" and prefix == "rdf"):
                                                metadataDic[prefix]["date"][identifier] = value.split("date")[-1]
                                                #set that the metadata date was found
                                                dateFound = True
                                            else:
                                                metadataDic[prefix]["date"][identifier] = value
                                                #set that the metadata date was found
                                                dateFound = True

                                    #only save the metadata field if it doesn't start with the attribute smybols '@' or '#'
                                    #and if it isn't already in the metadata dictionary
                                    #optionally, save the full path to this value
                                    if(not (metadata.startswith("@") or metadata.startswith("#"))):
                                        if(not metadata in metadataDic[prefix]["metadata"][identifier]):
                                            metadataDic[prefix]["metadata"][identifier].append(metadata)
                                            if(not metadata in metadataDic[prefix]["metadataList"]):
                                                metadataDic[prefix]["metadataList"].append(metadata)

                                    #optionally, save the content of the metadata field if it is set
                                    if(fields_list != None and metadata in fields_list):

                                        if(not identifier in fieldsDic[prefix].keys()):
                                            fieldsDic[prefix][identifier] = {}

                                        if(not metadata in fieldsDic[prefix][identifier].keys()):
                                            fieldsDic[prefix][identifier][metadata] = list()

                                        fieldsDic[prefix][identifier][metadata].append(metadata_format[metadata].replace(",", ";").replace("\n", " "))

                            #if no date stamp was found in the metadata section, set the Date to None
                            if(not dateFound or metadataDic[prefix]["date"][identifier] == None):
                                metadataDic[prefix]["date"][identifier] = headerDate + "_header"

                            #increase the limit counter for the 'limit' option by one
                            limit_counter += 1

                #if an KeyError or TypeError is thrown for the current record, ignore this one and go to the next record
                except KeyError:
                    metadataDic[prefix]["metadata"].pop(identifier, None)
                    continue
                except TypeError:
                    metadataDic[prefix]["metadata"].pop(identifier, None)
                    continue

    #if another error is thrown (for example connection errors), throw a SystemError and restart
    except:
        raise SystemError()

    #return the next resumnption token
    return resumptionToken




#method to get to the bottom/last field of a dictionary
def checkKey(dictionary, identifier, prefix, path):

    #dictionary containing the fields of the given metadata format
    global metadataDic
    #dictionary containing the contents of the fields of the given metadata format
    global fieldsDic
    #variable  specifying if a metadata date for the record was found
    global dateFound

    #loop over the keys and values of the given dictionary
    for key, value in dictionary.items():
        #check if the value is a dictionary
        #if yes, check again if the values of the this value are dictionaries or not
        #if no, check if the value is a list of fields
        #if the value is no list, save the value as a metadata field
        if(isinstance(value, dict)):
            if(full):
                checkKey(value, identifier, prefix, path + "/" + key)
            else:
                checkKey(value, identifier, prefix, key)
        elif(isinstance(value, list)):
            #loop over each elements of the value list
            for element in value:
                #check if the element is a dictionary
                #if yes, check again if the values of this element are dictionaries or not
                #if no, save as the element as a metadata field
                if(isinstance(element, dict)):
                    if(full):
                        checkKey(element, identifier, prefix, path + "/" + key)
                    else:
                        checkKey(element, identifier, prefix, key)
                else:
                    #get the metadata date stamp for the given metadata format
                    #in case of Dryad, the first one
                    #in case of Pangaea ISO19139 and ISO19139.iodp, the date that contains the path
                    ##'identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date'
                    #in case of Figshare RDF, the attribute with the key 'vivo:datePublished'
                    previousKey = path.split("/")[-1]
                    if(not dateFound and (key == dateDic[dataportal][prefix] or previousKey == dateDic[dataportal][prefix])):
                        if(isinstance(value, list)):
                            metadataDic[prefix]["date"][identifier] = value[0]
                            #set that the metadata date was found
                            dateFound = True
                        else:
                            if(prefix == "iso19139" or prefix == "iso19139.iodp"):
                                if("identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date" in path):
                                    metadataDic[prefix]["date"][identifier] = value
                                    #set that the metadata date was found
                                dateFound = True
                            elif(dataportal == "figshare" and prefix == "rdf"):
                                metadataDic[prefix]["date"][identifier] = value.split("date")[-1]
                                #set that the metadata date was found
                                dateFound = True
                            else:
                                metadataDic[prefix]["date"][identifier] = value
                                #set that the metadata date was found
                                dateFound = True

                        #set that the metadata date was found
                        dateFound = True

                    #save the current key, if it doesn't start with the attribute symbols '@' or '#'\
                    #else, save the previous key
                    #optionally, save the path to the (previous) key
                    if(not (key.startswith("@") or key.startswith("#"))):
                        if(full):
                            if(not path + "/" + key in metadataDic[prefix]["metadata"][identifier]):
                                metadataDic[prefix]["metadata"][identifier].append(path + "/" + key)
                                if(not path + "/" + key in metadataDic[prefix]["metadataList"]):
                                    metadataDic[prefix]["metadataList"].append(path + "/" + key)
                        else:
                            if(not key in metadataDic[prefix]["metadata"][identifier]):
                                metadataDic[prefix]["metadata"][identifier].append(key)
                                if(not key in metadataDic[prefix]["metadataList"]):
                                    metadataDic[prefix]["metadataList"].append(key)
                    else:
                        if(full):
                            if(not path in metadataDic[prefix]["metadata"][identifier]):
                                metadataDic[prefix]["metadata"][identifier].append(path)
                                if(not path in metadataDic[prefix]["metadataList"]):
                                    metadataDic[prefix]["metadataList"].append(path)
                        else:
                            previousKey = path.split("/")[-1]
                            if(not previousKey in metadataDic[prefix]["metadata"][identifier]):
                                metadataDic[prefix]["metadata"][identifier].append(previousKey)
                                if(not previousKey in metadataDic[prefix]["metadataList"]):
                                    metadataDic[prefix]["metadataList"].append(previousKey)

                    #optionally, save the content of the metadata element if it it isn't already saved
                    if(fields_list != None and key in fields_list):
                        if(not identifier in fieldsDic[prefix].keys()):
                            fieldsDic[prefix][identifier] = {}

                        if(full):
                            if(not path + "/" + key in fieldsDic[prefix][identifier].keys()):
                                fieldsDic[prefix][identifier][path + "/" + key] = list()

                            fieldsDic[prefix][identifier][path + "/" + key].append(value.replace(",", ";").replace("\n", " "))
                        else:
                            if(not key in fieldsDic[prefix][identifier].keys()):
                                fieldsDic[prefix][identifier][key] = list()

                            fieldsDic[prefix][identifier][key].append(value.replace(",", ";").replace("\n", " "))

        else:
            #get the metadata date stamp for the given metadata format
            #in case of Dryad, the first one
            #in case of Pangaea ISO19139 and ISO19139.iodp, the date that contains the path
            ##'identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date'
            #in case of Figshare RDF, the attribute with the key 'vivo:datePublished'
            previousKey = path.split("/")[-1]
            if(not dateFound and (key == dateDic[dataportal][prefix] or previousKey == dateDic[dataportal][prefix])):
                if(isinstance(value, list)):
                    metadataDic[prefix]["date"][identifier] = value[0]
                else:
                    if(prefix == "iso19139" or prefix == "iso19139.iodp"):
                        if("identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date" in path):
                            metadataDic[prefix]["date"][identifier] = value
                            #set that the metadata date was found
                            dateFound = True
                    elif(dataportal == "figshare" and prefix == "rdf"):
                        metadataDic[prefix]["date"][identifier] = value.split("date")[-1]
                        #set that the metadata date was found
                        dateFound = True
                    else:
                        metadataDic[prefix]["date"][identifier] = value
                        #set that the metadata date was found
                        dateFound = True

            #save the current key, if it doesn't start with the attribute symbols '@' or '#'\
            #else, save the previous key
            #optionally, save the path to the (previous) key
            if(not (key.startswith("@") or key.startswith("#"))):
                if(full):
                    if(not path + "/" + key in metadataDic[prefix]["metadata"][identifier]):
                        metadataDic[prefix]["metadata"][identifier].append(path + "/" + key)
                        if(not path + "/" + key in metadataDic[prefix]["metadataList"]):
                            metadataDic[prefix]["metadataList"].append(path + "/" + key)
                else:
                    if(not key in metadataDic[prefix]["metadata"][identifier]):
                        metadataDic[prefix]["metadata"][identifier].append(key)
                        if(not key in metadataDic[prefix]["metadataList"]):
                            metadataDic[prefix]["metadataList"].append(key)
            else:
                if(full):
                    if(not path in metadataDic[prefix]["metadata"][identifier]):
                        metadataDic[prefix]["metadata"][identifier].append(path)
                        if(not path in metadataDic[prefix]["metadataList"]):
                            metadataDic[prefix]["metadataList"].append(path)
                else:
                    if(not previousKey in metadataDic[prefix]["metadata"][identifier]):
                        metadataDic[prefix]["metadata"][identifier].append(previousKey)
                        if(not previousKey in metadataDic[prefix]["metadataList"]):
                            metadataDic[prefix]["metadataList"].append(previousKey)

            #optionally, save the content of the metadata value if it it isn't already saved
            if(fields_list != None and key in fields_list):

                if(not identifier in fieldsDic[prefix].keys()):
                    fieldsDic[prefix][identifier] = {}

                if(full):
                    if(not path + "/" + key in fieldsDic[prefix][identifier].keys()):
                        fieldsDic[prefix][identifier][path + "/" + key] = list()

                    fieldsDic[prefix][identifier][path + "/" + key].append(value.replace(",", ";").replace("\n", " "))
                else:
                    if(not key in fieldsDic[prefix][identifier].keys()):
                        fieldsDic[prefix][identifier][key] = list()

                    fieldsDic[prefix][identifier][key].append(value.replace(",", ";").replace("\n", " "))



#method for saving the metadata fields in a CSV file
#if the field appears in a record, a '1' is saved
#else, a '0' is saved
def saveMetadata(prefix):

    #list containing each line of the metadata CSV file
    metadata_str_list = list()
    #get the current date and time
    now = datetime.datetime.now()

    print(" -- save metadata from metadata format '" + prefix + "'")
    #create the dictionary of the metadata format it it doesn't already exist
    if(not os.path.exists("metadata/" + dataportal + "/" + prefix)):
        os.makedirs("metadata/" + dataportal + "/" + prefix)

    #add the first line with ID, all metadata fields and date to the metadata string list
    metadata_str = "id," + ",".join(metadataDic[prefix]["metadataList"]) + ",date"
    metadata_str_list.append(metadata_str)
    #loop over each ID in the metadata dictionary
    for identifier in metadataDic[prefix]["metadata"]:
        #set the ID of the record
        metadata_str = identifier
        #loop over each metadata field in the metadata fields list
        for key in metadataDic[prefix]["metadataList"]:
            #check if the current record contains the metadata field and was, therefore, set
            #if yes, add a 1 to the metadata string
            #if no, add a 0 to the metadata string
            found = "0"
            if(key in metadataDic[prefix]["metadata"][identifier]):
                found = "1"

            metadata_str += "," + found

        #add the date of the record to the metadata string
        metadata_str += "," + str(metadataDic[prefix]["date"][identifier])
        #add the metadata string (one line in the CSV file) to the metadata string list
        metadata_str_list.append(metadata_str)

    #set the current date and time
    today = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    #write the results to the CSV file
    with open("metadata/" + dataportal + "/" + prefix + "/" + today + ".csv", "w") as metadataWriter:
        metadataWriter.write("\n".join(metadata_str_list))

    if(harvestxml != None):
        if(not os.path.exists(harvestxml + dataportal)):
            os.makedirs(harvestxml + dataportal)

        if(not os.path.exists(harvestxml + dataportal + "/" + prefix)):
            os.makedirs(harvestxml + dataportal + "/" + prefix)

        with open(harvestxml + dataportal + "/" + prefix + "/" + today + ".xml", "w") as harvestWriter:
            harvestWriter.write("\n".join(xmlList))



#method for saving the content of each metadata field in a CSV file
def saveFields(prefix):
    #list containing each line of the metadata CSV file
    fields_str_list = list()

    #create the fields dictionaryit it doesn't already exist
    if(not os.path.exists("fields")):
        os.makedirs("fields")

    #create the fields dictionary of the dataportal it it doesn't already exist
    if(not os.path.exists("fields/" + dataportal)):
        os.makedirs("fields/" + dataportal)

    #get the current date and time
    now = datetime.datetime.now()

    print(" -- save fields format '" + prefix + "'")

    #create the fields dictionary of the metadata format it it doesn't already exist
    if(not os.path.exists("fields/" + dataportal + "/" + prefix)):
        os.makedirs("fields/" + dataportal + "/" + prefix)

    #set the first line of the fields CSV file
    fields_str = "id"
    #loop over each metadata field in the metadata fields list
    #and add it to the fields string if the fields list contains it
    for field in metadataDic[prefix]["metadataList"]:
        if(field in fields_list):
            fields_str += "," + field

    #add the first line with ID, all metadata fields and date to the metadata string list
    fields_str_list.append(fields_str)
    #loop over each ID in the fields dictionary
    for identifier in fieldsDic[prefix]:
        #set the ID of the record
        fields_str = identifier
        #loop over each field in the fields list
        for field in fields_list:
            #add the contents of the field to the fields string if the current record contains the field
            #else, add an empty string
            try:
                if(field in fields_list):
                    fields_str += "," + "<-->".join(fieldsDic[prefix][identifier][field])
                else:
                    fields_str += ","
            except KeyError as ke:
                pass

            #add the fields string (one line in the CSV file) to the fields string list
            fields_str_list.append(fields_str)

    #set the current date and time
    today = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    #write the results to the CSV file
    with open("fields/" + dataportal + "/" + prefix + "/" + today + ".csv", "w") as fieldsWriter:
        fieldsWriter.write("\n".join(fields_str_list))

    #loop over all fields in the fields list and print every field that didn't appear in at least one record
    notFound = False
    for field in fields_list:
        if(not field in metadataDic[prefix]["metadataList"]):
            if(not notFound):
                print(" -- the following fields are not in the metadata format: '" + prefix + "':")
                notFound = True

            print("  --- " + field)



#main method
if __name__ == '__main__':
    try:
        now = datetime.datetime.now()
        print("\nProgram started " + str(now) + ".\n")
        commandLine()
        print("- download metadata from dataportal '" + dataportal + "'")
        downloadMetadata()
        print("- download metadata from dataportal '" + dataportal + "' finished\n")
    except requests.exceptions.ConnectionError:
        print("Unable to connect to the '" + dataportal + "' portal.")
