# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 12:18:30 2024

@author: gcherot
"""

import create_matrix as cre
import numpy as np
import pandas as pd

PATH = "../nageur_points.csv"
res, X, P, Y, S, T, R, G, df = cre.main(PATH,1,1)

Nageur = df.loc[P==1, "NomPrénom"]
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
        nage_relais.append("")
        
df = pd.DataFrame()
df["NomPrénom"] = Nageur
df["Indiv"] = nage_indiv
df["Relais_4N"] = nage_relais
df["Relais_NL"] = 10*[""]

df = pd.concat([df,pd.DataFrame({"NomPrénom":["","Total points"],
                                 "Indiv":["",np.sum(X*S)],
                                 "Relais_4N": ["",np.sum(Y*R)],
                                 "Relais_NL": ["",np.sum(P.flatten()*T)]})],
               ignore_index=True)

print(df)