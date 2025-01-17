Projet de SOAP réalisé par : Othmane ABDIMI et Raffaele GIANNICO
Promotion : IATIC-5 
TD2
------------------------------------------------------------------

Attention il est possible qui soit nécessaire d'installer des
package supplémentaire pour pouvoir lancer l'application

--> pip install sqlalchemy

--> pip install uvicorn

--> pip install spacy

--> pip install python-multipart

--> pip install fastapi

--> pip install passlib

--> pip install python-jose

--> pip install pydantic
-------------------------------------------------------------------

Procédure de lancement du projet.

Maintenant que tous les services sont en marche ! Il nous faut maintenant démarrer l'interface Web nous permettant
d'effectuer la demande de prêt.

# Commande pour lancer l'application (Va lancer les services + l'interface)

---> python .\index.py

ou en fesant simplement un run depuis votre IDE

(S'il y'a des problème lors du lancement, vérifiez que vous êtes bien dans le répertoire)
------------------------------------------------------------------------------------------------------------

Le dossier APIs contient toute les API qui sont utilisés dans la pipeline.
Le dossier Database lui contient la base de données.
Le dossier DemandesClients contient toute les demandes des clients au format txt.
Le dossier Resultat contient tout les resultats de la demandes des clients.
Le dossier static contient toutes les ressources de notre interface.
Le dossier template contient les pages html de notre interface.
Le fichier Api_Main.py contient la fonction qui déclenchera la pipeline.
Le fichier utils.py contient des fonctions, librairies et variables utilisés dans d'autres fichiers.
Le fichier index.py contient les différentes routes accessible de notre application.

-----------------------------------------------------------------------------------------------------------
Utilisation : 

Le client accède à l'interface via l'url suivant : http://localhost:8000

-- Connexion 

Ici on suppose que le client à déjà un compte sur la base de données de la banque. Ainsi, le client doit se connecter.
Voici quelques clients :
username = DoeJ, password = loikujytgrehujrjrsjd
username = SmithW, password = poiuytreza
username = DupontJ, password = azertyuiop

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/!\ Afin que la demande soit prise en compte correctement. Veuillez vous assurer que le nom inscrit dans la demande correspond
bien à votre compte. Sinon cela produira une erreur et la demande n'aboutiera pas.
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

-- Réalisation de la demande 

Sur l'interface, le client peut choisir de déposer soit même un fichier txt (avec la description textuel) ou bien
directement saisir la demande sur le site.

-- Exemple de demande Accepté : 

Bonjour, je m'appelle Jean Dupont, je vis au 3 rue de la liberte a Paris. 
Je voudrai demander un pret de 2000 € pour 20 ans. 
En effet, j'ai une propriete qui a 2 etages avec jardin, 
situee dans un quartier residentiel calme. 50 m², 3 chambres, 2 salles de bains. Travaux nécessaire mais quand meme en bon etat. On a meme une vue sur mer. 
Je pourrais rembourser sans probleme. 
Je gagne 5000 € par mois et je fais tres peu 
de depenses environ 500 € (j'economise beaucoup). 
Si besoin n'hesitez pas a me contacter : +33612457847 ou 
par mail : toto.junior@email.com

-- Exemple de demande refusé :
Bonjour, je m'appelle John Doe, je vis au 3 rue de la liberte a Paris. 
Je voudrai demander un pret de 10000 € pour 5 ans. 
En effet, j'ai une propriete, 
situee dans un quartier residentiel calme. Travaux nécessaire mais quand meme en bon etat. 
Je pourrais rembourser sans probleme. 
Je gagne 100 € par mois et je fais tres peu 
de depenses environ 1000 € (j'economise beaucoup). 
Si besoin n'hesitez pas a me contacter : +33612457847 ou 
par mail : toto.junior@email.com. 

-- Consultation du résultat

Sur un autre onglet, il pourra consulter le résultat obtenu en saissant son nom ( s'il a au préalable effectuer une demande ).

