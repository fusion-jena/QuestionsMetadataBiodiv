import argparse
import pandas as pd
import os
import krippendorff as kp


#parameter that saves at which column the actual data begin
column = None

#paramater that saves the name of the evaluation file
resultName = ""

#dictionary containing the line Strings of each participant: key - participant ID
persIDdict = dict()

#list containing the categories given by the user
categoryList = list()


#Method for the Command Line Interface, arguments: -f (input file/files) -c (input column of data begin)
#and -ct (input file with categories and descriptions)
#return: A dictionary containing another dictionary of each column of each file: first key - file name, second key - column name (first line)
def commandLine():
    
    global column
    global resultName
    global persIDdict
    global categoryList
    
    #set CLI commands
    parser = argparse.ArgumentParser(description="Evaluate the contents of a LSG-Result file.")
    parser.add_argument("-f", "--file", help="Input path to CSV-Result file", required=True, nargs="*")
    parser.add_argument("-c", "--col", type=int, help="Choose at which column the actual result data begin", required=True)
    parser.add_argument("-ct", "--category", help="Input path to the text file containing the categories", required=True)

    #parse arguments
    args = parser.parse_args()
    #get the path of each file saved in a list
    csv_files = args.file
    #set the column number at which the actual data begin
    column = args.col
    categories = args.category
    
    #initializing survey dictionary
    surveys = {}
    try:
        #loop over each file path in the file list
        for csv_file in csv_files:
            
            #set name of the evaluation file with the names of the individual file separated with "__"
            resultName = resultName + "__" + os.path.splitext(csv_file)[-2]
            #pandas module: fill the survey dictionary with the column dictionary of the files. The pandas module goes
            #through the first line of the CSV file and takes each field as the keys for the column dictionary
            surveys[csv_file] = pd.read_csv(csv_file, sep=",")
            
            for persID in surveys[csv_file]["id. Response ID"]:
                
                persIDdict[persID] = "Rater " + str(persID)
    except:
        raise KeyError("The program couldn't process the survey file '" + csv_file + "'. Please make sure to input the right survey files and that each file contain the field 'id. Response ID'.")
       
    with open(categories, "r") as cfile:
        content = cfile.readlines()
        for line in content:
            
            categoryList.append(line.split("|"))
            
    
    #return the survey dictionary
    return surveys
    



def buildKrippendorffMatrix(surveys):
    
    #dictionary containing the IDs for each category: key - category name
    categories = {}
    categoryIndex = 1
    for category in categoryList:
        
        categories[category[0].strip()] = categoryIndex
        categoryIndex = categoryIndex + 1
        
    categories["Other"] = categoryIndex
    categories["None"] = categoryIndex + 1
    
    #get the name of the first input survey
    surveyName = list(surveys)[0]
    #get the first input survey
    survey = surveys[surveyName]
    #initialize counting the current column number
    currentColumn = 0
    #number of term
    termNumber = 1
    #String for the first line of the Krippendorff CSV file
    firstTop = "Rater"
    #String for the second line of the Krippendorff CSV file
    secondTop = ""
    #String for the next-to-last line of the Krippendorff CSV file
    firstBottom = ""
    for category in categories:
        firstBottom = firstBottom + category.strip() + ","
        
    #String for the line of the Krippendorff CSV file
    secondBottom = ""
    for category in categories:
        secondBottom = secondBottom + str(categories[category.strip()]) + ","
    
    #initialize counting the current column number
    currentColumn = 0
    
    #loop over each question and noun of the first input survey --> first key
    for term in survey:
        
        #check if the question starts with the String 'researchfield'. If it does, leave the loop
        #--> end of the actual data in the file
        if(term.lower().startswith("researchfield")):
            break
        
        #check if the current column number is equal or greater than the user set column number (begin of actual data).
        #If it does, start parsing the data of the file. Else, continue to the next column and check again
        if(currentColumn >= column):
            #get the title name
            title = term.split(".")[0].split("[")[0]
            #check if the question is an 'other' of comment section. If it is, ignore this question and noun
            #and continue to the next question and/or noun. Else, parse the question and noun
            if(title[-1] == "C" or title[-2:] == "CQ"):
                continue
            else:
                #get the noun
                noun = term.split("].")[1].split("[")[1][:-1].replace(",", ";")
                firstTop = firstTop + ",<title>-Term" + str(termNumber)
                #increase the term number by 1        
                termNumber = termNumber + 1
                secondTop = secondTop + "," +  title + "-" + noun
                
                #loop over each participant ID
                for persID in persIDdict:
                    
                    try:
                        #loop over each survey of the survey dictionary
                        for surveyKey in surveys:
                            
                            #initialize the category String
                            category = ""
                            #get the list of participant IDs
                            persIDs = surveys[surveyKey]["id. Response ID"]
                            #initialize index of participant ID
                            surveyIDindex = None
                            #check if the survey contain the participant ID. If it does, get the index of the participant ID.
                            #Else, continue to the next survey
                            if(persID in persIDs.tolist()):
                                surveyIDindex = persIDs[persIDs == persID].index[0]
                            else:
                                continue
                            
                            #get the answer    
                            answer = str(surveys[surveyKey][term][surveyIDindex])
                            #if the answer is 'other', set the category String to 'Other'
                            if(answer.startswith("<div>other")):
                                category = "Other"
                            #if the answer is empty (no answer was given/NaN), set the category String to 'None'
                            elif(answer == "nan"):
                                category = "None"
                            #else, set the category String to the answer given by the survey
                            else:
                                category = answer.split("</span>")[0].split(">")[-1]
                            
                            try:
                                #append the line String of each participant by the category ID
                                persIDdict[persID] = persIDdict[persID] + "," + str(categories[category])
                            except:
                                raise IndexError("The program couldn't evaluate the category '" + category + "'. Please make sure that this category is contained in the 'categories' file.")
                    except IndexError as ie:
                        raise IndexError(ie)
                    except:
                        raise KeyError("The program couldn't find the question and term '" + term + "' in the survey file '" + surveyKey + "'. Please make sure that all files contain identical questions and terms.")
        
        
        #increase the current column number by 1        
        currentColumn = currentColumn + 1
        
        
        
    summary = ""
    for persID in persIDdict:
        
        summary = summary + persIDdict[persID] + "\n"
        
        
    krippendorff_matrix_str = summary.split("\n")
    krippendorff_matrix = [[int(i) for i in j.split(",")[1:]] for j in krippendorff_matrix_str if j]
    krippendorff = kp.alpha(reliability_data=krippendorff_matrix)
    krippendorff_nominal = kp.alpha(reliability_data=krippendorff_matrix, level_of_measurement='nominal')
    
    #writes the formatted results to the Krippendorff CSV file
    with open("lsg__krippendorff__" + resultName + ".csv", "w") as lsg:
        lsg.write(firstTop + "\n" + secondTop + "\n" + summary + "\n\n\n" + firstBottom + "\n" + secondBottom + "\n\nKrippendorff's alpha for interval metric," + str(krippendorff) + "\nKrippendorff's alpha for nominal metric," + str(krippendorff_nominal)) 
                        
    
    




#Main method for parsing the Result-CSV file and building the matrix
def startMatrixBuilding():
    
    try:
        surveys = commandLine()
        buildKrippendorffMatrix(surveys)
    except IndexError as ie:
        print(ie)
    except KeyError as ke:
        print(ke)
    
    
startMatrixBuilding()
