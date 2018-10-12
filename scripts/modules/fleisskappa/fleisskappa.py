import numpy as np


#Method for calculating the P value
#pi_value_list: List containing the P(i) values of each row
#nounNumber: Number of nouns in the survey
#return: The calculated P value
def calculateP(pi_value_list, nounNumber):
    
    pi_array = np.array(pi_value_list)
    global_pi_value = np.sum(pi_array)
    p_value = float(global_pi_value) / nounNumber
    
    return p_value



#Method for calculating the Pe, the Pe(I), the p(j) [list] and the p(j)(I) [list] values
#ratings: List or dictionary containing the overall scores of each category for all nouns in the survey
#participantNumber: Number of people that participated in the survey
#nounNumber: Number of nouns in the survey
#categoryNumber: Number of categories in the survey
#return: List containing the calulated Pe, Pe(I), p(j) [list] and p(j)(I) [list] values.
#        Indexing: 0 - Pe, 1 - Pe(I), 2 - p(j) [list], 3 - p(j)(I) [list]
def calculatePE_PEI(ratings, participantNumber, nounNumber, categoryNumber):
    
    point_list = list()
    if(isinstance(ratings, dict)):
        for point in ratings:
            
            point_list.append(ratings[point])
    else:
        point_list = ratings
    
    points = np.array(point_list)
    
    pe_value = 0
    pe_i_value = 0
    pj_value_list = points / (participantNumber * nounNumber)
    pj_i_value_list = pj_value_list * (1 - pj_value_list)
    pe_value = np.sum(pj_value_list**2)
    pe_i_value = np.sum(pj_i_value_list) * (1 / float(categoryNumber - 1))

    return (pe_value, pe_i_value, (pj_value_list).tolist(), (pj_i_value_list).tolist())



#Method for calculating the P(i) value
#participantNumber: Number of people that participated in the survey
#sumN: Value calculated by the 'calculateSumN'-function
#return: The calculated P(i) value
def calculatePI(participantNumber, sumN):
    
    pi = 0
    div_value = participantNumber * (participantNumber - 1)
    if(div_value != 0):
        pi = (1 / float(div_value)) * sumN
        
    return pi



#Method for calculating the sum over all n(ij)
#ratings: List or dictionary containing the local scores of each category for one noun in the survey
#return: The calculated sum over all n(ij)
def calculateSumN(ratings):
    
    point_list = list()
    if(isinstance(ratings, dict)):
        for point in ratings:
            
            point_list.append(ratings[point])
    else:
        point_list = ratings
    
    points = np.array(point_list)
    sumN = np.sum(points * (points-1))
        
    return sumN



#Method for the non-matrix based calcuation of the Kappa or GWET value depending on the input values
#p_value: The P value calculated by the 'calculateP'-function
#pei_value: The Pe or Pe(I) value calculated by the 'calculatePE_PEI'-function
#return: The calculated Kappa (if the Pe value was used) or GWET (if the Pe(I) value was used) value
def calculateFleissKappa_GWET(p_value, pei_value):
    
    kappa_gwet = float(p_value - pei_value) / (1 - pei_value)
    
    return kappa_gwet



#Method the matrix based calculation of the Kappa and GWET values
#surveyMatrix: A 2-dimensional matrix (list of lists) containing the local scores (each line)
#              of each category in the survey
#return: List containing the calculated Kappa und GWET values
#        Indexing: 0 - Kappa, 1 - GWET
def calculateFleissKappa_GWET_Matrix(surveyMatrix):
    
    numpySurveyMatrix = np.array(surveyMatrix)
    nounNumber = numpySurveyMatrix.shape[0]
    categoryNumber = numpySurveyMatrix.shape[1]
    participantNumber = np.sum(numpySurveyMatrix, axis=1)[0]

    global_pi_value = 0
    for row in numpySurveyMatrix:
        
        sum_n = calculateSumN(row)
        pi = calculatePI(participantNumber, sum_n)
        global_pi_value = global_pi_value + pi
        
    p = float(global_pi_value) / nounNumber
    
    points = np.sum(numpySurveyMatrix, axis=0)
    pe_pei = calculatePE_PEI(points, participantNumber, nounNumber, categoryNumber)
    
    kappa = float(p - pe_pei[0]) / (1 - pe_pei[0])
    gwet = float(p - pe_pei[1]) / (1 - pe_pei[1])
    
    return (kappa, gwet)
