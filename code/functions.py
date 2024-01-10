# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:20:18 2024

@author: gcherot
"""
import numpy as np

def import_data(PATH):
    return

def import_data_fake(n = 20, m = 10, r = 4):
    """
    n swimmers
    m races
    r races in the relay"""
    S = np.arange(0,n*m).reshape((n,m))
    T = np.arange(0,n*1).reshape((n,1))
    R = np.arange(0,n*r).reshape((n,r))
    return S, T, R
    

def check_consistancy(S, T, R):
    """Chack that all imported variable have the write shape"""
    ns, ms = S.shape
    nt, mt = T.shape
    nr, mr = R.shape
    
    assert ns == nt == nr
    
    assert ms == 10
    assert mt == 1
    assert mr == 4
    
def flatten_variable(X):
    """Return flattened array and initial number of rows."""
    return X.flatten(), X.shape[0]

def inverse_flatten_variable(Y, n):
    """Take flattened array and initial number of rows.
    Returns original array"""
    return Y.reshape(n,-1)

def build_variable(L):
    """L : list of variable"""
    return np.concatenate(L)

def build_constrains(L):
    return np.stack(L)

def create_c(S, T, R):
    S_f = flatten_variable(S)[0]
    T_f = flatten_variable(T)[0]
    R_f = flatten_variable(R)[0]
    c = build_variable((S_f, T_f, R_f))
    return c