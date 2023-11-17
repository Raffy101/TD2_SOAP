#pip install twisted
#pip install spyne 

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import os
import spacy
import re
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API d'extraction d'information nous permet de pouvoir
    analyser une demande textuel ( via un fichier ".txt") et d'en extirper
    les informations importantes et nécessaires.

###########################################################################
'''

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

idClient= 1

token_Extraction = "AHshhxhczcrfkrvfkfnvrepdazdede"


@router.post("/creationDonneeClients")
@app.post('/creationDonneeClients')
async def CreationDonneeClients(demande_client : str, current_user: Annotated[User, Depends(get_current_user)]):
    
    print("current_user=", current_user)
    if not current_user :
        print("INVALID TOKEN !")
        return

    """if credentials.credentials != token_Extraction:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else :
        print("Success authentication token")"""
    

    print(f"Requête reçue avec demande_client : {demande_client}")
    if os.path.isfile(demande_client) and demande_client.endswith('.txt'):
        print("Fichier client trouvé :", demande_client)

        donneesClient = {}

        # Phase d'initialisation des données obligatoires --> Utiliser par la suite
        donneesClient["NomDuClient"] = "" 
        donneesClient["DescriptionPropriete"] = "" 
        donneesClient["RevenuMensuel"] = "" 
        donneesClient["DepensesMensuelles"] = ""

        nlp = spacy.load("fr_core_news_sm")

        with open(demande_client, "r") as file:
            file_content = file.read()
            print(f"File Content:\n{file_content}")

        doc = nlp(file_content)
        #print(doc)

        # Parcourez les tokens du document SpaCy
        telephone_pattern = r'(\+\d{1,3}[\s-]?\d{9,})|(\d{10,})'
        for match in re.finditer(telephone_pattern, file_content):
            numero_telephone = match.group()
            donneesClient['NumeroDeTelephone'] = numero_telephone

        
        for entite in doc.ents:
            if entite.label_ == "PERSON" or entite.label_ == "PER":
                donneesClient['NomDuClient'] = entite.text
            elif entite.label_ == "LOCATION" or entite.label_ == "LOC":
                donneesClient['Adresse'] = entite.text
        
        #init sinon erreur
        donneesClient['DescriptionPropriete'] = ""

        for token in doc:
            if (("prêt" in token.text or "pret" in token.text) and token.nbor(1).text == "de" and token.nbor(2).like_num) or ("emprunter" in token.text and token.nbor(1).like_num):
                donneesClient['MontantDuPretDemande'] = token.nbor(2).text
            elif "ans" in token.text and token.nbor(-1).like_num:
                donneesClient['DureeDuPret'] = token.nbor(-1).text
            elif token.like_email:
                donneesClient['Email'] = token.text

            elif ("gagne" in token.text and token.nbor(1).like_num and "par" in token.nbor(3).text and "mois" in token.nbor(4).text):
                donneesClient['RevenuMensuel'] = token.nbor(1).text
            elif ("salaire" in token.text and "est" in token.nbor(1).text and "de" in token.nbor(2).text and token.nbor(3).like_num) :
                donneesClient['RevenuMensuel'] = token.nbor(3).text

            if ("dépense" in token.text or "dépenses" in token.text or "depense" in token.text or "depenses" in token.text) and "environ" in token.nbor(1).text and token.nbor(2).like_num:
                donneesClient['DepensesMensuelles'] = token.nbor(2).text
            elif token.text.lower() in ["rue", "avenue", "boulevard", "place", "impasse", "quai"]:
                if token.nbor(-1).like_num:
                    adresse = f"{token.nbor(-1)} {token.text}"
                    # Recherchez les tokens suivants jusqu'à ce que vous atteigniez une ponctuation
                    i = token.i + 1
                    while i < len(doc) and not doc[i].is_punct:
                        adresse += " " + doc[i].text
                        i += 1
                    donneesClient['Adresse'] = adresse

            elif "jardin" in token.text:
                donneesClient['DescriptionPropriete'] += token.text+ ", "

            elif "pieces" in token.text or "pieces" in token.text or "pièces" in token.text or "pièce" in token.text:
                donneesClient['DescriptionPropriete'] += token.nbor(-1).text +" "+ token.text + ", "
                
            elif "etages" in token.text or "etage" in token.text or "etages" in token.text or "étage" in token.text:
                donneesClient['DescriptionPropriete'] += token.nbor(-1).text +" "+ token.text + ", "

            elif "piscine" in token.text:
                donneesClient['DescriptionPropriete'] += token.text + ", "

            elif "m²" in token.text:
                donneesClient['DescriptionPropriete'] += token.nbor(-1).text + token.text + ", "

            elif ("chambre" in token.text or "chambres" in token.text) and token.nbor(-1).like_num:
                donneesClient['DescriptionPropriete'] += token.nbor(-1).text+ " " +token.text + ", "

            elif ("bains" in token.text or "bain" in token.text) and token.nbor(-1).text in "de" and (token.nbor(-2).text in "salles" or token.nbor(-2).text in "salle") and token.nbor(-3).like_num:
                donneesClient['DescriptionPropriete'] += token.nbor(-3).text + " " + token.nbor(-2).text + " " + token.nbor(-1).text + " " +  token.text + ", "

            elif "vue" in token.text and token.nbor(1).text in "sur":
                donneesClient['DescriptionPropriete'] += token.text + " " + token.nbor(1).text + " " + token.nbor(2).text + ", "

            elif token.text.lower in ["accueillant", "Propre", "travaux"]:
                donneesClient['DescriptionPropriete'] += token.text + ", "

            elif "quartier" in token.text and (token.nbor(1).text in "residentiel" or token.nbor(1).text in "résidentiel"):
                donneesClient['DescriptionPropriete'] += token.text + " " + token.nbor(1).text + " " + token.nbor(2).text + ", "

            elif "etat" in token.text and token.nbor(-1).text in "bon" :
                donneesClient['DescriptionPropriete'] += token.nbor(-1).text + " " + token.text + ", "

        print(f"File {demande_client} has been created.")

        global idClient
        donneesClient['idClient'] = str(idClient)
        #print("Dictionnaire :",donneesClient)

        return donneesClient
    else :
        print("Fichier client non trouvé !")

# Autre méthode / On peut remplir via Post la var Global et ensuite la retourner via get
'''
@app.get('/creationDonneeClients')
async def ReponseCreationDonneeClients():
    global donneesClient
    return donneesClient
'''

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)