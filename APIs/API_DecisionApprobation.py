# Transformation en API
from fastapi import FastAPI, APIRouter
from fastapi.security import HTTPBearer
import uvicorn
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API de Décision d'Approbation nous sert à savoir si une
    personne est apte à pouvoir rembourser un prêt s'il a une solvabilité.
    S'il n'a pas de solvabilité, alors c'est un refus.

###########################################################################
'''

app = FastAPI()
securite = HTTPBearer()

# Endpoint pour votre API
router = APIRouter()

@router.post("/decision_credit")
@app.post('/decision_credit')
async def decision_credit_endpoint(solvabilite : int):

    if int(solvabilite) == 1 :
        resultat = "ACCEPTE"
    else :
        resultat = "REFUS"

    return resultat
