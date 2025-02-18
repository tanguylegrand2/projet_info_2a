from Creation_BDD.initialisation_base import Initialisation_base
import config

# Code d'initialisation de la base de données avec les données les plus récentes ("latest") des départements
# Loir-et-cher ("41") et Cher ("18"). Le chemin local désigne le lien de stockage utilisé par le programme pour
# télécharger les données sur le site web. Celui ci est à définir dans le fichier config.py à la racine
# du programme. Le paramètre select_parcelles est défini sur True car on a souhaité laisser
# la possibilité à l'administrateur de faire tourner son API en mode "restreint" pour accélérer
# les temps de calcul.
Initialisation_base(
    chemin_local=config.chemin_local,
    date="latest",
    departements=["41", "18"],
    select_parcelles=True,
).applique()
