from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

import sys
import os


# Insérer le chemin de 'scripts' dans le path
scripts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
sys.path.insert(0, scripts_path)

# Vérifie que Python a bien ajouté le bon chemin
print(f"Chemin vers scripts ajouté au PATH: {scripts_path}")

# Importation de la fonction principale de l'algorithme
import MILP.main as main  # Attention à l'orthographe

app = Flask(__name__)

# Dossier de téléchargement des CSV
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), '..', 'csv'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Vérifier si les fichiers ont été uploadés
    if 'participation_csv' not in request.files or 'annuaire_csv' not in request.files:
        return redirect(request.url)

    participation_file = request.files['participation_csv']
    annuaire_file = request.files['annuaire_csv']

    # Enregistrer les fichiers CSV dans le dossier 'csv'
    if participation_file.filename != '' and annuaire_file.filename != '':
        participation_path = os.path.join(app.config['UPLOAD_FOLDER'], participation_file.filename)
        print(participation_path)
        annuaire_path = os.path.join(app.config['UPLOAD_FOLDER'], annuaire_file.filename)
        print(annuaire_path)
        participation_file.save(participation_path)
        annuaire_file.save(annuaire_path)

        print(os.path.dirname(participation_path))

        # Appel de l'algorithme avec les chemins des fichiers CSV
               # Appel de l'algorithme
        results_F = main.execute_algorithm(str(os.path.dirname(participation_path)),'F')
        results_M = main.execute_algorithm(str(os.path.dirname(participation_path)),'M')

        # Vérifiez si les fichiers CSV sont générés
        femmes_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], "equipe_F_novembre.csv")
        hommes_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], "equipe_M_novembre.csv")
        
        print(f"Fichiers résultats : {femmes_csv_path}, {hommes_csv_path}")
        
        if os.path.exists(femmes_csv_path) and os.path.exists(hommes_csv_path):
            return redirect(url_for('results'))  # Redirection vers la route 'results'
        else:
            print("Les fichiers résultats n'ont pas été créés.")
            return "Erreur : les fichiers résultats n'ont pas été générés.", 500

    return redirect(url_for('index'))


@app.route('/results')
def results():
    # Lire les données CSV
    femmes_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], "equipe_F_novembre.csv")
    hommes_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], "equipe_M_novembre.csv")

    print(f"Lecture des fichiers : {femmes_csv_path}, {hommes_csv_path}")

    try:
        femmes_df = pd.read_csv(femmes_csv_path,sep=";")
        hommes_df = pd.read_csv(hommes_csv_path,sep=";")
        print(femmes_df.head())  # Imprimez les premières lignes
        print(hommes_df.head())  # Imprimez les premières lignes
    except FileNotFoundError as e:
        print(f"Erreur de fichier: {e}")
        return "Fichier introuvable", 404
    except Exception as e:
        print(f"Erreur lors de la lecture des fichiers : {e}")
        return "Erreur lors de la lecture des fichiers.", 500

    # Convertir les DataFrames en HTML
    femmes_html = femmes_df.to_html(index=False, classes='table table-striped')
    hommes_html = hommes_df.to_html(index=False, classes='table table-striped')

    return render_template('results.html', femmes=femmes_html, hommes=hommes_html)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    hommes_path = os.path.join(app.config['UPLOAD_FOLDER'], "meilleures_performances_hommes.csv")
    femmes_path = os.path.join(app.config['UPLOAD_FOLDER'], "meilleures_performances_femmes.csv")

    if request.method == 'POST':
        # Si le formulaire est soumis, récupérer les données du formulaire
        # Vous pouvez adapter cela selon vos besoins pour gérer les modifications
        hommes_data = request.form.get('hommes_data')
        femmes_data = request.form.get('femmes_data')

        # Sauvegarder les données modifiées dans les fichiers CSV
        with open(hommes_path, 'w') as f:
            f.write(hommes_data)

        with open(femmes_path, 'w') as f:
            f.write(femmes_data)

        return redirect(url_for('index'))  # Rediriger vers la page principale après la sauvegarde

    # Lire les données des fichiers CSV
    femmes_df = pd.read_csv(femmes_path, encoding='ISO-8859-1')
    hommes_df = pd.read_csv(hommes_path, encoding='ISO-8859-1')

    # Convertir les DataFrames en chaînes de caractères pour les afficher dans un formulaire
    hommes_data = hommes_df.to_csv(index=False, sep=';')
    femmes_data = femmes_df.to_csv(index=False, sep=';')

    return render_template('edit.html', hommes_data=hommes_data, femmes_data=femmes_data)


if __name__ == '__main__':
    app.run(debug=True)