# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:04:58 2024

@author: gcherot
"""
import scripts.create_matrix as cre
import scripts.display_results as disp

def execute_algorithm(PATH,sexe):
    res, X, P, Y, S, T, R, G, df = cre.main(PATH,sexe,1,1)
    disp.display(X, P, Y, S, T, R, df,sexe)
