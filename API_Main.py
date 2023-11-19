
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import requests
from fastapi import Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from utils import *
from fastapi.staticfiles import StaticFiles
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
api_EvalPropriete_url = "http://localhost:8000/evaluation_propriete"
api_CalculScore_url = "http://localhost:8000/calcul_score"
api_VerifSolva_url = "http://localhost:8000/verification_solvabilite"
api_DecisionApprob_url = "http://localhost:8000/decision_credit"

headers = {
    'Content-Type': 'application/json',
}
app = FastAPI()
router = APIRouter()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
directory = "./DemandesClients/"
token= None

@router.post("/upload_file")
@app.post('/upload_file')
def upload_file(request: Request, message : str = None, file: UploadFile = File(...)):
    if message is not None:
        return templates.TemplateResponse("index.html", {"request": request,"message": message})
        
    if file is None:
        return templates.TemplateResponse("index.html", {"request": request,"message": "Aucun fichier sélectionné."})
    
    # Vérifie si le nom du fichier est vide
    if file.filename == '':
        return templates.TemplateResponse("index.html", {"request": request,"message": "Nom de fichier vide."})

    if file and is_allowed_file(file.filename):
        cookie = request.cookies
        print("cookie Upload=", cookie)
        global token
        token = cookie["access_token"]
        
        # Enregistrez le fichier s'il a l'extension autorisée
        with open(directory+file.filename, "wb") as file_object:
            file_object.write(file.file.read())
        print("File Uploaded !")
        message="Fichier '{}' téléchargé avec succès.".format(file.filename)
        #response = RedirectResponse("/mainAPI")
        #response.set_cookie(key="access_token", value=current_user, httponly=True)
        #response.set_cookie(key="file", value=file.file.read(), httponly=True)
        #return response
        
        return templates.TemplateResponse("index.html", {"request": request,"access_token": token ,"message":"File Uploaded !", "token_type": "bearer"})

    else:
        return templates.TemplateResponse("index.html", {"request": request,"message": "Extension de fichier non autorisée. Les fichiers .txt sont autorisés."})
  


class Handler(FileSystemEventHandler):
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        data = {
            'demande_client' : str(event.src_path)
        }
        print(event.src_path)
        print("tokenonModified=", token)
        if token == None or token == 'None':
            print("token vide!")
            return
        try:
            headers['Authorization'] = f"Bearer {token}"
            donneeClient = requests.post(api_Extraction_url, params=data, headers=headers).json()
            print("requete : ",donneeClient)
            #print(donneeClient["RevenuMensuel"])
            
            if (donneeClient["NomDuClient"] == "" or donneeClient["DescriptionPropriete"] == "" or donneeClient["RevenuMensuel"] == "" or donneeClient["DepensesMensuelles"] == "") :
                print("Erreur durant l'exécution de la procédure des informations sont manquantes !")
                print("Veuillez vous assurer de renseigner dans la demande :\n NomduClient, la description de la propriété, les revenus Mensuels et les depenses mensuelles\n")
                return
        except:
            print("Error INVALID Token Extraction !")
            return 
                
        try:
            recherche_client_db = str(donneeClient["NomDuClient"])
        except:
            recherche_client_db = "None"
            print("Entrez un nom valide")
            return
        
        client_trouve = session.query(User).filter(User.name == recherche_client_db).first()

        all_clients = session.query(User).all()

        # Vérifier si des clients existent dans la base de données
        if len(all_clients) > 0:
            print("Liste des clients dans la base de données:")
            for client in all_clients:
                print(client.name, ", ", client.username)
        else:
            print("Aucun client trouvé dans la base de données.")
        

        print(client_trouve)
        if client_trouve:

            print(f"Client trouvé (Voici les Infos Associés): ID : {client_trouve.id}, Nom : {client_trouve.name}, username : {client_trouve.username} ,email : {client_trouve.email}, password : {client_trouve.password}")
            # Phase d'initialisation

            # API de d'évaluation de la propriété
            #headers['Authorization'] = f"Bearer {token_secret_EvalProp}"

            stat_client = session.query(StatistiquesClient).filter(StatistiquesClient.id_Client == client_trouve.id).first()

            if stat_client is None:
                print("Erreur aucune données statistiques sur le client trouvé")
                return 
            try:
                eval_propr = requests.post(api_EvalPropriete_url, params={'description' : str(donneeClient["DescriptionPropriete"])}, headers=headers).json()
            
            except:
                print("Erreur lors de la saisie du token pour l'API Eval Prop")
                return
            print(eval_propr)

            # API de calcul du score d'un client
            #headers['Authorization'] = f"Bearer {token_secret_CalculScore}"
            try:
                score = requests.post(api_CalculScore_url, params={'totalCredit' : stat_client.total_credit,'nbPayementRetard' : stat_client.nb_retards, 'nbBankRuptcy' : stat_client.nb_faillites}, headers=headers).json()
            except: 
                print("Erreur lors de la saisie du token pour l'API Score")
                return          
            print(score)

            # API de vérification de la solvabilité du client
            #headers['Authorization'] = f"Bearer {token_secret_VerifSolva}"
            try:
                Solvabilite = requests.post(api_VerifSolva_url, params={'salaireMensuel' : str(donneeClient["RevenuMensuel"]) , 'depenseMensuel' : str(donneeClient["DepensesMensuelles"]), 'dureeDuPret' : str(donneeClient["DureeDuPret"]) , 'calcul_score' : score }, headers=headers).json()
            except:
                print("Erreur lors de la saisie du token pour l'API Solvabilité")
                return
            print("SOLVABILITE :"+str(Solvabilite))

            # API de décision d'approbation ou non d'un prêt pour le client
            #headers['Authorization'] = f"Bearer {token_secret_DecisionApprob}"
            try:
                Decision =  requests.post(api_DecisionApprob_url, params={'solvabilite' : Solvabilite }, headers=headers).json()
            except:
                print("Erreur lors de la saisie du token pour l'API Decision")
                return
            
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
        

app.include_router(router)
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