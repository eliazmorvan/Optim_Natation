import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

def charger_donnees_licencies(fichier_licencies):
    df_nageurs = pd.read_csv(fichier_licencies, delimiter=';', encoding='utf-8')
    df_nageurs.columns = df_nageurs.columns.str.strip().str.replace(' ', '_').str.encode('utf-8').str.decode('utf-8')
    return df_nageurs

def init_driver():
    return webdriver.Chrome()

def rechercher_performance_bassin(driver, nageur, type_bassin):
    driver.get('https://ffn.extranat.fr/webffn/nat_recherche.php')
    champ_recherche = driver.find_element(By.ID, 'idrch')
    champ_recherche.clear()
    champ_recherche.send_keys(nageur)
    time.sleep(5)
    
    suggestion = driver.find_element(By.CSS_SELECTOR, "ul.ui-autocomplete li")
    if not suggestion:
        return {}
    suggestion.click()
    
    time.sleep(3)
    driver.find_element(By.ID, "idopt_prf").click()  # Sélectionner Performances
    time.sleep(4)
    
    bassin_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.ID, f"idbas_{'25' if type_bassin == '25m' else '50'}")
    ))
    bassin_radio.click()
    
    time.sleep(2)
    page_content = driver.page_source
    return extraire_performances(page_content, nageur)

def extraire_performances(page_content, nageur):
    soup = BeautifulSoup(page_content, 'html.parser')
    first_table = soup.find('table')
    
    if not first_table:
        return {}
    
    tbodies = first_table.find_all('tbody')
    performances = {}
    
    for tbody in tbodies:
        table_rows = tbody.find_all('tr')
        
        for row in table_rows:
            distance_cell = row.find("th")
            time_button = row.find('button')
            age_cell = row.find_all('td')[1]
            points_cell = row.find_all('td')[2]
            date_cell = row.find_all('td')[4]
            
            if distance_cell:
                distance = distance_cell.text.strip()
                result = time_button.find('a').text.strip() if time_button else row.find('td', class_='px-6 py-1 font-bold').text.strip()
                date = date_cell.text.strip() if date_cell else None
                age = age_cell.text.strip('()') if age_cell else None
                points = points_cell.text.strip('pts') if points_cell else None
                
                if distance not in performances:
                    performances[distance] = []
                performances[distance].append({
                    'Temps': result,
                    'Âge': age,
                    'Date': date,
                    'Points': points
                })
    
    return performances

def rechercher_performance(nageur, driver, cache_performances):
    if nageur in cache_performances:
        print(f"Utilisation du cache pour {nageur}.")
        return cache_performances[nageur]
    
    performances_25m = rechercher_performance_bassin(driver, nageur, "25m")
    performances_50m = rechercher_performance_bassin(driver, nageur, "50m")
    
    performances = {**performances_25m, **performances_50m}
    return performances

def collecter_performances(df_nageurs, driver):
    cache_performances = {}
    
    for _, row in df_nageurs.iterrows():
        nom_nageur = row['Nom_Prenom']
        print(f"Recherche des performances pour {nom_nageur}...")
        performances = rechercher_performance(nom_nageur, driver, cache_performances)
        cache_performances[nom_nageur] = performances
    
    return cache_performances

def sauver_performances_csv(cache_performances, fichier_sortie):
    data = []
    
    for nageur, performances in cache_performances.items():
        for distance, resultats in performances.items():
            for resultat in resultats:
                data.append({
                    'Nageur': nageur,
                    'Distance': distance,
                    'Temps': resultat.get('Temps', '#N/A'),
                    'Âge': resultat.get('Âge', '#N/A'),
                    'Date': resultat.get('Date', '#N/A'),
                    'Points': resultat.get('Points', '#N/A')
                })
    
    df_performances = pd.DataFrame(data)
    df_performances.to_csv(fichier_sortie, index=False)
    return df_performances

def charger_coefficients(fichier_coefficients):
    df_coefficients = pd.read_csv(fichier_coefficients, sep=";")
    df_coefficients[['Age_min', 'Age_max']] = df_coefficients['CATEGORIE'].apply(
        lambda x: pd.Series(extract_age_range(x))
    )
    return df_coefficients

def extract_age_range(categorie):
    match = re.search(r'(\d+)\s*-\s*(\d+)', categorie)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return None, None

def assign_category(age, df_coeff):
    row = df_coeff[(df_coeff['Age_min'] <= age) & (df_coeff['Age_max'] >= age)]
    return row['CATEGORIE'].values[0] if not row.empty else None

def enrichir_performances(df_performances, df_coefficients, df_nageurs):
    df_performances['Age'] = df_performances['Âge'].str.replace(' ans', '', regex=False).astype(int)
    df_performances['CATEGORIE'] = df_performances['Age'].apply(lambda age: assign_category(age, df_coefficients))
    df_performances['CATEGORIE'].fillna('Aucune', inplace=True)
    
    df_performances = pd.merge(df_performances, df_nageurs, left_on="Nageur", right_on="Nom_Prenom", how='left')
    df_performances['EPREUVE'] = df_performances.apply(transformer_epreuve, axis=1)
    
    df_final = pd.merge(df_performances, df_coefficients, on=['EPREUVE', 'CATEGORIE'], how='left')
    df_final['COEFFICIENT'] = df_final['COEFFICIENT'].fillna(1)
    df_final['Points_ajustes'] = round(df_final['Points'] / df_final['COEFFICIENT'], 0)
    
    return df_final

def transformer_epreuve(row):
    try:
        distance, style = row['Distance'].split(' ', 1)
    except ValueError:
        return "Épreuve inconnue"
    
    genre = "Dames" if row['Sexe'] == 'Femme' else "Messieurs"
    
    styles_dict = {
        "NL": "Nage Libre", "Dos": "Dos", "Bra.": "Brasse", 
        "Pap.": "Papillon", "4 N.": "4 Nages"
    }
    
    style_complet = styles_dict.get(style, style)
    return f"{distance} {style_complet} {genre}"

def filtrer_meilleures_performances(df_final):
    df_final['Date'] = pd.to_datetime(df_final['Date'])
    df_filtered = df_final[df_final['Date'] >= '2022-01-01']
    df_best_scores = df_filtered.loc[df_filtered.groupby(['Nageur', 'EPREUVE'])['Points_ajustes'].idxmax()]
    return df_best_scores.reset_index(drop=True)

"""
# Utilisation des fonctions
df_nageurs = charger_donnees_licencies('./csv/annuaire_licencies 2.csv')
driver = init_driver()

cache_performances = collecter_performances(df_nageurs, driver)
df_performances = sauver_performances_csv(cache_performances, 'performances_nageurs.csv')

df_coefficients = charger_coefficients('./csv/ffnex_coefficients_rajeunissement.csv')
df_final = enrichir_performances(df_performances, df_coefficients, df_nageurs)

df_best_scores = filtrer_meilleures_performances(df_final)

df_best_scores[df_best_scores['Sexe'] == 'Homme'].to_csv('meilleures_performances_hommes.csv', index=False)
df_best_scores[df_best_scores['Sexe'] == 'Femme'].to_csv("meilleures_performances_femmes.csv", index=False)

driver.quit()

"""