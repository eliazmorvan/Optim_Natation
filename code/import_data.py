# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:52:06 2024

@author: gcherot
"""


def import_perf_indiv(PATH, MILP=True):            
    import pandas as pd
    
    def convert_to_float(s):
        try:
            return float(s.replace(',', '.'))
        except ValueError:
            return 0  # or return None if you want to convert non-numeric strings to NaN

    # Read the CSV file
    cols =['NomPrénom', 'Age', 'AnnéeNaissance', 'Cat', 'Sexe',
           'Coef', '50pap', '100pap', '50Dos', '100Dos', '50Br',
           '100Br', '50NL', '100NL', '200NL', '1004N', "present"]
    nage_indiv = ['50pap', '100pap', '50Dos', '100Dos', '50Br',
            '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_relais = ['50pap', '50Dos', '50Br', '50NL']
    
    m = len(nage_indiv)
    r = len(nage_relais)
    
    converters = {col: convert_to_float for col in nage_indiv}
    
    df = pd.read_csv(PATH, sep=";", encoding='ISO-8859-1', converters=converters)
    df = df[cols]
    df.loc[df["present"]==0, nage_indiv] = 0
    df.loc[df["Sexe"] == "F", "Sexe"] = 1
    df.loc[df["Sexe"] == "M", "Sexe"] = -1
    df.fillna(0, inplace=True)
    
    if MILP :
        S = df[nage_indiv].to_numpy()
        T = (1/m)*df["50NL"].to_numpy()
        R = (1/r)*df[nage_relais].to_numpy()
        G = df["Sexe"].to_numpy()
    else :
        df = df.set_index('NomPrénom')
        S = df[nage_indiv]
        T = (1/m)*df["50NL"]
        R = (1/r)*df[nage_relais]
        G = df["Sexe"]
    
    n = S.shape[0]
    
    return S, T, R, G, n, m, r, df