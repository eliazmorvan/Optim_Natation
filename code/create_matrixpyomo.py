# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 22:06:56 2024

@author: gcherot
"""

import pyomo.environ as pyo
import import_data as imp

def concret_model(S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, linear):    
    model = pyo.ConcreteModel()
    
    model.n = pyo.Param(within=pyo.NonNegativeIntegers, initialize=n) # number of swimmers
    model.m = pyo.Param(within=pyo.NonNegativeIntegers, initialize=m) # Number of individual races
    model.r = pyo.Param(within=pyo.NonNegativeIntegers, initialize=r) # Number of races in the relay
    
    model.I = pyo.Set(initialize=S.index)
    model.J = pyo.Set(initialize=S.columns)
    model.K = pyo.Set(initialize=R.columns)
    
    # the next line declares a variable indexed by the set J
    model.X = pyo.Var(model.I, model.J, domain=pyo.Binary)
    model.P = pyo.Var(model.I, domain=pyo.Binary)
    model.Y = pyo.Var(model.I, model.K, domain=pyo.Binary)

    def obj_expression(model):
        model.OBJ_1 = sum(model.X[i,j] * S.loc[i,j] for i in model.I for j in model.J)
        if linear :
            model.OBJ_2 = sum(model.P[i] * T.loc[i] for i in model.I)
            model.OBJ_3 = sum(model.Y[i,k] * R.loc[i,k] for i in model.I for k in model.K)
        else :
            model.OBJ_2 = sum((-a_NL*10*model.P[i] * T_4N.loc[i,"50NL"] for i in model.I))/ \
                                    sum(model.P[i] * RHO_4N.loc[i,"50NL"] for i in model.I)
            model.OBJ_3 = sum((-a_4N*4*model.Y[i,k] * T_4N.loc[i,k] for i in model.I for k in model.K))/ \
                                    sum(model.Y[i,k] * RHO_4N.loc[i,k] for i in model.I for k in model.K)
        return sum([model.OBJ_1, model.OBJ_2, model.OBJ_3])

    model.OBJ = pyo.Objective(rule=obj_expression, sense=pyo.maximize)
    
    def race_once(model, j):
        return sum(model.X[i,j] for i in model.I) == 1
    
    def number_participants(model):
        return sum(model.P[i] for i in model.I) == 10
    
    def participate_to_race(model, i):
        return (sum(model.X[i,j] for j in model.J) - model.P[i]) == 0
    
    
    def relais4N_1(model, i):
        return (2*sum(model.Y[i,k] for k in model.K) - model.P[i]) <= 1
    
    def relais4N_2(model, k):
        return sum(model.Y[i,k] for i in model.I) == 1
    
    def relais4N_3(model):
        return sum(model.Y[i,k]*G.loc[i] for i in model.I for k in model.K) == 0
    
    # the next line creates one constraint for each member of the set model.I
    model.cons_race_once = pyo.Constraint(model.J, rule=race_once)
    model.cons_number_participants = pyo.Constraint(rule=number_participants)
    model.cons_participate_to_race = pyo.Constraint(model.I,rule=participate_to_race)
    
    model.cons_relais4N_1 = pyo.Constraint(model.I, rule=relais4N_1)
    model.cons_relais4N_2 = pyo.Constraint(model.K, rule=relais4N_2)
    model.cons_relais4N_3 = pyo.Constraint(rule=relais4N_3)
    
    return model


def main(PATH, linear=False):
    if linear :
        S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, df = imp.import_perf_indiv(PATH, MILP=False)
        model = concret_model(S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, linear)
        opt = pyo.SolverFactory('glpk')
        opt.solve(model)
    else :
        S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, df = imp.import_perf_indiv(PATH, MILP=False)
        model = concret_model(S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, linear)
        pyo.SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt') 
    return model


model = main("../nageur_points.csv", linear=True)
for i in model.X:
    if model.X[i].value == 1:
        print(i)

print("---------")
for i in model.Y:
    if model.Y[i].value == 1:
        print(i)