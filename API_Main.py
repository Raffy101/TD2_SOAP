import requests
from fastapi import Request, File, UploadFile, Response
from fastapi.responses import RedirectResponse
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

# Liste des URL des Différents API
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
global token

@router.post("/upload_file")
@app.post('/upload_file')
def upload_file(response: Response, request: Request, message : str = '', file: UploadFile = File(...)):
    cookie = request.cookies
    print("cookie Upload=", cookie)
    if "access_token" in cookie:
        token = cookie["access_token"]
    else:
        token = ''

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            response = RedirectResponse(url="/")
            response.headers["Location"] = "/?message=Error INVALID Token !"
            return response
            #raise credentials_exception
    except JWTError:
        response = RedirectResponse(url="/")
        response.headers["Location"] = "/?message=Error INVALID Token !"
        return response 
        #raise credentials_exception

    if message != '':
        response = RedirectResponse(url="/")
        response.headers["Location"] = "/?message="+message
        return response
    
    if file is None:
        response = RedirectResponse(url="/")
        response.headers["Location"] = "/?message=Aucun fichier sélectionné."
        return response
    
    # Vérifie si le nom du fichier est vide
    if file.filename == '':
        response = RedirectResponse(url="/")
        response.headers["Location"] = "/?message=Nom de fichier vide."
        return response

    if file and is_allowed_file(file.filename):
        
        
        contenuFile = file.file.read()
        contenuFileSTR = contenuFile.decode("utf-8")
        if cookie["name"] in contenuFileSTR:
            data = {
            'demande_client' : str(contenuFileSTR)
            }
            print(data)
            print("tokenonModified=", token)
            if token == None or token == 'None':
                print("token vide!")
                return
            try:
                headers['Authorization'] = f"Bearer {token}"
                donneeClient = requests.post(api_Extraction_url, params=data, headers=headers).json()
                print("requete : ",donneeClient)
                
                if (donneeClient["NomDuClient"] == "" or donneeClient["DescriptionPropriete"] == "" or donneeClient["RevenuMensuel"] == "" or donneeClient["DepensesMensuelles"] == "") :
                    print("Erreur durant l'execution de la procedure des informations sont manquantes !")
                    print("Veuillez vous assurer de renseigner dans la demande :\n NomduClient, la description de la propriete, les revenus Mensuels et les depenses mensuelles\n")
                    response = RedirectResponse(url="/")
                    
                    manqueInfos = "Erreur durant l'execution de la procedure des informations sont manquantes !\n Veuillez vous assurer de renseigner dans la demande : NomduClient, la description de la propriete, les revenus Mensuels et les depenses mensuelles"
                    urlencodemsg= urllib.parse.quote_plus(manqueInfos)
                    
                    response.headers["Location"] = f"/?message={urlencodemsg}"
                    return response 
            except:
                print("Error INVALID Token !")
                response = RedirectResponse(url="/")
                response.headers["Location"] = "/?message=Error INVALID Token !"
                return response 
                    
            try:
                recherche_client_db = str(donneeClient["NomDuClient"])
            except:
                recherche_client_db = "None"
                print("Entrez un nom valide")
                response = RedirectResponse(url="/")
                response.headers["Location"] = "/?message=Entrez un nom valide"
                return response 
            
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
                stat_client = session.query(StatistiquesClient).filter(StatistiquesClient.id_Client == client_trouve.id).first()

                # API évaluation de la propriété
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
                try:
                    score = requests.post(api_CalculScore_url, params={'totalCredit' : stat_client.total_credit,'nbPayementRetard' : stat_client.nb_retards, 'nbBankRuptcy' : stat_client.nb_faillites}, headers=headers).json()
                except: 
                    print("Erreur lors de la saisie du token pour l'API Score")
                    return          
                print(score)

                # API de vérification de la solvabilité du client
                try:
                    Solvabilite = requests.post(api_VerifSolva_url, params={'salaireMensuel' : str(donneeClient["RevenuMensuel"]) , 'depenseMensuel' : str(donneeClient["DepensesMensuelles"]), 'dureeDuPret' : str(donneeClient["DureeDuPret"]) , 'calcul_score' : score }, headers=headers).json()
                except:
                    print("Erreur lors de la saisie du token pour l'API Solvabilité")
                    return
                print("SOLVABILITE :"+str(Solvabilite))

                # API de décision d'approbation ou non d'un prêt pour le client
                try:
                    Decision =  requests.post(api_DecisionApprob_url, params={'solvabilite' : Solvabilite }, headers=headers).json()
                except:
                    print("Erreur lors de la saisie du token pour l'API Decision")
                    return
                
                # Print du résutat
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
                        msg = "La demande de pret est acceptee !! Felicitation"
                    elif str(Decision) == "REFUS" :
                        msg = "Nous sommes dans le regret de vous informer que votre demande est rejetee !"
                    else:
                        msg = "Erreur au cours de l'execution de la demande de credit !"
                    fichiers.write(msg)
            
            else:
                print("Aucun client trouvé dans la base de donnée avec ce nom.")

            # Enregistremnt du fichier s'il a l'extension autorisée
            with open(directory+file.filename, "wb") as file_object:
                file_object.write(contenuFile)
            print("File Uploaded !")
            message="Fichier '{}' telecharge avec succes.".format(file.filename)
            
            response = RedirectResponse(url="/")
            response.headers["Location"] = "/?message="+message
            response.headers["access_token"] = token
            response.headers["token_type"] = "bearer"
            response.headers["message"] = "message"
            return response 
        else:
            response = RedirectResponse(url="/")
            response.headers["Location"] = "/?message=Le nom saisie dans le fichier est incorrect"
            return response
    else:
        response = RedirectResponse(url="/")
        response.headers["Location"] = "/?message=Extension de fichier non autorisee. Les fichiers .txt sont autorises."
        return response

app.include_router(router)
