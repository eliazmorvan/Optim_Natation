# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:52:06 2024

@author: gcherot
"""
import functions as func

def import_perf_indiv(PATH, MILP=True):            
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
        
    # Read the CSV file
    cols =['NomPrénom', 'Age', 'AnnéeNaissance', 'Cat', 'Sexe',
            'Coef', '50pap', '100pap', '50Dos', '100Dos', '50Br',
            '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_indiv = ['50pap', '100pap', '50Dos', '100Dos', '50Br',
            '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_relais = ['50pap', '50Dos', '50Br', '50NL']
    
    m = len(nage_indiv)
    r = len(nage_relais)
    
    nageur_point = pd.read_csv(PATH+"nageur_points.csv", sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float_0 for col in nage_indiv})
    relais_temps = pd.read_csv(PATH+"relais_temps.csv", sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float for col in nage_relais})
    relais_coeff = pd.read_csv(PATH+"relais_coef.csv", sep=";",
                               encoding='ISO-8859-1',
                               converters={col: convert_to_float_0 for col in nage_relais})
    participation = pd.read_csv(PATH+"participation.csv", sep=";",
                                encoding='ISO-8859-1',
                                converters={"Participation" : convert_to_float_0})
    
    id_10x50NL = 59
    id_4x504N = 98
    table_cotation = pd.read_csv(PATH+"ffnex_table_cotation.csv", sep=";",
                                encoding='ISO-8859-1',
                                converters={"TEMPS" : cotation})
    
    relais_NL = table_cotation[table_cotation["EPREUVE_ID"]==id_10x50NL][["TEMPS","POINTS"]]
    relais_4N = table_cotation[table_cotation["EPREUVE_ID"]==id_4x504N][["TEMPS","POINTS"]]
    
    # Remove swimmers not available
    func.remove_swimmer(nageur_point, relais_temps, participation, nage_indiv, nage_relais)
    
    nageur_point.loc[nageur_point["Sexe"] == "F", "Sexe"] = 1
    nageur_point.loc[nageur_point["Sexe"] == "M", "Sexe"] = -1
    nageur_point.fillna(0, inplace=True)
    
    if MILP :
        S = nageur_point[nage_indiv].to_numpy()
        T = (1/m)*nageur_point["50NL"].to_numpy()
        R = (1/r)*nageur_point[nage_relais].to_numpy()
        G = nageur_point["Sexe"].to_numpy()
        n = S.shape[0]
        return S, T, R, G, n, m, r, nageur_point
    
    else :
        nageur_point = nageur_point.set_index('NomPrénom')
        relais_temps = relais_temps.set_index('NomPrénom')
        relais_coeff = relais_coeff.set_index('NomPrénom')
        
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
        # a_NL = -(1257-1000)/(60+44.4-2*60-47.7) #pt/s
        # a_4N = -(1257-1000)/(3*60+57.2-4*60-39.5) #pt/s
    
        return S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, nageur_point, relais_NL, relais_4N