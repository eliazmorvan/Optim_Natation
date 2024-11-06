# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:52:06 2024

@author: gcherot
"""
import functions as func
import os
import pandas as pd
from MILP.scrapper_results import (charger_donnees_licencies, init_driver, collecter_performances, 
                              sauver_performances_csv, charger_coefficients, enrichir_performances, 
                              filtrer_meilleures_performances)
from transform_data import (process_file)

def import_perf_indiv(PATH, sexe, MILP=True, in_other_team=None):   
    """
    Input :
        - in_other_team : dataframe
            1 if in other team
            0 otherwise
        - sexe : str
            'F' pour femmes, 'M' pour hommes"""         
    import pandas as pd

    def convert_to_float_0(s):
        try:
            s = s.replace(',', '.')
            s = s.replace(':', '*60+')
            return float(s)
        except ValueError:
            return 0

    def convert_to_float(s):
        if s == "#N/A":
            return 1000
        else :
            x = s.split(':')
            return 60*float(x[0]) + float(x[1])
        
    def cotation(s):
        x = s.split('.')
        return 60*float(x[0]) + float(x[1][:2]) + 0.01*float(x[1][2:])
    
        # Fichiers à utiliser
    fichier_licencies = '../csv/annuaire_licencies 2.csv'
    fichier_coefficients = '../csv/ffnex_coefficients_rajeunissement.csv'
    fichier_participation = PATH + 'participation_novembre.csv'
    fichier_performances_sortie = 'performances_nageurs.csv'

    """
    # Étape 1 : Charger les données des licenciés
    df_nageurs = charger_donnees_licencies(fichier_licencies)

    # Étape 2 : Initialiser le driver Selenium
    driver = init_driver()

    # Étape 3 : Collecter les performances avec le driver
    cache_performances = collecter_performances(df_nageurs, driver)

    # Étape 4 : Sauvegarder les performances collectées en CSV
    df_performances = sauver_performances_csv(cache_performances, fichier_performances_sortie)

    # Étape 5 : Charger les coefficients pour enrichir les performances
    df_coefficients = charger_coefficients(fichier_coefficients)

    # Étape 6 : Enrichir les performances avec les coefficients et les informations des licenciés
    df_final = enrichir_performances(df_performances, df_coefficients, df_nageurs)

    # Étape 7 : Filtrer les meilleures performances et les sauvegarder
    df_best_scores = filtrer_meilleures_performances(df_final)
    #df_best_scores[df_best_scores['Sexe'] == 'Homme'].to_csv('meilleures_performances_hommes.csv', index=False)
    #df_best_scores[df_best_scores['Sexe'] == 'Femme'].to_csv('meilleures_performances_femmes.csv', index=False)

    # Fermer le driver une fois le scraping terminé
    driver.quit()

    # Étape 8 : Utiliser transform_data pour traiter les fichiers créés
    # Processus pour les performances des femmes et des hommes
    process_file('./meilleures_performances_femmes.csv', fichier_participation, './csv/femmes_points_novembre.csv', 'F')
    process_file('./meilleures_performances_hommes.csv', fichier_participation, './csv/hommes_points_novembre.csv', 'M')
    """
    print("Le processus d'importation et de transformation des données est terminé.")

        
    # Spécifier le fichier selon le sexe
    if sexe == 'F':
        process_file(PATH + 'meilleures_performances_femmes.csv', fichier_participation, PATH + 'femmes_points_novembre.csv', sexe)
        nageur_points_file = PATH + "femmes_points_novembre.csv"
    else:
        process_file(PATH + 'meilleures_performances_hommes.csv', fichier_participation, PATH + 'hommes_points_novembre.csv', 'M')
        nageur_points_file = PATH + "hommes_points_novembre.csv"

    print(nageur_points_file)
    
    # Read the CSV file
    cols =['NomPrenom', 'Age', 'Sexe','100pap', '200pap', '100Dos', '200Dos', '100Br', '200Br', 
                  '100NL', '400NL', '1004N', '2004N',"50NL","200NL"]
    nage_indiv = ['100pap', '200pap', '100Dos', '200Dos', '100Br', '200Br', 
                  '100NL', '400NL', '1004N', '2004N']
    nage_relais = ['100pap', '100Dos', '100Br', '100NL']
    
    m = len(nage_indiv)
    r = len(nage_relais)
    
    # Charger les fichiers en fonction du sexe sélectionné
    nageur_point = pd.read_csv(nageur_points_file, sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float_0 for col in nage_indiv})
    relais_temps = pd.read_csv(PATH+"/relais_temps.csv", sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float for col in nage_relais})
    relais_coeff = pd.read_csv(PATH+"/relais_coef.csv", sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float_0 for col in nage_relais})
    participation = pd.read_csv(PATH+"participation_novembre.csv", sep=",",
                                encoding='ISO-8859-1',
                                converters={"Participation" : convert_to_float_0})
    participation = participation.set_index(list(participation.columns[[0,1]]))
    
    if in_other_team is None :
        participation["in_other_team"] = 1
    else :
        participation["in_other_team"] = 1-in_other_team
    
    # Définir les ID des relais
    id_10x50NL = 59
    id_4x504NMi = 98
    id_4x1004NMi = 36
    id_4x1004NM = 96
    id_4x1004ND = 46
    id_4x200NLM = 94
    id_4x200NLD = 44

    table_cotation = pd.read_csv(PATH+"/ffnex_table_cotation.csv", sep=";",
                                encoding='ISO-8859-1',
                                converters={"TEMPS" : cotation})
    
    relais_NL = table_cotation[table_cotation["EPREUVE_ID"]==id_10x50NL][["TEMPS","POINTS"]]
    relais_4N = table_cotation[table_cotation["EPREUVE_ID"]==id_4x1004NMi][["TEMPS","POINTS"]]
    relais_4x2 = table_cotation[table_cotation["EPREUVE_ID"]==id_4x200NLM][["TEMPS","POINTS"]]

    # Assurer que la colonne 'Sexe' est correcte
    nageur_point.loc[nageur_point["Sexe"] == "F", "Sexe"] = 0
    nageur_point.loc[nageur_point["Sexe"] == "M", "Sexe"] = 0  # Modifier pour les hommes
    
    nageur_point.fillna(0, inplace=True)
    
    if MILP :
        S = nageur_point[nage_indiv].to_numpy()
        T = (1/m)*nageur_point["50NL"].to_numpy()
        R = (1/r)*nageur_point[nage_relais].to_numpy()
        G = nageur_point["Sexe"].to_numpy()
        n = S.shape[0]
        return S, T, R, G, n, m, r, nageur_point
    
    else :
        nageur_point = nageur_point.set_index('NomPrenom')
        relais_temps = relais_temps.set_index('NomPrenom')
        relais_coeff = relais_coeff.set_index('NomPrenom')
        
        # Remove swimmers not available
        func.remove_swimmer(nageur_point, relais_temps, participation, nage_indiv, nage_relais)
        
        S = nageur_point[nage_indiv].copy()
        T = (1/m)*nageur_point["50NL"].copy()
        R = (1/r)*nageur_point[nage_relais].copy()
        G = nageur_point["Sexe"].copy()
        
        n = S.shape[0]
    
        # Time for each race
        T_4N = relais_temps[nage_relais].copy()
        # Coeff for each race
        RHO_4N = relais_coeff[nage_relais].copy()
        
        # Score calculation for each race in relay
        a_NL = func.approx_lin(relais_NL, 900, 1300)
        a_4N = func.approx_lin(relais_4N, 900, 1300)
    
        return S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, nageur_point, relais_NL, relais_4N