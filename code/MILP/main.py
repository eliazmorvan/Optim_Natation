# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:04:58 2024

@author: gcherot
"""
import MILP.create_matrix as cre
import MILP.display_results as disp

def main(PATH):
    res, X, P, Y, S, T, R, G, df = cre.main(PATH,1,1)
    disp.display(X, P, Y, S, T, R, df)
    
main("../csv/")