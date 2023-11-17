from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import re
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API de vérification de solvabilité va nous permettre de 
    savoir si notre client possède des économies et qu'il est donc apte
    à pouvoir rebourser petit à petit un prêt.

###########################################################################
'''

app = FastAPI()
securite = HTTPBearer()

token_VerifSolva = "AHqsddazcvfervbrXZ3repdazdede"

# Endpoint pour votre API
router = APIRouter()

@router.post("/verification_solvabilite")
@app.post('/verification_solvabilite')
def verification_solvabilite(salaireMensuel : str, depenseMensuel : str, calcul_score : int, current_user: Annotated[User, Depends(get_current_user)]):
    
    """if credentials.credentials != token_VerifSolva:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else :
        print("Success authentication token")"""

    # Dans le cas où Salaire et Dépense mensuel contiendrait dans la chaîne de caractère une devise monaitaire ! 
    list_mots1 = re.findall(r'\w+', salaireMensuel)
    list_mots2 = re.findall(r'\w+', depenseMensuel) 

    economieMensuel = int(list_mots1[0]) - int(list_mots2[0])
    print(" economieMensuel :",  economieMensuel)
    print(" calculscore :",  calcul_score)
    solvabilite = 0
    if economieMensuel > 0 and calcul_score > 0 :
        solvabilite = 1
    else : 
        solvabilite = 0

    return solvabilite

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8003)