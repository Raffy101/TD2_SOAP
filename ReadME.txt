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

-------------------------------------------------------------------

Procédure de lancement du projet.

Maintenant que tous les services sont en marche ! Il nous faut maintenant démarrer l'interface Web nous permettant
d'effectuer la demande de prêt.

# Commande pour lancer l'application (Va lancer les services + l'interface)

---> python .\index.py

------------------------------------------------------------------------------------------------------------

Utilisation : 

Le client accède à l'interface via l'url suivant : http://localhost:8000

Ici on suppose que le client à déjà un compte sur la base de données de la banque. Ainsi, le client doit se connecter.
Voici quelques clients :
username = DoeJ, password = loikujytgrehujrjrsjd
username = SmithW, password = poiuytreza
username = DupontJ, password = azertyuiop

Sur l'interface, le client peut choisir de déposer soit même un fichier txt (avec la description textuel) ou bien
directement saisir la demande sur le site.

Sur un autre onglet, il pourra consulter le résultat obtenu en saissant son nom ( s'il a au préalable effectuer une demande ).
