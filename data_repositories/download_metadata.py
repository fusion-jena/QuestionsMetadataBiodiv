import argparse
import requests
import xmltodict
import datetime
import time
import os
import traceback


dataportal = None
metadataformat = None
fields_list = None
limit = None
full = None
metadataDic = {}
fieldsDic = {}
dateDic = {}
dateFound = None
headerDate = None


#method for getting the command line arguments
def commandLine():

    global dataportal
    global metadataformat
    global fields_list
    global limit
    global full

    parser = argparse.ArgumentParser(description="Download and check metadata of datasets from a dataportal.")
    parser.add_argument("-dp", "--dataportal", help="Choose from what dataportal the metadata will be downloaded (options: dryad, gbif, pangaea, zenodo, figshare)", required=True)
    parser.add_argument("-mf", "--metadataformat", help="Specify from which metadata format the metadata will be downloaded (default: metadata from all formats will be downloaded)")
    parser.add_argument("-fs", "--fields", help="Set whether the content of specific fields should also be saved in an extra CSV file (see the fields.csv file of the respective datarepositories and metadata formats; multiple fields are separated by comma; default: the content of any field won't be saved)")
    parser.add_argument("-lm", "--limit", help="Only the first <limit> metadata sets will be downloaded (default: 0 {= all metadata sets})", type=int, default=0)
    parser.add_argument("-fl", "--full", help="Save the whole path of a field", action="store_true")

    args = parser.parse_args()

    dataportal = args.dataportal
    metadataformat = args.metadataformat
    fields = args.fields
    limit = args.limit
    full = args.full

    if(fields != None):
        fields_list = fields.split(",")



