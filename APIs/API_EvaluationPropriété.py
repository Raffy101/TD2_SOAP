from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

import re

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

token_EvalProp = "dfeferjclefekzffS22EDkfazc"

@app.post('/evaluation_propriete')
async def evaluation_propriete(description : str , credentials: HTTPAuthorizationCredentials = Depends(securite)):
    
    if credentials.credentials != token_EvalProp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token"
        )
    else :
        print("Success authentication token")

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

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8001)