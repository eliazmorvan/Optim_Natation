# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 18:04:58 2024

@author: gcherot
"""
import pyomo.environ as pyo

import MINLP.create_matrixpyomo as cre
import MINLP.display_results_pyomo as disp
import import_data as imp

def solve(PATH, linear=False):
    S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, nageur_point, relais_NL, relais_4N = imp.import_perf_indiv(PATH, MILP=False)
    model = cre.concret_model(S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, linear)
    if linear :
        opt = pyo.SolverFactory('glpk')
        opt.solve(model)
    else :
        pyo.SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt') 
    return model, nageur_point, relais_NL, relais_4N, RHO_4N, T_4N

def main(PATH, linear=False):
    model, nageur_point, relais_NL, relais_4N, RHO_4N, T_4N = solve(PATH, linear)
    disp.display_res(model, nageur_point, relais_NL, relais_4N, RHO_4N, T_4N)
    
main("../csv/", linear=False)