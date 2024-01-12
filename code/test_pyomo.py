# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 17:45:57 2024

@author: gcherot
"""

import pyomo.environ as pyo
import import_data as imp

PATH = "../nageur_points.csv"

S, T, R, G, n, m, r, df = imp.import_perf_indiv(PATH, MILP=False)

model = pyo.ConcreteModel()

model.I = pyo.Set(initialize=S.index)
model.J = pyo.Set(initialize=S.columns)

# the next line declares a variable indexed by the set J
model.X = pyo.Var(model.I, model.J, domain=pyo.Binary)

def obj_expression(model):
    return sum(model.X[i,j] * S.loc[i,j] for i in model.I for j in model.J)

model.OBJ = pyo.Objective(rule=obj_expression, sense=pyo.maximize)

def race_once(model, j):
    return sum(model.X[i,j] for i in model.I) == 1

# the next line creates one constraint for each member of the set model.I
model.cons_race_once = pyo.Constraint(model.J,rule=race_once)
model.c2 = pyo.Constraint(expr=sum(model.X[i,j] * S.loc[i,j] for i in model.I for j in model.J)*
                          pyo.log(sum(model.X[i,j] * S.loc[i,j] for i in model.I for j in model.J))+5.0 <= 0)

pyo.SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt') 