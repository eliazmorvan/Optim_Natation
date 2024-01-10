# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:11:21 2024

@author: gcherot
"""
import numpy as np
import functions as func
import create_matrix as cr


def _test_flatten_variable():
    X = np.arange(0,24).reshape((6,4))
    print(X)
    Y, n = func.flatten_variable(X)
    print(Y)
    return Y, n
    
def _test_inverse_flatten_variable(Y, n):
    X = func.inverse_flatten_variable(Y, n)
    print(X)

def _test_consistancy():
    # Should pass
    S, T, R, G = func.import_data_fake(20,10,4)
    func.check_consistancy(S, T, R, G)
    
    try :
        S, _, R, G = func.import_data_fake(20,10,4)
        _, T, _, _ = func.import_data_fake(10,10,4)
        func.check_consistancy(S, T, R, G)
    except :
        print("n check passed")
        
    try :
        S, T, R, G = func.import_data_fake(20,8,4)
        func.check_consistancy(S, T, R, G)
    except :
        print("m check passed")
        
    try :
        S, T, R, G = func.import_data_fake(20,10,3)
        func.check_consistancy(S, T, R, G)
    except :
        print("r check passed")

def _test_create_c():
    S, T, R, G = func.import_data_fake(20,10,4)
    c = func.create_c(S, T, R)
    print(c)
    
def _test_create_14():
    A, bl, ul = cr.create_14(n=20,m=10,r=4)
    print(A)
    
def main():
    # Y, m = _test_flatten_variable()
    # _test_inverse_flatten_variable(Y, m)
    # _test_consistancy()
    # _test_create_c()
    # _test_create_14()
    
main()