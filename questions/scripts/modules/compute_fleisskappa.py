import fleisskappa as fk
import numpy as np


def main():
    
    print()
    print("  example of data matrix and calculation of the Fleiss'Kappa and GWET values")
    print()
    
    #4 nouns, 10 categories and 7 participants
    data_matrix_string = (
   #c = category
   #c1   c2   c3   c4   c5   c6   c7   c8   c9   c10
    "  1    5    0    1    0    0    0    0    0    0", #noun 1
    "  0    0    1    4    0    0    1    0    0    1", #noun 2
    "  1    0    1    1    1    1    0    1    1    0", #noun 3
    "  0    0    0    0    0    0    7    0    0    0", #noun 4
    #the number of participants is the sum of any row
    )
    
    print("\n".join(data_matrix_string))
    print()
    
    data_matrix = [[int(v) for v in row.split()] for row in data_matrix_string]
    
    kappa_gwet = fk.calculateFleissKappa_GWET_Matrix(data_matrix)
    print("  Fleiss' Kappa: " + str(kappa_gwet[0]))
    print("      GWET     : " + str(kappa_gwet[1]))



if __name__ == '__main__':
    main()
