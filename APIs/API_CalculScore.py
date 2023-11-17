from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

token_CalculScore = "AHshhxhwxsaSA23Evrfrve"

# Endpoint pour votre API
router = APIRouter()

@router.post("/calcul_score")
@app.post('/calcul_score')
async def calcul_score_endpoint(totalCredit: int, nbPayementRetard: int, nbBankRuptcy: int, current_user: Annotated[User, Depends(get_current_user)]):
    
    # Sécurité : check du token
    """if credentials.credentials != token_CalculScore:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else :
        print("Success authentication token")"""
    
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

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8002)
