import streamlit as st
import pandas as pd
import os

st.header("Sélectionner un genre")
selected_gender = st.selectbox("Choisissez le genre", ["Homme", "Femme"])
st.write('Si vous ajoutez des temps, veuillez remplir à la main toutes les colonnes hormis la date, l\'age et la catégorie, en respectant bien le format.')

# Sélection du fichier en fonction du genre
file_gender = "M" if selected_gender == "Homme" else "F"
CSV_PATH = f"csv/meilleures_performances_{'hommes' if file_gender == 'M' else 'femmes'}.csv"

# Fonction pour charger les données
def load_performances_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, encoding="ISO-8859-1", sep=";")
    else:
        st.warning("Le fichier de performances n'existe pas encore.")
        return pd.DataFrame()

# Fonction pour sauvegarder les données
def save_performances_data(data):
    data.to_csv(CSV_PATH, index=False, sep=";", encoding="ISO-8859-1")
    st.success("Les modifications ont été enregistrées.")

# Interface de la page "Participation"
def performances_page():
    st.title("Meilleures performances des Nageurs")
    
    # Charger les données complètes
    full_data = load_performances_data()
    
    # Colonnes à afficher pour l'édition
    display_columns = ["Nageur", "Distance","EPREUVE","Age","Date","CATEGORIE","Temps","Points", "Points_ajustes"]
    
    if not full_data.empty:
        # Filtrage par texte
        query = st.text_input("Rechercher un nageur (par nom, prénom, etc.)").lower()
        if query:
            mask = full_data.applymap(lambda x: query in str(x).lower()).any(axis=1)
            filtered_data = full_data[mask]
        else:
            filtered_data = full_data
        
        # Afficher et éditer seulement certaines colonnes
        edited_data = st.data_editor(filtered_data[display_columns], num_rows="dynamic")
        
        # Bouton pour sauvegarder les modifications
        if st.button("Enregistrer les modifications"):
            # Mettre à jour les colonnes affichées dans les données complètes
            for col in display_columns:
                full_data.loc[filtered_data.index, col] = edited_data[col]
            
            # Sauvegarder les données complètes
            save_performances_data(full_data)
    else:
        st.info("Aucune donnée de performances n'est actuellement disponible.")

performances_page()