#method for download the metadata of a given datarepository and, optionally, a given metadata format
def downloadMetadata():

    global metadataDic
    global fieldsDic
    global dateFound
    global dateDic
    global headerDate

    #set metadata format for each datarepository
    prefixDic = {}
    prefixDic["dryad"] = ("oai_dc", "rdf", "ore", "mets")
    prefixDic["gbif"] = ("oai_dc", "eml")
    prefixDic["pangaea"] = ("oai_dc", "pan_md", "dif", "iso19139", "iso19139.iodp", "datacite3")
    prefixDic["zenodo"] = ("marcxml", "oai_dc", "oai_datacite", "marc21", "datacite", "datacite3", "datacite4", "oai_datacite3")
    prefixDic["figshare"] = ("oai_dc", "oai_datacite", "rdf", "cerif", "qdc", "mets")

    #set taken date stamps for each datarepository
    dateDic["dryad"] = ("dateAvailable", "dc:date", "atom:published")
    dateDic["gbif"] = ("pubDate", "dc:date" )
    dateDic["pangaea"] = ("publicationYear", "DIF_Creation_Date", "gco:Date", "dc:date", "md:dateTime")
    dateDic["zenodo"] = ("publicationYear", "dc:date")
    dateDic["figshare"] = ("dc:date", "publicationYear")

    if(not os.path.exists("metadata")):
        os.makedirs("metadata")

    if(not os.path.exists("metadata/" + dataportal)):
        os.makedirs("metadata/" + dataportal)

    with open("metadata/" + dataportal + "/" + dataportal + ".log", "w") as logWriter:
        logWriter.write("")

    #loop over each metadata format of the given datarepository
    for prefix in prefixDic[dataportal]:

        tokenIndex = 0
        breaking = False
        try:
            #counter for limit argument
            limit_counter = 0
            if(metadataformat == None or (metadataformat != None and metadataformat == prefix)):
                #set the metadata dictionary containing the used metadata items
                metadataDic[prefix] = {}
                metadataDic[prefix]["metadata"] = {}
                metadataDic[prefix]["date"] = {}
                metadataDic[prefix]["metadataList"] = list()

                if(fields_list != None):
                    #set the fields dictionary containing the content of the metadata items
                    fieldsDic[prefix] = {}

                wait = 5
                for timer in range(60*wait, 0, -1):

                    #time.sleep(1)
                    print("\033[K -- Wait " + str(timer) + " seconds", end="\r")

                print()
                #write log file for given metadata format
                os.system("echo \"- download metadata format '" + prefix + "'\" >> metadata/" + dataportal + "/" + dataportal + ".log")
                print(" -- download metadata format '" + prefix + "'")

                #get the datarepository URL for the given metadata format
                metadata_url = None
                if(dataportal == "dryad"):
                    metadata_url = "http://api.datadryad.org/oai/request?verb=ListRecords&metadataPrefix=" + prefix
                elif(dataportal == "gbif"):
                    metadata_url = "http://api.gbif.org/v1/oai-pmh/registry?verb=ListRecords&metadataPrefix=" + prefix
                elif(dataportal == "pangaea"):
                    metadata_url = "http://ws.pangaea.de/oai/provider?verb=ListRecords&metadataPrefix=" + prefix
                elif(dataportal == "zenodo"):
                    metadata_url = "https://zenodo.org/oai2d?verb=ListRecords&metadataPrefix=" + prefix
                elif(dataportal == "figshare"):
                    metadata_url = "https://api.figshare.com/v2/oai?verb=ListRecords&metadataPrefix=" + prefix
                else:
                    raise ValueError("Error: The data portal '" + dataportal + "' is not known. Please choose a valid dataportal (options: dryad, gbif, pangaea, zenodo, figshare).")

                #download the records (first page, first 100 records)
                metadata_request = requests.get(metadata_url)
                metadata_text = metadata_request.text
                #transform xml tree to dictionary
                metadata_content = xmltodict.parse(metadata_text.encode("utf-8"))
                resumptionToken = None
                #check if the current page has a resumption token
                #if yes, save the resumption token
                #if no, it's the last page
                if(isinstance(metadata_content["OAI-PMH"]["ListRecords"], dict) and "resumptionToken" in metadata_content["OAI-PMH"]["ListRecords"].keys() and metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"] != None and isinstance(metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"], dict) and "#text" in metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"].keys()):
                    resumptionToken = metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]["#text"]

                tokenIndex += 1
                print("\033[K  --- Resumption index: " + str(tokenIndex), end="\r")

                #add resumption token to log file of the metadata format
                os.system("echo \" -- resumptionToken " + str(resumptionToken) + "\" >> metadata/" + dataportal + "/" + dataportal + ".log")
                #loop over each record
                for record in metadata_content["OAI-PMH"]["ListRecords"]["record"]:

                    try:
                        #check if the limit counter is reached
                        #if yes, save the metadata (and, optionally, the fields) and go to next metadata format or quit
                        if(limit != 0 and limit_counter >= limit):
                            saveMetadata(prefix)
                            if(fields_list != None):
                                saveFields(prefix)

                            breaking = True
                            break

                        #only check the current record if it isn't deleted
                        if(isinstance(record, dict) and not ("@status" in record.keys() and record["@status"] == "deleted")):

                            #save the ID and header date stamp of the current record
                            identifier = record["header"]["identifier"]
                            headerDate = record["header"]["datestamp"]
                            metadataDic[prefix]["metadata"][identifier] = list()
                            dateFound = False

                            #only check the metadata items if the current record contains a metadata section
                            if("metadata" in record.keys()):
                                metadata_format = record["metadata"]
                                #loop over each item of the metadata section
                                for metadata in metadata_format:

                                    #check if the item contains further metadata items
                                    #if yes, check if the next item contains further metadata items (get to last item of the 'branch')
                                    #if no, save the item (and, optionally, the full path to the item)
                                    if(isinstance(metadata_format[metadata], dict)):
                                        if(full):
                                            checkKey(metadata_format[metadata], identifier, prefix, metadata)
                                        else:
                                            checkKey(metadata_format[metadata], identifier, prefix)
                                    else:
                                        #get the taken date stamp for the given metadata format (in case of Dryad the first one)
                                        if(not dateFound and metadata in dateDic[dataportal]):
                                            if(isinstance(metadata_format[metadata], list)):
                                                metadataDic[prefix]["date"][identifier] = metadata_format[metadata][0]
                                            else:
                                                metadataDic[prefix]["date"][identifier] = metadata_format[metadata]

                                            dateFound = True

                                        #only save the metadata item if it doesn't start with the attribute smybols '@' or '#'
                                        if(not (metadata.startswith("@") or metadata.startswith("#"))):
                                            if(not metadata in metadataDic[prefix]["metadata"][identifier]):
                                                metadataDic[prefix]["metadata"][identifier].append(metadata)
                                                if(not metadata in metadataDic[prefix]["metadataList"]):
                                                    metadataDic[prefix]["metadataList"].append(metadata)

                                        #optionally, save the content of the metadata item if it it isn't already saved
                                        if(fields_list != None and metadata in fields_list):

                                            if(not identifier in fieldsDic[prefix].keys()):
                                                fieldsDic[prefix][identifier] = {}

                                            if(not metadata in fieldsDic[prefix][identifier].keys()):
                                                fieldsDic[prefix][identifier][metadata] = list()

                                            fieldsDic[prefix][identifier][metadata].append(metadata_format[metadata].replace(",", ";").replace("\n", " "))

                                #if no date stamp was found, save the header date stamp
                                if(not identifier in metadataDic[prefix]["date"].keys() or metadataDic[prefix]["date"][identifier] == None):
                                    metadataDic[prefix]["date"][identifier] = headerDate + "_header"

                                limit_counter += 1
                    except:
                        continue

                if(breaking):
                    continue

                #loop over all paged till the last page (has no resumption token)
                while(resumptionToken != None):

                    #get the datarepository URL for the given metadata format
                    metadata_url = None
                    if(dataportal == "dryad"):
                        metadata_url = "http://api.datadryad.org/oai/request?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "gbif"):
                        metadata_url = "http://api.gbif.org/v1/oai-pmh/registry?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "pangaea"):
                        metadata_url = "http://ws.pangaea.de/oai/provider?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "zenodo"):
                        metadata_url = "https://zenodo.org/oai2d?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "figshare"):
                        metadata_url = "https://api.figshare.com/v2/oai?verb=ListRecords&resumptionToken=" + resumptionToken

                    #download the records (first page, first 100 records)
                    metadata_request = requests.get(metadata_url)
                    metadata_text = metadata_request.text
                    #transform xml tree to dictionary
                    metadata_content = xmltodict.parse(metadata_text.encode("utf-8"))
                    resumptionToken = None
                    #check if the current page has a resumption token
                    #if yes, save the resumption token
                    #if no, it's the last page
                    if(isinstance(metadata_content["OAI-PMH"]["ListRecords"], dict) and "resumptionToken" in metadata_content["OAI-PMH"]["ListRecords"].keys() and metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"] != None and isinstance(metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"], dict) and "#text" in metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]):
                        resumptionToken = metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]["#text"]

                    tokenIndex += 1
                    print("\033[K  --- Resumption index: " + str(tokenIndex), end="\r")

                    #add resumption token to log file of the metadata format
                    os.system("echo \" -- resumptionToken " + str(resumptionToken) + "\" >> metadata/" + dataportal + "/" + dataportal + ".log")
                    #loop over each record
                    for record in metadata_content["OAI-PMH"]["ListRecords"]["record"]:

                        try:
                            #check if the limit counter is reached
                            #if yes, save the metadata (and, optionally, the fields) and go to next metadata format or quit
                            if(limit != 0 and limit_counter >= limit):
                                saveMetadata(prefix)
                                if(fields_list != None):
                                    saveFields(prefix)

                                breaking = True
                                break

                            #only check the metadata items if the current record contain a metadata section
                            if(isinstance(record, dict) and not ("@status" in record.keys() and record["@status"] == "deleted")):

                                #save the ID and header date stamp of the current record
                                identifier = record["header"]["identifier"]
                                metadataDic[prefix]["metadata"][identifier] = list()
                                dateFound = False

                                #only check the metadata items if the current record contains a metadata section
                                if("metadata" in record.keys()):
                                    metadata_format = record["metadata"]
                                    #loop over each item of the metadata section
                                    for metadata in metadata_format:

                                        #check if the item contains further metadata items
                                        #if yes, check if the next item contains further metadata items (get to last item of the 'branch')
                                        #if no, save the item (and, optionally, the full path to the item)
                                        if(isinstance(metadata_format[metadata], dict)):
                                            if(full):
                                                checkKey(metadata_format[metadata], identifier, prefix, metadata)
                                            else:
                                                checkKey(metadata_format[metadata], identifier, prefix)
                                        else:
                                            #get the taken date stamp for the given metadata format (in case of Dryad the first one)
                                            if(not dateFound and metadata in dateDic[dataportal]):
                                                if(isinstance(metadata_format[metadata], list)):
                                                    metadataDic[prefix]["date"][identifier] = metadata_format[metadata][0]
                                                else:
                                                    metadataDic[prefix]["date"][identifier] = metadata_format[metadata]

                                                dateFound = True

                                            #only save the metadata item if it doesn't start with the attribute smybols '@' or '#'
                                            if(not (metadata.startswith("@") or metadata.startswith("#"))):
                                                if(not metadata in metadataDic[prefix]["metadata"][identifier]):
                                                    metadataDic[prefix]["metadata"][identifier].append(metadata)
                                                    if(not metadata in metadataDic[prefix]["metadataList"]):
                                                        metadataDic[prefix]["metadataList"].append(metadata)

                                            #optionally, save the content of the metadata item if it it isn't already saved
                                            if(fields_list != None and metadata in fields_list):

                                                if(not identifier in fieldsDic[prefix].keys()):
                                                    fieldsDic[prefix][identifier] = {}

                                                if(not metadata in fieldsDic[prefix][identifier].keys()):
                                                    fieldsDic[prefix][identifier][metadata] = list()

                                                fieldsDic[prefix][identifier][metadata].append(metadata_format[metadata].replace(",", ";").replace("\n", " "))

                                    #if no date stamp was found, save the header date stamp
                                    if(not identifier in metadataDic[prefix]["date"].keys() or metadataDic[prefix]["date"][identifier] == None):
                                        metadataDic[prefix]["date"][identifier] = headerDate + "_header"

                                    limit_counter += 1
                        except:
                            continue

                    if(breaking):
                        break

                if(breaking):
                    continue

                #save the metadata fields and, optionally, the content of the fields
                print()
                print(" -- finished download")
                saveMetadata(prefix)
                if(fields_list != None):
                    saveFields(prefix)
        except Exception as ex:
            try:
                #if exception was thrown, wait 5 minutes and restart from the last seen page
                wait = 5
                print(end="\n\n")
                print(str(traceback.print_exc()))
                print("Exception was thrown. Wait " + str(60 * wait) + " seconds and restart.", end="\n\n")
                for timer in range(60*wait, 0, -1):

                    time.sleep(1)
                    print("\033[K -- Wait " + str(timer) + " seconds", end="\r")

                print()
                #loop over all paged till the last page (has no resumption token)
                while(resumptionToken != None):

                    #get the datarepository URL for the given metadata format
                    metadata_url = None
                    if(dataportal == "dryad"):
                        metadata_url = "http://api.datadryad.org/oai/request?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "gbif"):
                        metadata_url = "http://api.gbif.org/v1/oai-pmh/registry?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "pangaea"):
                        metadata_url = "http://ws.pangaea.de/oai/provider?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "zenodo"):
                        metadata_url = "https://zenodo.org/oai2d?verb=ListRecords&resumptionToken=" + resumptionToken
                    elif(dataportal == "figshare"):
                        metadata_url = "https://api.figshare.com/v2/oai?verb=ListRecords&resumptionToken=" + resumptionToken

                    #download the records (first page, first 100 records)
                    metadata_request = requests.get(metadata_url)
                    metadata_text = metadata_request.text
                    #transform xml tree to dictionary
                    metadata_content = xmltodict.parse(metadata_text.encode("utf-8"))
                    resumptionToken = None
                    #check if the current page has a resumption token
                    #if yes, save the resumption token
                    #if no, it's the last page
                    if(isinstance(metadata_content["OAI-PMH"]["ListRecords"], dict) and "resumptionToken" in metadata_content["OAI-PMH"]["ListRecords"].keys() and metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"] != None and isinstance(metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"], dict) and "#text" in metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]):
                        resumptionToken = metadata_content["OAI-PMH"]["ListRecords"]["resumptionToken"]["#text"]

                    tokenIndex += 1
                    print("\033[K  --- Resumption index: " + str(tokenIndex), end="\r")

                    #add resumption token to log file of the metadata format
                    os.system("echo \" -- resumptionToken " + str(resumptionToken) + "\" >> metadata/" + dataportal + "/" + dataportal + ".log")
                    #loop over each record
                    for record in metadata_content["OAI-PMH"]["ListRecords"]["record"]:

                        try:
                            #check if the limit counter is reached
                            #if yes, save the metadata (and, optionally, the fields) and go to next metadata format or quit
                            if(limit != 0 and limit_counter >= limit):
                                saveMetadata(prefix)
                                if(fields_list != None):
                                    saveFields(prefix)

                                breaking = True
                                break

                            #only check the metadata items if the current record contain a metadata section
                            if(isinstance(record, dict) and not ("@status" in record.keys() and record["@status"] == "deleted")):

                                #save the ID and header date stamp of the current record
                                identifier = record["header"]["identifier"]
                                metadataDic[prefix]["metadata"][identifier] = list()
                                dateFound = False

                                #only check the metadata items if the current record contains a metadata section
                                if("metadata" in record.keys()):
                                    metadata_format = record["metadata"]
                                    #loop over each item of the metadata section
                                    for metadata in metadata_format:

                                        #check if the item contains further metadata items
                                        #if yes, check if the next item contains further metadata items (get to last item of the 'branch')
                                        #if no, save the item (and, optionally, the full path to the item)
                                        if(isinstance(metadata_format[metadata], dict)):
                                            if(full):
                                                checkKey(metadata_format[metadata], identifier, prefix, metadata)
                                            else:
                                                checkKey(metadata_format[metadata], identifier, prefix)
                                        else:
                                            #get the taken date stamp for the given metadata format (in case of Dryad the first one)
                                            if(not dateFound and metadata in dateDic[dataportal]):
                                                if(isinstance(metadata_format[metadata], list)):
                                                    metadataDic[prefix]["date"][identifier] = metadata_format[metadata][0]
                                                else:
                                                    metadataDic[prefix]["date"][identifier] = metadata_format[metadata]

                                                dateFound = True

                                            #only save the metadata item if it doesn't start with the attribute smybols '@' or '#'
                                            if(not (metadata.startswith("@") or metadata.startswith("#"))):
                                                if(not metadata in metadataDic[prefix]["metadata"][identifier]):
                                                    metadataDic[prefix]["metadata"][identifier].append(metadata)
                                                    if(not metadata in metadataDic[prefix]["metadataList"]):
                                                        metadataDic[prefix]["metadataList"].append(metadata)

                                            #optionally, save the content of the metadata item if it it isn't already saved
                                            if(fields_list != None and metadata in fields_list):

                                                if(not identifier in fieldsDic[prefix].keys()):
                                                    fieldsDic[prefix][identifier] = {}

                                                if(not metadata in fieldsDic[prefix][identifier].keys()):
                                                    fieldsDic[prefix][identifier][metadata] = list()

                                                fieldsDic[prefix][identifier][metadata].append(metadata_format[metadata].replace(",", ";").replace("\n", " "))

                                    #if no date stamp was found, save the header date stamp
                                    if(not identifier in metadataDic[prefix]["date"].keys() or metadataDic[prefix]["date"][identifier] == None):
                                        metadataDic[prefix]["date"][identifier] = headerDate + "_header"

                                    limit_counter += 1
                        except:
                            continue

                    if(breaking):
                        break

                if(breaking):
                    continue

                #save the metadata fields and, optionally, the content of the fields
                print()
                print(" -- finished download")
                saveMetadata(prefix)
                if(fields_list != None):
                    saveFields(prefix)
            except Exception as ex:
                print()
                #if an exception occurs, save the current metadata fields and, optionally, the content of the fields
                os.system("echo \"" + str(traceback.print_exc()) + "\" >> metadata/" + dataportal + "/" + dataportal + ".log")
                print(" -- finished exception download")
                saveMetadata(prefix)
                if(fields_list != None):
                    saveFields(prefix)



