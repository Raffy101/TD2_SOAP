from fastapi import FastAPI, APIRouter
from fastapi.security import HTTPBearer
import re
from utils import *

'''
###########################################################################

Creator : Othmane ABDIMI & Raffaele GIANNICO

Description : L'API de vérification de solvabilité va nous permettre de 
    savoir si notre client possède des économies et qu'il est donc apte
    à pouvoir rembourser petit à petit un prêt.

###########################################################################
'''

app = FastAPI()
securite = HTTPBearer()

# Endpoint pour votre API
router = APIRouter()

@router.post("/verification_solvabilite")
@app.post('/verification_solvabilite')
def verification_solvabilite(salaireMensuel : str, depenseMensuel : str, calcul_score : int,dureeDuPret : str, token: str = Depends(oauth2_scheme)):

    # Dans le cas où Salaire et Dépense mensuel contiendrait dans la chaîne de caractère une devise monaitaire ! 
    list_mots1 = re.findall(r'\w+', salaireMensuel)
    list_mots2 = re.findall(r'\w+', depenseMensuel) 
    list_mots3 = re.findall(r'\w+', dureeDuPret)

    economieMensuel = int(list_mots1[0]) - int(list_mots2[0])
    print(" economieMensuel :",  economieMensuel)
    print(" calculscore :",  calcul_score)

    ratioAnnee = (int(dureeDuPret)/ economieMensuel) / 12 
    solvabilite = 0

    # On vérifie que le temps de remboursement soit inférieur à 10 ans et Un score Positif
    if (ratioAnnee > 0 and ratioAnnee < 10.0) and calcul_score > 0 :
        solvabilite = 1
    else : 
        solvabilite = 0

    return solvabilite