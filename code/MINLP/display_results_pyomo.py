# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 10:48:42 2024

@author: gcherot
"""
import pandas as pd
import functions as func

def compute_dataframe_display(model, nageur_point, relais_NL, relais_4N, RHO_4N, T_4N, in_other_team):
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
    df["Coeff relais 4N"] = 0.0
    df["Temps relais 4N"] = 0.0
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
    
    if in_other_team is None :
        in_other_team=pd.DataFrame()
        in_other_team["NomPrénom"] = nageur_point.index
        in_other_team["swim_in_other_team"] = 0
        in_other_team = in_other_team.set_index('NomPrénom')
    in_other_team.loc[df.index,"swim_in_other_team"] = 1
    
    return in_other_team, df, points

def save_in_csv(equipe, points, PATH):
    with open(PATH+'best_team.csv','a') as f:
        for n in range(len(equipe)):
            f.write("Equipe "+str(n+1) +"\n")
            equipe[n][["Nage indiv", "Nage relais", "Points indiv"]].to_csv(f, sep=';', lineterminator="\n")
            f.write("\n")
            points[n].to_csv(f, sep=';', lineterminator="\n")
            f.write("\n")

def display(equipe, points):
    for n in range(len(equipe)):
        print("------------------------------------------")
        print("EQUIPE "+str(n+1))
        print(equipe[n][["Nage indiv", "Nage relais", "Points indiv"]])
        print()
        print(points[n])