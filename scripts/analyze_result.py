import argparse
import pandas as pd
import fleisskappa as fk
import os


#number of people that participated in the surveys
participants = 0

#parameter that saves at which column the actual data begin
column = None

#paramater that saves the name of the evaluation file
resultName = ""

#list containing the categories given by the user
categoryList = list()


#Method for the Command Line Interface, arguments: -f (input file/files), -c (input column of data begin)
#and -ct (input file with categories and descriptions)
#return: A dictionary containing another dictionary of each column of each file: first key - file name, second key - column name (first line)
def commandLine():
    
    global participants
    global column
    global resultName
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
    #loop over each file path in the file list
    try:
        for csv_file in csv_files:
            
            #set name of the evaluation file with the names of the individual file separated with "__"
            resultName = resultName + "__" + os.path.splitext(csv_file)[-2]
            #pandas module: fill the survey dictionary with the column dictionary of the files. The pandas module goes
            #through the first line of the CSV file and takes each field as the keys for the column dictionary
            surveys[csv_file] = pd.read_csv(csv_file, sep=",")
            #increase the number of participants by the number of lines in the CSV file (excluding the first line)
            participants = participants + len(surveys[csv_file]["id. Response ID"])
    except:
        raise KeyError("The program couldn't process the survey file '" + csv_file + "'. Please make sure to input the right survey files and that each file contain the field 'id. Response ID'.")
    
    with open(categories, "r") as cfile:
        content = cfile.readlines()
        for line in content:
            
            categoryList.append(line.split("|"))
    
    #return the survey dictionary
    return surveys



