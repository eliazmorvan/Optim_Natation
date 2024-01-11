# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 12:18:30 2024

@author: gcherot
"""

import create_matrix as cre
import numpy as np

PATH = "../nageur_points.csv"
res, X, P, Y, df = cre.main(PATH)

Nageur = df.loc[P==1, "Nom"]
nage_indiv_name = ['50pap', '100pap', '50Dos', '100Dos', '50Br',
        '100Br', '50NL', '100NL', '200NL', '1004N']
nage_indiv = []
for x in X[P.flatten()==1,:]:
    ind = np.where(x == 1)[0][0]
    nage_indiv.append(nage_indiv_name[ind])

nage_relais_name = ['50pap', '50Dos', '50Br','50NL']
nage_relais = []
for x in Y[P.flatten()==1,:]:
    try :
        ind = np.where(x == 1)[0][0]
        nage_relais.append(nage_relais_name[ind])
    except :
        nage_relais.append(None)
        
print(Nageur)
print(nage_indiv)
print(nage_relais)