
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import sqlite3

import requests

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : Il  s'agit ici de notre programme Main qui nous sert à faire
    appel à toutes nos APIs et à donc executer tout le système qui nous
    sert à attribuer ou non à un client une demande de prêt

###########################################################################
'''

# Liste de URL des Différents API

api_Extraction_url = "http://localhost:8000/creationDonneeClients"
api_EvalPropriete_url = "http://localhost:8001/evaluation_propriete"
api_CalculScore_url = "http://localhost:8002/calcul_score"
api_VerifSolva_url = "http://localhost:8003/verification_solvabilite"
api_DecisionApprob_url = "http://localhost:8004/decision_credit"

# Liste des différents tokens 

token_secret_Extraction = "AHshhxhczcrfkrvfkfnvrepdazdede"
token_secret_EvalProp = "dfeferjclefekzffS22EDkfazc"
token_secret_CalculScore = "AHshhxhwxsaSA23Evrfrve"
token_secret_VerifSolva = "AHqsddazcvfervbrXZ3repdazdede"
token_secret_DecisionApprob = "cqsdzdaSvrepdazdede"

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {token_secret_Extraction}"
}

class Handler(FileSystemEventHandler):
    def on_modified(self, event):

        # Créer une connexion à la base de données
        conn = sqlite3.connect('./DataBase/BaseDeDonneesClients.db')
        # Créer un curseur pour exécuter des requêtes
        cur = conn.cursor()
                
        if event.is_directory:
            return
        
        data = {
            'demande_client' : str(event.src_path)
        }
       
        print(event.src_path)

        try:
            headers['Authorization'] = f"Bearer {token_secret_Extraction}"
            donneeClient = requests.post(api_Extraction_url, params=data, headers=headers).json()
            #print(donneeClient["RevenuMensuel"])

            if (donneeClient["NomDuClient"] == "" or donneeClient["DescriptionPropriete"] == "" or donneeClient["RevenuMensuel"] == "" or donneeClient["DepensesMensuelles"] == "") :
                print("Erreur durant l'exécution de la procédure des informations sont manquantes !")
                print("Veuillez vous assurer de renseigner dans la demande :\n NomduClient, la description de la propriété, les revenus Mensuels et les depenses mensuelles\n")
                return
        except:
            print("Erreur INVALIDE Token !")
            return 
                
        try:
            recherche_client_db = str(donneeClient["NomDuClient"])
        except:
            recherche_client_db = "None"
            print("Entrez un nom valide")
            return

        cur.execute("SELECT * FROM clients WHERE nom=?", (recherche_client_db,))
        client_trouve = cur.fetchone()

        cur.execute("SELECT * FROM clients")
        all_clients = cur.fetchall()

        # Vérifier si des clients existent dans la base de données
        if len(all_clients) > 0:
            print("Liste des clients dans la base de données:")
            for client in all_clients:
                print(client)
        else:
            print("Aucun client trouvé dans la base de données.")
        

        print(client_trouve)
        if client_trouve:

            print(f"Client trouvé (Voici les Infos Associés): ID : {client_trouve[0]}, Nom : {client_trouve[1]}, TotalCrédit : {client_trouve[2]} ,Nb Faillites : {client_trouve[3]}, Nb Retards : {client_trouve[4]}")
            # Phase d'initialisation

            # API de d'évaluation de la propriété
            headers['Authorization'] = f"Bearer {token_secret_EvalProp}"
            
            eval_propr = requests.post(api_EvalPropriete_url, params={'description' : str(donneeClient["DescriptionPropriete"])}, headers=headers).json()
            if type(eval_propr) != int : 
                print("Erreur lors de la saisie du token pour l'API Eval Prop")
                return
            print(eval_propr)

            # API de calcul du score d'un client
            headers['Authorization'] = f"Bearer {token_secret_CalculScore}"
            score = requests.post(api_CalculScore_url, params={'totalCredit' : int(client_trouve[2]),'nbPayementRetard' : int(client_trouve[4]), 'nbBankRuptcy' : int(client_trouve[3])}, headers=headers).json()
            if type(score) != int : 
                print("Erreur lors de la saisie du token pour l'API Score")
                return          
            print(score)

            # API de vérification de la solvabilité du client
            headers['Authorization'] = f"Bearer {token_secret_VerifSolva}"
            Solvabilite = requests.post(api_VerifSolva_url, params={'salaireMensuel' : str(donneeClient["RevenuMensuel"]) , 'depenseMensuel' : str(donneeClient["DepensesMensuelles"]) , 'calcul_score' : score }, headers=headers).json()
            if type(Solvabilite) != int : 
                print("Erreur lors de la saisie du token pour l'API Solvabilité")
                return
            print("SOLVABILITE :"+str(Solvabilite))

            # API de décision d'approbation ou non d'un prêt pour le client
            headers['Authorization'] = f"Bearer {token_secret_DecisionApprob}"
            Decision =  requests.post(api_DecisionApprob_url, params={'solvabilite' : Solvabilite }, headers=headers).json()
            if Decision == "ACCEPTE" or Decision == "REFUS" : 
                print(str(Decision))
            else :
                print("Erreur lors de la saisie du token pour l'API Decision")
                return

            # API du résultat de la décision après analyse du dossier du client
            print(str(donneeClient["NomDuClient"]))
            nom_fichier = "./Resultats/" + str(donneeClient["NomDuClient"]) + ".txt"
            
            with open(nom_fichier, 'w') as fichiers :
            
                if str(Decision) == "ACCEPTE" :
                    msg = "La demande de prêt est acceptee !! Félicitation"
                elif str(Decision) == "REFUS" :
                    msg = "Nous sommes dans le regrêt de vous informer que votre demande est rejetee !"
                else:
                    msg = "Erreur au cours de l'execution de la demande de crédit !"
                fichiers.write(msg)
        
        else:
            print("Aucun client trouvé dans la base de donnée avec ce nom.")
        
        cur.close()
        conn.close()

if __name__ == '__main__':

    chemin_dossier = ".\DemandesClients"

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path=chemin_dossier, recursive=False)

    print(f"Surveillance du dossier : {chemin_dossier}")
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()