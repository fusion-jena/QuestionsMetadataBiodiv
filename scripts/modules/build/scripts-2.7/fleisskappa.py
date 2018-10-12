def calculateFleissKappa(p_value, pe_value):
	
	kappa = (p_value - pe_value) / (1 - pe_value)
	return kappa
