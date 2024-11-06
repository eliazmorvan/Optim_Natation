import pandas as pd
import numpy as np
import streamlit as st
import os


DATA_FOLDER = 'data/'

# Streamlit options
st.set_page_config(
    page_title="Home")

# Sidebar for Date Picker
st.sidebar.markdown('# APP Rennes Natation v0.2')
st.sidebar.markdown('## Saison 2024-25')
st.sidebar.markdown(
    "## App de séléction d'équipes Rennes Natation.")
st.sidebar.image('img/RennesNat.jpg', use_column_width=True)

st.title('# APP Rennes Natation v.0.2')
st.write('## Saison 24/25')


st.markdown("""
    Sur mobile, veuillez cliquer sur la flèche en haut à gauche pour accéder au menu.

    Cette application vous permet d'analyser visuellement les performances des nageurs de Rennes Natation, pour choisir les équipes pour les compétitions.
    
    ### Utilisation de l'application Rennes Natation
    - Première section :
        - Page participation : Tableau à modifier en fonction de la disponibilité des nageurs
    - Deuxième section :
        - Page performances : Tableau à modifier avec les meilleurs performances des nageurs depuis le 01/01/2022
    - Troisième section :
        - Page équipes : Tableau des équipes optimales, par sexe
""")