#Method for parsing the data of the survey files and writing the results in a new evaluation CSV file
#surveys: A dictionary containing the files as the first key and the names of the columns of each file
#         as the seond key
def parseResults(surveys):
    
    #String for the first line of the evaluation CSV file
    top = ",,P(i),Sum over all n(ij),Total Responses,"
    #String for each following line
    fileResults = "\n"
    
    #dictionary containing all categories and saving the overall score of each category
    allpoints = {}
    for category in categoryList:
        
        allpoints[category[0].strip()] = 0
        top = top + category[0].strip() + ","
        
    allpoints["Other"] = 0
    allpoints["None"] = 0
    top = top + "Other,None,Other Category,Comment"
    
    globalTitle = ""
    
    #list containing the P(I) values of each question and noun
    p_i_list = list()
    #get the number of categories
    categories = len(allpoints)
    #initialize counting the number of nouns
    nounNumber = 0
    #boolean for checking if the first noun of the question is parsed
    firstNoun = True
    #get the name of the first input survey
    surveyName = list(surveys)[0]
    #get the first input survey
    survey = surveys[surveyName]
    #initialize counting the current column number
    currentColumn = 0
    
    #loop over each question and noun of the first input survey --> first key
    for question in survey:
        
        #dictionary containing all categories and saving the local score of each category
        #for each question and noun
        points = {}
        for category in categoryList:
            
            points[category[0].strip()] = 0
            
        points["Other"] = 0
        points["None"] = 0
        
        comments = ""
        #check if the question starts with the String 'researchfield'. If it does, leave the loop
        #--> end of the actual data in the file
        if(question.lower().startswith("researchfield")):
            break
        
        #check if the current column number is equal or greater than the user set column number (begin of actual data).
        #If it does, start parsing the data of the file. Else, continue to the next column and check again
        if(currentColumn >= column):
            
            #get the title name plus ID
            titleID = question.split(".")[0]
            #get the title name
            title = titleID.split("[")[0]
            #initialize the title
            localTitle = ""
            
            #check if a new question is parsed. If it is, set the title to the question title and the
            #firstNoun boolean to True again. Else, leave the title empty and firstNoun boolean False
            if(globalTitle != title):
                globalTitle = title
                localTitle = title
                firstNoun = True
            
            #check if the question is an 'other' of comment section. If it is, ignore this question and noun
            #and continue to the next question and/or noun. Else, parse the question and noun
            if(title[-1] == "C" or title[-2:] == "CQ"):
                continue
            else:
                #get the noun
                noun = question.split("].")[1].split("[")[1][:-1].replace(",", ";")
                #increase the number of nouns by 1
                nounNumber = nounNumber + 1
                #initialize String containing the other categories (one noun can have multiple other/custom categories)
                others = ""
                
                #loop over each survey of the survey dictionary
                for surveyKey in surveys:
                    
                    try:
                        #loop over each answer to the question (received by the first input survey) of each survey
                        for answer in surveys[surveyKey][question]:
                        
                            answer = str(answer)
                            #initialize the category String
                            category = ""
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
                                #increase the local and overall score of the given category by 1
                                points[category] = points[category] + 1
                                allpoints[category] = allpoints[category] + 1
                            except:
                                raise IndexError("The program couldn't evaluate the category '" + category + "'. Please make sure that this category is contained in the 'categories' file.")
                    except IndexError as ie:
                        raise IndexError(ie)
                    except:
                        raise KeyError("The program couldn't find the question and term '" + question + "' in the survey file '" + surveyKey + "'. Please make sure that all files contain identical questions and terms.")
                    
                    
                    
                    #block for getting the other/custom categories of each noun and the comments of
                    #each question. Since each question can only have one comment per participant,
                    #the comments are only get once and saved in the line of the first noun of each question
                    
                    #append a 'C' at the end of the question title to get the 'other' question        
                    otherTitle = titleID.split("[")[0] + "C[" + titleID.split("[")[1]
                    #as with the other/custom category, append a 'CQ' at the end of the question title
                    #to get the 'comment' question
                    commentTitle = titleID.split("[")[0] + "CQ"
                    #loop over each question of each survey
                    for otherBlock in surveys[surveyKey]:
                        
                        #check if the question is the 'other' title for this question title
                        if(otherTitle == otherBlock.split(".")[0]):
                            #if the 'other' question is found, loop over each answer
                            for answer in surveys[surveyKey][otherBlock]:
                               
                               answer = str(answer)
                               #if the answer is not empty, save the other/custom category
                               if(answer != "nan"): 
                                    others = others + answer + "::"
                        
                        #check if it is the first noun of the question and if the question is the 'comment' title
                        #for this question title           
                        elif(firstNoun and commentTitle == otherBlock.split(".")[0]):
                            #set the firstNoun boolean to False till the next question
                            firstNoun = False
                            #if the 'comment' question is found, loop over each answer
                            for answer in surveys[surveyKey][otherBlock]:
                                
                                answer = str(answer)
                                #if the answer is not empty, save the comment
                                if(answer != "nan"):
                                    comments = comments + answer + "::"
                    


            #calculation of the statistics      
            
            #sum of total responses for this noun
            sum_n = fk.calculateSumN(points)
            
            #calculate the P(I) value and add it to the P(I) list
            p_i = fk.calculatePI(participants, sum_n)
            p_i_list.append(p_i)
                 
            #block for building the each row of the evaluation CSV file
            rowResults = "," + str(p_i) + "," + str(sum_n) + "," + str(participants)
            for p in points:
                    
                rowResults = rowResults + "," + str(points[p])
                    
            rowResults = rowResults + "," + others[:-2].replace(",",";") + "," + comments[:-2].replace(",",";")            
            fileResults = fileResults + localTitle + "," + noun + rowResults + "\n"
        
        #increase the current column number by 1        
        currentColumn = currentColumn + 1
        
    
    
    #final block for building the evalutation CSV file by combining all individual rows
    #and adding the remaining calculations
       
    summary = "\n\n,Summary,,,"
    #loops through all answers containing the total number of selected answers to each noun
    #and saves it for the summary line
    for category in allpoints:
        
        summary = summary + "," + str(allpoints[category])
    
    #calculate the P value    
    p = fk.calculateP(p_i_list, nounNumber)
    summary = summary + "\n,P," + str(p) + ",,p(j),"
    
    #calculate Pe, Pe(I), p(j) and p(j)(I) values
    p_ei_j = fk.calculatePE_PEI(allpoints, participants, nounNumber, categories)
    p_e = p_ei_j[0]
    p_j_list = p_ei_j[2]
    p_e_i = p_ei_j[1]
    p_j_i_list = p_ei_j[3]
    
    for p_j in p_j_list:
        
        summary = summary + str(p_j) + ","
        
    summary = summary + "\n,,,,Pe," + str(p_e)
    
    summary = summary + "\n,,,,p(j)(I),"    
    for p_j_i in p_j_i_list:
        
        summary = summary + str(p_j_i) + ","
        
    summary = summary + "\n,,,,Pe(I)," + str(p_e_i)
    
    
    #calculate the Fleiss Kappa and GWET values
    kappa = fk.calculateFleissKappa_GWET(p, p_e)
    gwet = fk.calculateFleissKappa_GWET(p, p_e_i)
    summary = summary + "\n,Fleiss Kappa," + str(kappa) + "\n,GWET," + str(gwet)
    
    #writes the formatted results to the evaluation CSV file
    with open("lsg__" + resultName + ".csv", "w") as lsg:
        lsg.write(top + fileResults + summary) 
    
    

#Main method for parsing the CSV survey file/files and evaluating its/their results
def startEvaluation():
    
    try:
        surveys = commandLine()
        parseResults(surveys)
    except IndexError as ie:
        print(ie)
    except KeyError as ke:
        print(ke)
    
    
    
startEvaluation()
