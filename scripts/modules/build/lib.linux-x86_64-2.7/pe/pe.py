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
