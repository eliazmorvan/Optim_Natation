import pandas as pd
import os
import streamlit as st

from create_matrix import *
from import_data import *
from transform_data import *
from display_results import *

DATA_FOLDER = 'csv/'

# Titre et sélection du genre
st.title('Equipes Rennes Natation')
st.header("Sélectionner un genre")
selected_gender = st.selectbox("Choisissez le genre", ["Homme", "Femme"])

# Sélection du fichier en fonction du genre
file_gender = "M" if selected_gender == "Homme" else "F"
file_name = f"equipe_{file_gender}_novembre.csv"
file_path = os.path.join(DATA_FOLDER, file_name)

# Bouton pour rafraîchir les données
if st.button("Rafraîchir les données"):
    st.cache_data.clear()

# Charger et afficher le fichier sélectionné
if os.path.exists(file_path):
    st.write(f"### Fichier chargé : {file_name}")

    # Charger et afficher les résultats d'optimisation
    res, X, P, Y, S, T, R, G, df = matrix(DATA_FOLDER, file_gender, 1, 1)
    data = display(DATA_FOLDER, X, P, Y, S, T, R, df, file_gender)
    st.dataframe(data)
else:
    st.write(f"Le fichier {file_path} n'existe pas.")