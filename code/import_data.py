# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:52:06 2024

@author: gcherot
"""


def import_perf_indiv(PATH):            
    import pandas as pd
    import numpy as np
    
    def convert_to_float(s):
        try:
            return float(s.replace(',', '.'))
        except ValueError:
            return 0  # or return None if you want to convert non-numeric strings to NaN


    # Read the CSV file
    cols =['Nom', 'Age', 'AnnéeNaissance', 'Cat', 'Sexe',
           'Coef', '50pap', '100pap', '50Dos', '100Dos', '50Br',
           '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_indiv = ['50pap', '100pap', '50Dos', '100Dos', '50Br',
            '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_relais = ['50pap', '50Dos', '50Br', '50NL']
    
    converters = {col: convert_to_float for col in nage_indiv}
    
    df = pd.read_csv(PATH, sep=";", encoding='ISO-8859-1', converters=converters)
    df = df[cols]
    df.loc[df["Sexe"] == "F", "Sexe"] = 1
    df.loc[df["Sexe"] == "M", "Sexe"] = -1
    df.fillna(0, inplace=True)
    
    S = df[nage_indiv].to_numpy()
    T = df["50NL"].to_numpy()
    R = df[nage_relais].to_numpy()
    G = df["Sexe"].to_numpy()
    
    n = S.shape[0]
    m = len(nage_indiv)
    r = len(nage_relais)
    
    return S, T, R, G, n, m, r, df