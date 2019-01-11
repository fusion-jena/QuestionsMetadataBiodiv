def calculatePI(responses, sumN):
	
	pi = 0
	div_value = responses * (responses - 1)
	if(div_value != 0):
		pi = (1 / div_value) * sumN
		
	return pi
