def calculateP(pi_value_list, nounNumber):
	
	global_pi_value = 0
	for pi_value in pi_value_list:
		
		global_pi_value = global_pi_value + pi_value
		
	p_value = global_pi_value / nounNumber
	return p_value



def calculatePE(ratings, participantNumber, nounNumber):
	
	point_list = ()
	if(isinstance(ratings, dict)):
		for point in global_points:
			
			point_list.append(ratings[point])
	else:
		point_list = ratings
	
	pe_value = 0
	pj_value_list = ()
	for point in point_list:
		
		pj_value = float(point) / (participantNumber * nounNumber)
		pj_value_list.append(pj_value)
		pe_value = pe_value + (pj_value *pj_value)
		
	return (pe_value, pj_value_list)



def calculatePI(responses, sumN):
	
	pi = 0
	div_value = responses * (responses - 1)
	if(div_value != 0):
		pi = (1 / div_value) * sumN
		
	return pi



def calculateSumN(ratings):
	
	point_list = ()
	if(isinstance(local_points, dict)):
		for point in ratings:
			
			point_list.append(ratings[point])
	else:
		point_list = ratings
	
	sumN = 0
	for point in point_list:
		
		sumN = sumN + (point * (point - 1))
		
	return sumN



def calculateFleissKappa(p_value, pe_value):
	
	kappa = (p_value - pe_value) / (1 - pe_value)
	return kappa
