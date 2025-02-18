===================================================================================================================================
                                                             FRANCAIS
===================================================================================================================================


But de l'API :
==============
Notre API permet de répondre aux questions suivantes :

QUESTION 1 : Quelles sont les communes contiguës à une commune donnée

QUESTION 2 : Quelles sont les parcelles qui sont en limite d'une commune donnée

QUESTION 3 : Quelles sont les parcelles contiguës à une parcelle donnée


Pour utiliser l'API :
=====================
ETAPE 1 : Se rendre à la racine dans le fichier config.py et choisir un emplacement de dossier local.
          Il est également possible de choisir une méthode de calcul pour savoir si deux zones géographiques
          sont attenantes : Au choix (distance+seuil , rectangles qui se recoupent, segment en commun).

ETAPE 2 : Vérifier que le fichier .env pointe vers une base de données postgre valide.

ETAPE 3 : Si la base est déja remplie, passer l'étape. Sinon, executer initialisation_de_la_base_de_donnees_Administrateur.py
	    à la racine avec les paramètres voulus.

ETAPE 4 : Lancer __main__.py à la racine.

ETAPE 5 : Envoyer des requêtes. Les requêtes possibles sont détaillées en faisant localhost/aide.
          Pour plus de détails sur les requêtes, le code est consultable dans Controler_layer/control_layer.py.


/!\ AVERTISSEMENT /!\ : Les données de 2019 semblent disponibles sur le site mais les fichiers ne sont en réalité pas présents.
				Seules les données à partir de 2020 sont téléchargeables.


Définition des différentes couches :
==================================================================================================================================

DAO_layer: communiquer avec la base de données (lecture et écriture)

Client_layer : télécharger les fichiers sur le site internet et les décompresser

Controler_layer : contient l'API permettant de recevoir les requêtes des utilisateurs. 
Transmet ensuite les requêtes au service, puis récupère la réponse et la renvoie à l'utilisateur. 

Business_layer : contient les objets métiers. Chaque objet métier contient les fonctions nécéssaires.

Service_layer : Permet de faire appel à toutes les classes de manière coordonnée afin de répondre aux questions.
Le service layer ne doit cependant pas contenir de code "intelligent" (pas d'algos complexes). Il se contente de mettre en
relation les classes et doit être codé simplement.

creation_BDD : Code légèrement à part. C'est le code qui sera executé lorsque l'administrateur souhaitera changer de
zone géographique. Il utilise le client pour télécharger les données. Ensuite les objets metier du Business layer sont utilisés
afin de créer une base qui est enfin envoyée à la DAO pour être enregistrée.

===============================================================================================================================




===============================================================================================================================
                                                      ENGLISH
===============================================================================================================================


Purpose of the API:
==============
Our API allows to answer the following questions:

QUESTION 1: What are the municipalities adjacent to a given municipality?

QUESTION 2: Which parcels border a given municipality

QUESTION 3: Which parcels are contiguous to a given parcel


To use the API:
=====================
STEP 1: Go to the root in the config.py file and choose a local folder location.
          It is also possible to choose a calculation method to know if two geographical areas
          are adjacent: Your choice (distance+threshold, intersecting rectangles, segment in common).

STEP 2: Check that the .env file points to a valid postgre database.

STEP 3 : If the database is already filled, skip this step. Otherwise, execute initialisation_de_la_base_de_donnees_Administrateur.py
	    at the root with the desired parameters.

STEP 4 : Run __main__.py at the root.

STEP 5 : Send queries. The possible requests are detailed by doing localhost/aide.
          For more details on the requests, the code is available in Controler_layer/control_layer.py.


/!\ WARNING /!\ : The 2019 data seems to be available on the site but the files are not actually present.
				Only data from 2020 onwards is available for download.


Definition of the different layers :
==================================================================================================================================

DAO_layer: communicate with the database (read and write)

Client_layer: download files from the website and unzip them

Controler_layer: contains the API to receive user requests. 
It then transmits the requests to the service, then retrieves the response and sends it back to the user. 

Business_layer: contains the business objects. Each business object contains the necessary functions.

Service_layer: Allows all classes to be called in a coordinated manner in order to answer questions.
However, the service layer must not contain any "intelligent" code (no complex algos). It simply connects the classes and must be
classes and must be coded simply.

creation_BDD: Slightly separate code. This is the code that will be executed when the administrator wishes to change the
geographical area. It uses the client to download the data. Then the business objects of the Business layer are used
to create a database which is finally sent to the DAO to be registered.

===============================================================================================================================
