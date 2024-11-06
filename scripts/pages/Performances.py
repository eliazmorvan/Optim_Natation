import streamlit as st
import pandas as pd
import os

st.header("Sélectionner un genre")
selected_gender = st.selectbox("Choisissez le genre", ["Homme", "Femme"])

# Sélection du fichier en fonction du genre
file_gender = "M" if selected_gender == "Homme" else "F"



if file_gender == "M":
    CSV_PATH = "csv/meilleures_performances_hommes.csv"
else :
    CSV_PATH = "csv/meilleures_performances_femmes.csv"

def load_performances_data():
    # Charger les données de performances
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, encoding="utf-8",sep=";")
    else:
        st.warning("Le fichier de performances n'existe pas encore.")
        return pd.DataFrame()  # Retourne un dataframe vide si le fichier n'existe pas

def save_performances_data(data):
    # Sauvegarder les données de participation
    data.to_csv(CSV_PATH, index=False,sep=";")
    st.success("Les modifications ont été enregistrées.")

# Interface de la page "Participation"
def performances_page():
    st.title("Meilleures performances des Nageurs")
    
    # Charger les données existantes
    participation_data = load_performances_data()
    
    if not participation_data.empty:
        # Afficher les données pour modification
        edited_data = st.data_editor(participation_data, num_rows="dynamic")
        
        # Bouton pour sauvegarder les modifications
        if st.button("Enregistrer les modifications"):
            save_performances_data(edited_data)
    else:
        st.info("Aucune donnée de performances n'est actuellement disponible.")

performances_page()