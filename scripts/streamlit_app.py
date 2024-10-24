import pandas as pd
import numpy as np
import streamlit as st
import os


DATA_FOLDER = 'csv/'

# Streamlit options
st.set_page_config(layout="wide")

# ST title
st.title('Equipes Rennes Natation')

st.sidebar.header("Sélectionner un genre")
selected_gender = st.sidebar.selectbox("Choisissez le genre", ["Homme", "Femme"])

# Format the date as YYYYMMDD
if selected_gender=="Homme":
    file_gender = "M"
else :
    file_gender = "F"

file_name = f"equipe_{file_gender}_novembre.csv"  
file_path = os.path.join(DATA_FOLDER, file_name)
print(file_path)

# Load the file based on the selected date
if os.path.exists(file_path):
    # Display the filename
    st.write(f"### File loaded: {file_name}")

    # Load the file
    df = pd.read_csv(file_path)

    # Show the dataframe in the app
    st.dataframe(df)

    # Optionally, you can apply your previous heatmap, logos, etc.
    # Apply heatmap or logos if needed
else:
    st.write(f"File {file_path} does not exist.")