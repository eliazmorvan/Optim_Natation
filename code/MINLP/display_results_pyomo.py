# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 10:48:42 2024

@author: gcherot
"""
import pandas as pd
import functions as func

def display_res(model, nageur_point, relais_NL, relais_4N, RHO_4N, T_4N):
    Nageur_indiv = []
    Nage_indiv = []
    Nageur_relais = []
    Nage_relais = []
    
    for i in model.X:
        if model.X[i].value == 1:
            Nageur_indiv.append(i[0])
            Nage_indiv.append(i[1])

    for i in model.Y:
        if model.Y[i].value == 1:
            Nageur_relais.append(i[0])
            Nage_relais.append(i[1])
    relais = pd.DataFrame()
    relais["NomPrénom"] = Nageur_relais
    relais["Nage relais"] = Nage_relais
    relais = relais.set_index('NomPrénom')
        
    
    df = pd.DataFrame()
    df["NomPrénom"] = Nageur_indiv
    df["Nage indiv"] = Nage_indiv
    df["Nage relais"] = ""
    df["Coeff relais 4N"] = 0
    df["Temps relais 4N"] = 0
    df = df.set_index('NomPrénom')
    
    for nom in df.index:
        nage = df.loc[nom,"Nage indiv"]
        df.loc[nom,"Points indiv"] = nageur_point.loc[nom, nage]
        df.loc[nom,"Temps relais NL"] = T_4N.loc[nom, "50NL"]
        df.loc[nom,"Coeff relais NL"] = RHO_4N.loc[nom, "50NL"]
        
        
        if nom in relais.index :
            nage = relais.loc[nom,"Nage relais"]
            df.loc[nom,"Nage relais"] = nage
            df.loc[nom,"Temps relais 4N"] = T_4N.loc[nom, nage]
            df.loc[nom,"Coeff relais 4N"] = RHO_4N.loc[nom, nage]
            
            
    temps_relais_NL = 10 * df["Temps relais NL"].sum()/df["Coeff relais NL"].sum()
    temps_relais_4N = 4 * df["Temps relais 4N"].sum()/df["Coeff relais 4N"].sum()
    
    points = pd.DataFrame()
    
    points["Points moyen indiv"] = [df["Points indiv"].mean()]
    points["Points relais NL"] = [func.point(temps_relais_NL, relais_NL)]
    points["Points relais 4N"] = [func.point(temps_relais_4N, relais_4N)]
    
    print()
    print(df[["Nage indiv", "Nage relais", "Points indiv"]])
    print()
    print()
    print(points)