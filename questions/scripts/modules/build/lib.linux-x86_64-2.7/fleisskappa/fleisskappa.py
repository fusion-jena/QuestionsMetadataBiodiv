import numpy as np

def calculateP(pi_value_list, nounNumber):
    
    pi_array = np.array(pi_value_list)
    global_pi_value = np.sum(pi_array)
    p_value = float(global_pi_value) / nounNumber
    
    return p_value



def calculatePE_PEI(ratings, participantNumber, nounNumber, categoryNumber):
    
    point_list = list()
    if(isinstance(ratings, dict)):
        for point in ratings:
            
            point_list.append(ratings[point])
    else:
        point_list = ratings
    
    pe_value = 0
    pe_i_value = 0
    pj_value_list = list()
    pj_i_value_list = list()
    for point in point_list:
        
        pj_value = float(point) / (participantNumber * nounNumber)
        pj_value_list.append(pj_value)
        
        pj_i_value = pj_value * (1 - pj_value)
        pj_i_value_list.append(pj_i_value)
        
        pe_value = pe_value + (pj_value * pj_value)
        pe_i_value = pe_i_value + pj_i_value
        
    pe_i_value = pe_i_value * (1 / float(categoryNumber - 1))
    
    return (pe_value, pe_i_value, pj_value_list, pj_i_value_list)



def calculatePI(participantNumber, sumN):
    
    pi = 0
    div_value = participantNumber * (participantNumber - 1)
    if(div_value != 0):
        pi = (1 / float(div_value)) * sumN
        
    return pi



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



def calculateFleissKappa_GWET(p_value, pei_value):
    
    kappa_gwet = float(p_value - pei_value) / (1 - pei_value)
    
    return kappa_gwet



def calculateFleissKappa_GWET_Matrix(surveyMatrix):
    
    numpySurveyMatrix = np.array(surveyMatrix)
    nounNumber = numpySurveyMatrix.shape[0]
    categoryNumber = numpySurveyMatrix.shape[1]
    participantNumber = 0
    
    firstLine = True
    global_pi_value = 0
    
    for row in numpySurveyMatrix:
        
        sum_n = calculateSumN(row)
        if(firstLine):
            for col in range(len(row)):
            
                participantNumber = participantNumber + row[col]
        
        firstLine = False
        
        pi = calculatePI(participantNumber, sum_n)
        global_pi_value = global_pi_value + pi
        
    p = float(global_pi_value) / nounNumber
    
    
    points = np.sum(numpySurveyMatrix, axis=0)
    pe_pei = calculatePE_PEI(points, participantNumber, nounNumber, categoryNumber)
    
    kappa = float(p - pe_pei[0]) / (1 - pe_pei[0])
    gwet = float(p - pe_pei[1]) / (1 - pe_pei[1])
    
    return (kappa, gwet)
        