#method to get to the bottom/last item of a dictionary
def checkKey(dictionary, identifier, prefix, path=""):

    global metadataDic
    global fieldsDic
    global dateFound

    #loop over the keys and values of the given dictionary
    for key, value in dictionary.items():

        #check if the value is a dictionary
        #if yes, check again if the values of the this value are dictionaries or not
        #if no, check if the value is a list of items
        #if the value is no list, save the value as a metadata item
        if(isinstance(value, dict)):
            if(full):
                checkKey(value, identifier, prefix, path + "/" + key)
            else:
                checkKey(value, identifier, prefix)
        elif(isinstance(value, list)):
            #loop over each elements of the value list
            for element in value:
                #check if the element is a dictionary
                #if yes, check again if the values of this element are dictionaries or not
                #if no, save as the element as a metadata item
                if(isinstance(element, dict)):
                    if(full):
                        checkKey(element, identifier, prefix, path + "/" + key)
                    else:
                        checkKey(element, identifier, prefix)
                else:
                    #get the taken date stamp for the given metadata format (in case of Dryad the first one)
                    if(not dateFound and key in dateDic[dataportal]):
                        if(isinstance(value, list)):
                            metadataDic[prefix]["date"][identifier] = value[0]
                        else:
                            metadataDic[prefix]["date"][identifier] = value

                        dateFound = True

                    #only save the metadata element if it doesn't start with the attribute smybols '@' or '#'
                    #optionally, save the full path to this element
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
            #get the taken date stamp for the given metadata format (in case of Dryad the first one)
            if(not dateFound and key in dateDic[dataportal]):
                if(isinstance(value, list)):
                    metadataDic[prefix]["date"][identifier] = value[0]
                else:
                    metadataDic[prefix]["date"][identifier] = value

                dateFound = True

            #only save the metadata value if it doesn't start with the attribute smybols '@' or '#'
            #optionally, save the full path to this value
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



