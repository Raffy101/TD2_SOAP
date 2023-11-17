import os
import spacy
from API_Main import router as routerMain
from APIs.API_Extraction import router as routerExtraction
from APIs.API_VerifSolvabilité import router as routerVerifSolvabilité
from APIs.API_EvaluationPropriété import router as routerEvaluationPropriété
from APIs.API_CalculScore import router as routerCalculScore
from APIs.API_DecisionApprobation import router as routerDecisionApprobation
from utils import router as routerGetCurrentUserActive
from fastapi import Depends,FastAPI, APIRouter, HTTPException, status, File, UploadFile, Request, Header
import uvicorn
from multiprocessing import Process
from API_Main import Handler
import time
from watchdog.observers import Observer
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from utils import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : Notre Fonction Index nous sert à pouvoir réaliser notre
    demande de prêt via une interface Web.

###########################################################################
'''
"""class User(BaseModel):
    name : str
    username: str
    password : str
    email: str 
    disabled: bool | None = None"""

#codage=utf-8
app = FastAPI()

router = APIRouter()
app.include_router(routerMain)
app.include_router(routerExtraction)
app.include_router(routerVerifSolvabilité)
app.include_router(routerEvaluationPropriété)
app.include_router(routerCalculScore)
app.include_router(routerDecisionApprobation)
app.include_router(routerGetCurrentUserActive)

directory = "./DemandesClients/"

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
current_user = None
def is_allowed_file(filename): 
  return filename.lower().endswith(".txt")

"""@router.get("/items")
@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@router.get("/users/me")
@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
"""

@router.post("/token")
@app.post("/token")
async def login(request: Request,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Interroger la base de données
    print("form_data.username=", form_data.username)
    print("form_data.password=", form_data.password)
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    global current_user
    current_user = access_token
    return templates.TemplateResponse("index.html", {"request": request,"access_token": access_token , "token_type": "bearer"})


@router.get("/decision")
@app.get('/decision')
def decision(request: Request, nom: str = None):
    directory_results="./Resultats/"
    fichier_resultat = os.path.join(directory_results+nom+".txt")
    if os.path.exists(fichier_resultat):
        with open(directory_results+ nom+".txt", 'r') as fichier:
            contenu = fichier.read()
        return templates.TemplateResponse("decisionPage.html", {"request": request,"nom": nom, "message": contenu})
    else:
        return templates.TemplateResponse("decisionPage.html", {"request": request,"nom": nom, "message": "Aucun fichier trouvé."})


@router.get("/")
@app.get('/', response_class=HTMLResponse)
def accueil(request: Request, message=None):
    return templates.TemplateResponse("index.html" ,{"request": request})

@router.post("/upload_file")
@app.post('/upload_file')
def upload_file(request: Request, message : str = None, file: UploadFile = File(...)):
    if message is not None:
        return templates.TemplateResponse("index.html", {"request": request,"message": message})
        
    if file is None:
        return templates.TemplateResponse("index.html", {"request": request,"message": "Aucun fichier sélectionné."})
    
    print("tetset")
    # Vérifie si le nom du fichier est vide
    if file.filename == '':
        return templates.TemplateResponse("index.html", {"request": request,"message": "Nom de fichier vide."})

    if file and is_allowed_file(file.filename):
        # Enregistrez le fichier s'il a l'extension autorisée
        with open(directory+file.filename, "wb") as file_object:
            file_object.write(file.file.read())
        global current_user
        message="Fichier '{}' téléchargé avec succès.".format(file.filename)
        response = RedirectResponse("/mainAPI")
        response.set_cookie(key="access_token", value=current_user, httponly=True)
        return response
    else:
        return templates.TemplateResponse("index.html", {"request": request,"message": "Extension de fichier non autorisée. Les fichiers .txt sont autorisés."})
    
    
@router.post("/cree_fichier")
@app.post('/cree_fichier')
def creer_fichier(request: Request, texte: str = None):
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
            message="Erreur durant l'exécution de la procédure, des informations sont manquantes ! \n Veuillez vous assurer de renseigner dans la demande : \n NomduClient, la description de la propriété, les revenus Mensuels et les depenses mensuelles"
            return RedirectResponse(url="/?message={message}")

        with open(nomFichier, 'w') as fichier:
            fichier.write(texte)
        message="La demande a été envoyé avec succès."    
        return RedirectResponse(url="/?message={message}")
    
    message="Aucun client trouvé avec ce nom."
    return RedirectResponse(url="/?message={message}")

app.include_router(router)

def run_fastapi():
    uvicorn.run(app, host="localhost", port=8000)

def surveillance():
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

if __name__ == '__main__':
    process_fastapi = Process(target=run_fastapi)
    process_surveillance = Process(target=surveillance)

    process_fastapi.start()
    process_surveillance.start()

    process_fastapi.join()
    process_surveillance.join()
    session.close()
    #uvicorn.run(appAPI, host="localhost", port=8000)
    #app.run(debug=True)
    