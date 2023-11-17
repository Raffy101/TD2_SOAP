# Transformation en API
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

token_DecisionApprob = "cqsdzdaSvrepdazdede"

# Endpoint pour votre API
router = APIRouter()

@router.post("/decision_credit")
@app.post('/decision_credit')
async def decision_credit_endpoint(solvabilite : int, current_user: Annotated[User, Depends(get_current_user)]):

    """if credentials.credentials != token_DecisionApprob:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else :
        print("Success authentication token")"""

    if int(solvabilite) == 1 :
        resultat = "ACCEPTE"
    else :
        resultat = "REFUS"

    return resultat

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8004)
