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