#method for saving the metadata items in a CSV file
#if the item appears in a record, a '1' is saved
#else, a '0' is saved
def saveMetadata(prefix):

    metadata_str_list = list()

    now = datetime.datetime.now()

    print(" -- save metadata format '" + prefix + "'")

    if(not os.path.exists("metadata/" + dataportal + "/" + prefix)):
        os.makedirs("metadata/" + dataportal + "/" + prefix)

    metadata_str = "id"
    for key in metadataDic[prefix]["metadataList"]:

        metadata_str = metadata_str + "," + key

    metadata_str = metadata_str + ",date"
    metadata_str_list.append(metadata_str)
    for identifier in metadataDic[prefix]["metadata"]:

        metadata_str = identifier
        if(len(metadataDic[prefix]["metadata"][identifier])):
            for key in metadataDic[prefix]["metadataList"]:

                found = "0"
                if(key in metadataDic[prefix]["metadata"][identifier]):
                    found = "1"

                metadata_str = metadata_str + "," + found

            metadata_str = metadata_str + "," + metadataDic[prefix]["date"][identifier]
            metadata_str_list.append(metadata_str)

    today = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    with open("metadata/" + dataportal + "/" + prefix + "/" + today + ".csv", "w") as metadataWriter:
        metadataWriter.write("\n".join(metadata_str_list))



