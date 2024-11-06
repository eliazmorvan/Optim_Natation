import pandas as pd

def read_csv_file(input_file, encoding='ISO-8859-1', sep=";"):
    """Lit un fichier CSV et retourne un DataFrame."""
    return pd.read_csv(input_file, encoding=encoding, sep=sep)

def create_output_dataframe():
    """Crée et retourne un DataFrame vide avec les colonnes de sortie."""
    output_columns = ['NomPrenom', 'Age', 'Sexe', 
                      '100pap', '200pap', '100Dos', '200Dos', '100Br', '200Br', 
                      '100NL', '400NL', '1004N', '2004N', "50NL", "200NL"]
    return pd.DataFrame(columns=output_columns)

def clean_event_names(df):
    """Nettoie les épreuves dans le DataFrame (élimine les espaces et met en minuscule)."""
    df['EPREUVE'] = df['EPREUVE'].str.strip().str.lower()
    return df

def update_output_dataframe(output_df, row, sexe):
    """Met à jour le DataFrame de sortie avec les informations d'un nageur pour une épreuve donnée."""
    nom_prenom = row['Nageur']
    age = row['Age']
    
    # Vérifier si le nageur est déjà présent dans le DataFrame de sortie
    if nom_prenom not in output_df['NomPrenom'].values:
        # Ajouter une nouvelle ligne pour le nageur s'il n'existe pas
        new_row = pd.DataFrame([[nom_prenom, age, sexe] + [None] * (len(output_df.columns) - 3)], 
                               columns=output_df.columns)
        output_df = pd.concat([output_df, new_row], ignore_index=True)

    # Mettre à jour la bonne colonne selon l'épreuve
    event = row['EPREUVE']
    points = row['Points_ajustes']
    
    if '100 pap' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '100pap'] = points
    elif '200 pap' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '200pap'] = points
    elif '100 dos' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '100Dos'] = points
    elif '200 dos' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '200Dos'] = points
    elif '100 br' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '100Br'] = points
    elif '200 br' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '200Br'] = points
    elif '100 nage' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '100NL'] = points
    elif '400 nage' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '400NL'] = points
    elif '100 4 n' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '1004N'] = points
    elif '200 4 n' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '2004N'] = points
    elif '50 nage' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '50NL'] = points
    elif '200 nage' in event:
        output_df.loc[output_df['NomPrenom'] == nom_prenom, '200NL'] = points
    
    return output_df

def merge_participation_data(output_df, participation_file):
    """Fusionne les données de participation et filtre les nageurs non participants."""
    participation_df = pd.read_csv(participation_file, sep=";", encoding='ISO-8859-1')
    merged_df = pd.merge(output_df, participation_df, left_on="NomPrenom", right_on="Nom ", how="inner")
    filtered_df = merged_df[merged_df['Participation'] == 0]
    filtered_df.drop(columns=["Nom ", "Report  Participation", "Participation"], inplace=True)
    return filtered_df

def save_csv_file(df, output_file, sep=';'):
    """Sauvegarde un DataFrame dans un fichier CSV."""
    df.to_csv(output_file, sep=sep, index=False)

def process_file(input_file, participation_file, output_file, sexe):
    """Processus complet pour un fichier d'entrée donné et un sexe spécifique."""
    # Lecture du fichier CSV d'origine
    df = read_csv_file(input_file)
    
    # Nettoyage des noms d'épreuves
    df = clean_event_names(df)
    
    # Création du DataFrame de sortie
    output_df = create_output_dataframe()

    # Remplir le DataFrame de sortie avec les performances
    for _, row in df.iterrows():
        output_df = update_output_dataframe(output_df, row, sexe)

    # Remplacer les valeurs manquantes par '#N/A'
    output_df.fillna('#N/A', inplace=True)

    # Fusionner avec les données de participation
    output_df = merge_participation_data(output_df, participation_file)
    
    # Sauvegarde du DataFrame de sortie dans un fichier CSV
    save_csv_file(output_df, output_file)

def main():
    # Liste des fichiers d'entrée, de sortie et les sexes associés
    files = [
        {'input': './csv/meilleures_performances_femmes.csv', 'output': './csv/femmes_points_novembre.csv', 'sexe': 'F'},
        {'input': './csv/meilleures_performances_hommes.csv', 'output': './csv/hommes_points_novembre.csv', 'sexe': 'M'}
    ]
    participation_file = './csv/participation_novembre.csv'
    
    # Traitement de chaque fichier
    for file_info in files:
        process_file(file_info['input'], participation_file, file_info['output'], file_info['sexe'])

if __name__ == '__main__':
    main()