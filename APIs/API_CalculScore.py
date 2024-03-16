from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import HTTPBearer
import uvicorn
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API de Calcul score est une API qui nous permet de retourner
    un score pour un client donné en fonction de ses antécédants banquaires.

###########################################################################
'''

app = FastAPI()
securite = HTTPBearer()

# Endpoint pour votre API
router = APIRouter()

@router.post("/calcul_score")
@app.post('/calcul_score')
async def calcul_score_endpoint(totalCredit: int, nbPayementRetard: int, nbBankRuptcy: int):
    
    score = 0

    # Poids pour chaque paramètre
    poids_total_credit = 3
    poids_nb_paiement_retard = -2
    poids_nb_bankruptcy = -4

    # Calculez le score en fonction des pondérations
    score += totalCredit * poids_total_credit
    score += nbPayementRetard * poids_nb_paiement_retard
    score += nbBankRuptcy * poids_nb_bankruptcy

    return score