#method for saving the content of each metadata item in a CSV file
def saveFields(prefix):

    fields_str_list = list()

    if(not os.path.exists("fields")):
        os.makedirs("fields")

    if(not os.path.exists("fields/" + dataportal)):
        os.makedirs("fields/" + dataportal)

    now = datetime.datetime.now()

    print(" -- save fields format '" + prefix + "'")

    if(not os.path.exists("fields/" + dataportal + "/" + prefix)):
        os.makedirs("fields/" + dataportal + "/" + prefix)

    fields_str = "id"
    for field in metadataDic[prefix]["metadataList"]:

        if(field in fields_list):
            fields_str = fields_str + "," + field

    fields_str_list.append(fields_str)
    for identifier in fieldsDic[prefix]:

        fields_str = identifier
        if(len(fieldsDic[prefix][identifier])):
            for field in fields_list:

                try:
                    if(field in fields_list):
                        fields_str = fields_str + "," + "<-->".join(fieldsDic[prefix][identifier][field])
                    else:
                        fields_str = fields_str + ","
                except KeyError as ke:
                    pass

            fields_str_list.append(fields_str)

    today = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
    with open("fields/" + dataportal + "/" + prefix + "/" + today + ".csv", "w") as fieldsWriter:
        fieldsWriter.write("\n".join(fields_str_list))

    notFound = False
    for field in fields_list:

        if(not field in metadataDic[prefix]["metadataList"]):
            if(not notFound):
                print(" -- the following fields are not in the metadata format: '" + prefix + "':")
                notFound = True

            print("  --- " + field)





try:
    now = datetime.datetime.now()
    print("\nProgram started " + str(now) + ".\n")
    commandLine()
    print("\n- download metadata from data portal '" + dataportal + "'")
    downloadMetadata()
    print("- download metadata from data portal '" + dataportal + "' finished\n")
except ValueError as ve:
    print(ve)
except requests.exceptions.ConnectionError:
    print("Unable to connect to the " + dataportal + " dryad portal.")
