from fastapi import FastAPI, APIRouter
from fastapi.security import HTTPBearer
import re
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API Evaluation de propriété nous sert à analyser la
    description du bien immobilier que la personne souhaite acquérir
    et nous renvoi une estimation de sa valeur.

###########################################################################
'''

app = FastAPI()
securite = HTTPBearer()

router = APIRouter()

@router.post("/evaluation_propriete")
@app.post('/evaluation_propriete')
async def evaluation_propriete(description : str, token: str = Depends(oauth2_scheme)):

    #print(description)
    valeur = 0

    list_mots = re.findall(r'\w+', description)
    #print(list_mots)

    for i, mot in enumerate(list_mots):
        if mot == "maison" or mot == "Maison" :
            valeur = valeur + 100000
        elif mot == "appartement" or mot == "Appartement":
            valeur = valeur + 50000
        elif mot == "etages" or mot == "Etages":
            if i > 0:
                prev_mot = list_mots[i - 1]
                if prev_mot == "1":
                    valeur = valeur + 10000
                elif prev_mot == "2":
                    valeur = valeur + 20000
                elif prev_mot == "3":
                    valeur = valeur + 30000
        elif mot == "piscine" or mot == "Piscine":
            valeur = valeur + 50000

    print("Evaluation de la propriete estimée à : ", valeur)        
    return valeur