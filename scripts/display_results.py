# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 12:18:30 2024

@author: gcherot
"""
import numpy as np
import pandas as pd

def display(PATH,X, P, Y, S, T, R, df,sexe):
    # Récupérer les noms des nageurs sélectionnés
    Nageur = df.loc[P == 1, "NomPrenom"]

    # Noms des épreuves individuelles
    nage_indiv_name = ['100pap', '200pap', '100Dos', '200Dos', '100Br',
                       '200Br', '100NL', '400NL', '1004N', '2004N']
    nage_indiv = []
    points_indiv = []  # Liste pour stocker les points individuels
    
    # Extraire les épreuves individuelles sélectionnées et les points
    for x, s in zip(X[P.flatten() == 1, :], S[P.flatten() == 1, :]):
        ind = np.where(x == 1)[0][0]  # Récupérer l'index de l'épreuve sélectionnée
        nage_indiv.append(nage_indiv_name[ind])
        points_indiv.append(s[ind])  # Récupérer les points correspondants
    
    # Noms des épreuves de relais
    nage_relais_name = ['100pap', '100Dos', '100Br', '100NL']
    nage_relais = []
    points_relais_4N = []  # Liste pour stocker les points des relais 4N
    
    # Extraire les épreuves de relais sélectionnées et les points
    for y, r in zip(Y[P.flatten() == 1, :], R[P.flatten() == 1, :]):
        try:
            ind = np.where(y == 1)[0][0]
            nage_relais.append(nage_relais_name[ind])
            points_relais_4N.append(r[ind])  # Récupérer les points du relais
        except:
            nage_relais.append("")
            points_relais_4N.append(0)  # Pas de relais pour ce nageur
    
    # Créer le DataFrame de résultats
    df_result = pd.DataFrame()
    df_result["NomPrénom"] = Nageur
    df_result["Indiv"] = nage_indiv
    df_result["Points_Indiv"] = points_indiv  # Ajouter les points individuels
    df_result["Relais_4N"] = nage_relais
    df_result["Points_Relais_4N"] = points_relais_4N  # Ajouter les points des relais 4N
    df_result["Relais_NL"] = 10 * [""]  # Placeholder pour le relais NL (peut être modifié si besoin)

    # Ajouter une ligne pour le total des points
    total_points_indiv = np.sum(X * S)
    total_points_relais_4N = np.sum(Y * R)
    total_points_relais_NL = np.sum(P.flatten() * T)
    
    df_totaux = pd.DataFrame({
        "NomPrénom": ["", "Total points"],
        "Indiv": ["", total_points_indiv],
        "Points_Indiv": ["", total_points_indiv],  # Points totaux individuels
        "Relais_4N": ["", total_points_relais_4N],
        "Points_Relais_4N": ["", total_points_relais_4N],  # Points totaux relais 4N
        "Relais_NL": ["", total_points_relais_NL]
    })

    # Concatenation des résultats et du total
    df_final = pd.concat([df_result, df_totaux], ignore_index=True)

    # Afficher le DataFrame
    print(df_final)

    df_final.to_csv(PATH + 'equipe_'+ sexe +'_novembre.csv', sep=";",index=False)
    
    return df_final