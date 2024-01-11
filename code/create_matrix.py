# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:41:54 2024

@author: gcherot
"""
import numpy as np
import functions as func
import import_data as imp

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
    
    A = np.zeros((1,n*m+n+r*n))
    A[0] = func.build_variable((Ax, Ap, Ay))
    bl = m*np.ones(1)
    ul = m*np.ones(1)
    return A, bl, ul

def create_18(n,m,r):
    A = np.zeros((n,n*m+n+r*n))
    for i in range(n):
        Ax = np.zeros((n,m))
        Ax[i,:] = -1
        Ap = np.zeros((n,1))
        Ap[i,:] = 1
        Ay = np.zeros((n,r))
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[i] = func.build_variable((Ax, Ap, Ay))
    bl = np.zeros(n)
    ul = np.zeros(n)
    return A, bl, ul

def create_20(n,m,r):
    A = np.zeros((n,n*m+n+r*n))
    for i in range(n):
        Ax = np.zeros((n,m))
        Ap = np.zeros((n,1))
        Ap[i,:] = -1
        Ay = np.zeros((n,r))
        Ay[i,:] = 2
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[i] = func.build_variable((Ax, Ap, Ay))
    bl = -np.ones(n)
    ul = np.ones(n)
    return A, bl, ul

def create_22(n,m,r):
    A = np.zeros((r,n*m+n+r*n))
    for k in range(r):
        Ax = np.zeros((n,m))
        Ap = np.zeros((1,n))
        Ay = np.zeros((n,r))
        Ay[:,k] = 1
        
        Ax = func.flatten_variable(Ax)[0]
        Ap = func.flatten_variable(Ap)[0]
        Ay = func.flatten_variable(Ay)[0]
        
        A[k] = func.build_variable((Ax, Ap, Ay))
    bl = np.ones(r)
    ul = np.ones(r)
    return A, bl, ul

def create_24(n,m,r,G):
    Ax = np.zeros((n,m))
    Ap = np.zeros((1,n))
    Ay = np.zeros((n,r))
    for i in range(n):
        Ay[i,:] = G[i]
    
    Ax = func.flatten_variable(Ax)[0]
    Ap = func.flatten_variable(Ap)[0]
    Ay = func.flatten_variable(Ay)[0]
    
    A = np.zeros((1,n*m+n+r*n))
    A[0] = func.build_variable((Ax, Ap, Ay))
    bl = np.zeros(1)
    ul = np.zeros(1)
    return A, bl, ul

def create_A_bl_ul(n,m,r,G):
    A14, bl14, ul14 = create_14(n,m,r)
    A16, bl16, ul16 = create_16(n,m,r)
    A18, bl18, ul18 = create_18(n,m,r)
    A20, bl20, ul20 = create_20(n,m,r)
    A22, bl22, ul22 = create_22(n,m,r)
    A24, bl24, ul24 = create_24(n,m,r,G)
    A = func.build_constrains((A14,A16,A18,A20,A22,A24))
    bl = func.build_constrains((bl14,bl16,bl18,bl20,bl22,bl24))
    ul = func.build_constrains((ul14,ul16,ul18,ul20,ul22,ul24))
    return A, bl, ul

def main(PATH):
    n = 20
    m = 10
    r = 4
    S, T, R, G = func.import_data_fake(n,m,r)
    S, T, R, G, n, m, r, df = imp.import_perf_indiv(PATH)
    A, bl, ul = create_A_bl_ul(n,m,r,G)
    c = func.create_c(S, T, R)
    Nx = len(c) # size of x
    l = np.zeros(Nx)
    u = np.ones(Nx)
    
    from scipy.optimize import LinearConstraint, milp, Bounds
    constraints = LinearConstraint(A, bl, ul)
    bounds = Bounds(lb=l, ub=u)

    res = milp(c=-c, constraints=constraints, bounds=bounds, integrality=np.ones(len(c)))
    
    X = func.inverse_flatten_variable(res.x[0:n*m],n)
    P = func.inverse_flatten_variable(res.x[n*m:n*(m+1)],n)
    Y = func.inverse_flatten_variable(res.x[n*(m+1):n*(m+r+1)],n)
    return res, X, P, Y, df