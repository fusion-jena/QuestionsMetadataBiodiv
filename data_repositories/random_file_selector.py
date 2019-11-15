import shutil
import os
import random
import argparse
import sys

parser = argparse.ArgumentParser(description="Choose a random number of individual files from a data repository")
parser.add_argument("-dp", "--dataportal", help="Select a dataportal (options: dryad, gbif, pangaea, zenodo, figshare)", required=True)
parser.add_argument("-mf", "--metadataformat", help="Select a format (options: oai_dc, eml, pan_md, datacite)", required=True)
parser.add_argument("-p", "--population", help="Set the number of files that will be selected", type=int, required=True)
parser.add_argument("-s", "--seed", help="Set the seed to obtain previous results", default=None)
args = parser.parse_args()

try:
    data_path = args.dataportal + "/" + args.metadataformat
    file_list = []
    for dirpath, dirnames, filenames in os.walk(data_path):
        for file in filenames:
            if(file.endswith(".xml")):
                file_list.append(file)

    if(not len(file_list)):
        raise Exception("No XML file found in path '" + data_path + "'.")

    if(args.population > len(file_list)):
        raise Exception("The population size cannot be larger than the number of files.")

    if(args.seed == None):
        args.seed = str(random.randrange(sys.maxsize))

    random.seed(args.seed)
    selected_files = random.sample(file_list, args.population)
    if(not os.path.exists(data_path + "/selected_files")):
        os.mkdir(data_path + "/selected_files")

    for file in selected_files:
        print(file)
        shutil.copyfile(data_path + "/" + file, data_path + "/selected_files/" + file)

    with open(data_path + "/selected_files/seed.txt", "w") as seedWriter:
        print("Seed: " + args.seed)
        seedWriter.write(str(args.seed))
except Exception as ex:
    print(sys.exc_info()[0])
    print(ex)
