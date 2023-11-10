from flask import Flask, request, render_template, redirect, url_for
import os
import spacy

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : Notre Fonction Index nous sert à pouvoir réaliser notre
    demande de prêt via une interface Web.

###########################################################################
'''

#codage=utf-8
app = Flask(__name__)

directory = "./DemandesClients/"

def is_allowed_file(filename): 
  return filename.lower().endswith(".txt")

    
@app.route('/decision', methods=['GET', 'POST'])
def decision():
    if request.method == 'POST':
        nom = request.form['nom']

        directory_results="./Resultats/"
        fichier_resultat = os.path.join(directory_results+nom+".txt")
        if os.path.exists(fichier_resultat):
            with open(directory_results+ nom+".txt", 'r') as fichier:
                contenu = fichier.read()
            return render_template('decisionPage.html', nom = nom, message=contenu)
        else:
            return render_template('decisionPage.html', nom = nom, message="Aucun fichier trouvé.")


    return render_template('decisionPage.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = request.args.get('message', None)
    if message is not None:
        redirect(url_for('upload_file'))
        return render_template('index.html', message=message)
        
        
    if request.method == 'POST':
        if 'fichier' not in request.files:
            return render_template('index.html', message="Aucun fichier sélectionné.")
        
        fichier = request.files['fichier']
        print("tetset")
        # Vérifie si le nom du fichier est vide
        if fichier.filename == '':
            return render_template('index.html', message="Nom de fichier vide.")

        if fichier and is_allowed_file(fichier.filename):
            # Enregistrez le fichier s'il a l'extension autorisée
            fichier.save(directory+fichier.filename)
            return render_template('index.html', message="Fichier '{}' téléchargé avec succès.".format(fichier.filename))
        else:
            return render_template('index.html', message="Extension de fichier non autorisée. Les fichiers .txt sont autorisés.")
    
    return render_template('index.html')
    

@app.route('/cree_fichier', methods=['GET', 'POST'])
def creer_fichier():
    if request.method == 'POST':
        texte = request.form.get('texte', '')
        #message = request.args.get('La demande a été envoyé avec succès.', None)# post
        
        if texte:
            nlp = spacy.load("fr_core_news_sm")
            doc = nlp(texte)
            nom=None
            for entite in doc.ents:
                if entite.label_ == "PERSON" or entite.label_ == "PER":
                    nom = entite.text

            if nom:
                nomFichier = directory+'demande_de_'+nom+'.txt'
            else:
                return redirect(url_for('upload_file',message="Erreur durant l'exécution de la procédure, des informations sont manquantes ! \n Veuillez vous assurer de renseigner dans la demande : \n NomduClient, la description de la propriété, les revenus Mensuels et les depenses mensuelles"))

            with open(nomFichier, 'w') as fichier:
                fichier.write(texte)
                
            return redirect(url_for('upload_file',message="La demande a été envoyé avec succès."))
    
        return redirect(url_for('upload_file',message="Aucun client trouvé avec ce nom."))
            
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
