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
    # cols =['NomPrénom', 'Age', 'AnnéeNaissance', 'Cat', 'Sexe',
    #        'Coef', '50pap', '100pap', '50Dos', '100Dos', '50Br',
    #        '100Br', '50NL', '100NL', '200NL', '1004N', "present"]
    cols = ['Age', 'AnnéeNaissance', 'Cat', 'Sexe',
           'ReportTemps', 'Coef', 'TS', 'TS/coef', 'TS/coef \nmm,sscc', 'Si femme',
           'Si Monsieur', '50pap', 'ReportTemps2', 'Coef2', 'TS2', 'TS/coef3',
           'TS/coef mm,sscc4', 'Si femme5', 'Si Monsieur6', '100pap',
           'ReportTemps3', 'Coef3', 'TS3', 'TS/coef33', 'TS/coef mm,sscc44',
           'Si femme55', 'Si Monsieur66', '50Dos', 'ReportTemps4', 'Coef4',
           'TS232', 'TS/coef34', 'TS/coef mm,sscc45', 'Si femme56',
           'Si Monsieur67', '100Dos', 'ReportTemps5', 'Coef5', 'TS4', 'TS/coef35',
           'TS/coef mm,sscc46', 'Si femme57', 'Si Monsieur68', '50Br',
           'ReportTemps6', 'Coef6', 'TS5', 'TS/coef36', 'TS/coef mm,sscc47',
           'Si femme58', 'Si Monsieur69', '100Br', 'ReportTemps7', 'Coef7', 'TS6',
           'TS/coef37', 'TS/coef mm,sscc48', 'Si femme59', 'Si Monsieur610',
           '50NL', 'ReportTemps8', 'Coef8', 'TS7', 'TS/coef38',
           'TS/coef mm,sscc49', 'Si femme510', 'Si Monsieur611', '100NL',
           'ReportTemps9', 'Coef9', 'TS8', 'TS/coef39', 'TS/coef mm,sscc410',
           'Si femme511', 'Si Monsieur612', '200NL', 'ReportTemps10', 'Coef10',
           'TS9', 'TS/coef310', 'TS/coef mm,sscc411', 'Si femme512',
           'Si Monsieur613', '1004N', 'present']
    nage_indiv = ['50pap', '100pap', '50Dos', '100Dos', '50Br',
            '100Br', '50NL', '100NL', '200NL', '1004N']
    nage_relais = ['50pap', '50Dos', '50Br', '50NL']
    
    m = len(nage_indiv)
    r = len(nage_relais)
    
    converters = {col: convert_to_float for col in cols}
    
    df = pd.read_csv(PATH, sep=";", encoding='ISO-8859-1', converters=converters)
    df.loc[df["present"]==0, nage_indiv] = 0
    df.loc[df["Sexe"] == "F", "Sexe"] = 1
    df.loc[df["Sexe"] == "M", "Sexe"] = -1
    df.fillna(0, inplace=True)
    
    if MILP :
        S = df[nage_indiv].to_numpy()
        T = (1/m)*df["50NL"].to_numpy()
        R = (1/r)*df[nage_relais].to_numpy()
        G = df["Sexe"].to_numpy()
        n = S.shape[0]
        return S, T, R, G, n, m, r, df
    
    else :
        df = df.set_index('NomPrénom')
        S = df[nage_indiv].copy()
        T = (1/m)*df["50NL"].copy()
        R = (1/r)*df[nage_relais].copy()
        G = df["Sexe"].copy()
        
        n = S.shape[0]
    
        # Time for each race
        temps = df[['TS', 'TS3', 'TS5', 'TS7']].copy()
        rename = {'TS': '50pap',
                  'TS3': '50Dos',
                  'TS5': '50Br',
                  'TS7': '50NL',
                  }
        T_4N = temps.rename(columns=rename)
        # Coeff for each race
        coef = df[['Coef', 'Coef3', 'Coef5', 'Coef7']].copy()
        rename = {'Coef': '50pap',
                  'Coef3': '50Dos',
                  'Coef5': '50Br',
                  'Coef7': '50NL',
                  }
        RHO_4N = coef.rename(columns=rename)
        
        # Score calculation for each race in relay
        a_NL = -(1257-1000)/(60+44.4-2*60-47.7) #pt/s
        a_4N = -(1257-1000)/(3*60+57.2-4*60-39.5) #pt/s
    
        return S, T, R, G, T_4N, RHO_4N, n, m, r, a_NL, a_4N, df