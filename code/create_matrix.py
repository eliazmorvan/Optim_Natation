# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:41:54 2024

@author: gcherot
"""
import numpy as np
import functions as func

def create_14(n,m,r):
    A = np.zeros((m,n*m+n+r*n))
    for j in range(m):
        Ax = np.zeros((n,m))
        Ax[:,j] = 1
        Ap = np.zeros((1,n))
        Ay = np.zeros((n,r))
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[j] = func.build_variable((Ax, Ap, Ay))
    bl = np.ones(m)
    ul = np.ones(m)
    return A, bl, ul

def create_16(n,m,r):
    Ax = np.zeros((n,m))
    Ap = np.ones((1,n))
    Ay = np.zeros((n,r))
    
    Ax = func.flatten_variable(Ax)[0]
    Ap = func.flatten_variable(Ap)[0]
    Ay = func.flatten_variable(Ay)[0]
    
    A = func.build_variable((Ax, Ap, Ay))
    bl = m*np.ones(1)
    ul = m*np.ones(1)
    return A, bl, ul

def create_18(n,m,r):
    A = np.zeros((n,n*m+m+r*n))
    for i in range(n):
        Ax = np.zeros((n,m))
        Ax[i,:] = 1
        Ap = np.zeros((1,n))
        Ap[0,i] = 1
        Ay = np.zeros((n,r))
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[i] = func.build_variable((Ax, Ap, Ay))
    bl = np.zeros(n)
    ul = np.zeros(n)
    return A, bl, ul

def create_20(n,m,r):
    A = np.zeros((n,n*m+m+r*n))
    for i in range(n):
        Ax = np.zeros((n,m))
        Ap = np.zeros((1,n))
        Ap[0,i] = -1
        Ay = np.zeros((n,r))
        Ay[i,:] = 2
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[i] = func.build_variable((Ax, Ap, Ay))
    bl = -np.ones(n)
    ul = np.ones(n)
    return A, bl, ul





def main():
    n = 20
    m = 10
    r = 4
    S, T, R = func.import_data_fake(n,m,r)
    c = func.create_c(S, T, R)
    Nx = len(c) # size of x
    Nc = m+1+n+n+r+1 # number of constrains
    l = np.zeros(Nx)
    u = np.ones(Nx)