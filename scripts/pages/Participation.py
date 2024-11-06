import streamlit as st
import pandas as pd
import os

# Définir le chemin vers le fichier CSV de participation
CSV_PATH = "csv/participation_novembre.csv"

def load_participation_data():
    # Charger les données de participation
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, encoding="ISO-8859-1",sep=",")
    else:
        st.warning("Le fichier de participation n'existe pas encore.")
        return pd.DataFrame()  # Retourne un dataframe vide si le fichier n'existe pas

def save_participation_data(data):
    # Sauvegarder les données de participation
    data.to_csv(CSV_PATH, index=False,sep=",",encoding="ISO-8859-1")
    st.success("Les modifications ont été enregistrées.")

# Interface de la page "Participation"
def participation_page():
    st.title("Participation des Nageurs")
    
    # Charger les données existantes
    participation_data = load_participation_data()
    
    if not participation_data.empty:
        # Afficher les données pour modification
        edited_data = st.data_editor(participation_data, num_rows="dynamic")
        
        # Bouton pour sauvegarder les modifications
        if st.button("Enregistrer les modifications"):
            save_participation_data(edited_data)
    else:
        st.info("Aucune donnée de participation n'est actuellement disponible.")

participation_page()