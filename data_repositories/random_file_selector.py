import shutil
import os
import random
import argparse
import sys
from xml.dom import minidom
import traceback

parser = argparse.ArgumentParser(description="Choose a random number of individual files from a data repository")
parser.add_argument("-fs", "--files", help="Set the path to the directory with the XML files", required=True)
parser.add_argument("-p", "--population", help="Set the number of files that will be selected", type=int, required=True)
parser.add_argument("-s", "--seed", help="Set the seed to obtain previous results", default=None)
parser.add_argument("-f", "--filter", help="Specify keywords to filter out specific files; the first element is the field to filter, all following elements are the keywords; keywords are separated by comma")
parser.add_argument("-d", "--delete", help="Delete the output folder 'selected_files' if it already exists", action="store_true")
args = parser.parse_args()

try:
    filters = None
    if(args.filter != None):
        filters = args.filter.split(",")

    if(filters != None and len(filters) < 2):
        raise Exception("The '-f/--filter' option needs at least two elements")

    if(os.path.exists(args.files + "/selected_files")):
        if(args.delete):
            shutil.rmtree(args.files + "/selected_files")
        else:
            raise Exception("The output folder 'selected_files' in the directory '" + args.files + "' already exists. Delete it manually or use the '-d/--delete' option.")

    file_list = []
    print("\rLoading files...", end="")
    number_of_files = 0
    for dirpath, dirnames, filenames in os.walk(args.files):
        for file in filenames:
            if(file.endswith(".xml")):
                if(filters != None):
                    with open(args.files + "/" + file, "r") as xml_reader:
                        content = xml_reader.read().strip()
                        if("<" + filters[0] + ">" in content):
                            items = content.split("<" + filters[0] + ">")[-1].split("</" + filters[0] + ">")[0].split("|")
                            for item in items:
                                if(item.strip() in filters[1:]):
                                    file_list.append(file)
                                    number_of_files += 1
                                    print("\rLoaded " + str(number_of_files) + " file(s)", end="")
                                    break
                else:
                    file_list.append(file)
                    number_of_files += 1
                    print("\rLoaded " + str(number_of_files) + " file(s)", end="")

    print("\rLoading files -> done")
    if(not len(file_list)):
        raise Exception("No XML file found in path '" + args.files + "' or all files were filtered out.")

    if(args.population > len(file_list)):
        raise Exception("The population size cannot be larger than the number of files.")

    if(args.seed == None):
        args.seed = str(random.randrange(sys.maxsize))

    random.seed(args.seed)
    print("\rSelecting randomly " + str(args.population)  + " files...", end="")
    selected_files = random.sample(file_list, args.population)
    print("\rSelecting randomly " + str(args.population) + " files -> done")
    os.mkdir(args.files + "/selected_files")
    progress = 0
    for file in selected_files:
        shutil.copyfile(args.files + "/" + file, args.files + "/selected_files/" + file)
        progress += 1
        print("\rCopy progress: " + str(int((progress/len(selected_files))*100)) + "%", end="")

    print("\rCopy progress: finished")
    with open(args.files + "/selected_files/seed.txt", "w") as seedWriter:
        print("Seed: " + args.seed)
        seedWriter.write(str(args.seed))
except Exception as ex:
    print(ex)
    print(traceback.format_exc())
