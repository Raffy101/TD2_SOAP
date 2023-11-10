Projet de SOAP réalisé par : Othmane ABDIMI et Raffaele GIANNICO
Promotion : IATIC-5 
TD2
------------------------------------------------------------------

Procédure de lancement du projet.

Afin de pouvoir exécuter le projet il vous faut d'abord lancé les différentes API utilisés :
( dans des terminals différents ! )

# Commande pour lancer L'API d'extraction : 

---> python .\APIs\API_Extraction.py

# Commande pour lancer L'API d'évaluation de propriété : 

---> python .\APIs\API_EvaluationPropriété.py

# Commande pour lancer L'API de calcul de score : 

---> python .\APIs\API_CalculScore.py

# Commande pour lancer L'API de vérification de solvabilité : 

---> python .\APIs\API_VerifSolvabilité.py 

# Commande pour lancer L'API de décision d'approbation : 

---> python .\APIs\API_DecisionApprobation.py

Un fois celà fait, nous pouvons lancer notre programme Python Main qui fait appel à ces services

# Commande Pour lancer le programme :

---> python .\API_Main.py

Maintenant que tous les services sont en marche ! Il nous faut maintenant démarrer l'interface Web nous permettant
d'effectuer la demande de prêt.

# Commande pour lancer l'interface 

---> python .\index.py

------------------------------------------------------------------------------------------------------------

Utilisation : 

Le client accède à l'interface via l'url suivant : http://127.0.0.1:5000

Sur l'interface, le client peut choisir de déposer soit même un fichier txt (avec la description textuel) ou bien
directement saisir la demande sur le site.

Sur un autre onglet il pourra consulter le résultat obtenu en saissant son nom ( s'il a au préhalable effectuer une demande ).
