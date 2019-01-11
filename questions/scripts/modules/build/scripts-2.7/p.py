def calculateP(pi_value_list, nounNumber):
	
	global_pi_value = 0
	for pi_value in pi_value_list:
		
		global_pi_value = global_pi_value + pi_value
		
	p_value = global_pi_value / nounNumber
	return p_value
