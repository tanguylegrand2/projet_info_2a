from Service_layer.parcelles_contigues_parcelle_donnee import (
    Parcelles_contigues_parcelle_donnee,
)
from Service_layer.communes_contigues_commune import CommunesContiguesCommune
from Service_layer.parcelles_en_limite_commune import ParcellesEnLimiteCommune
from Business_layer.fonctions.lire_annees_site_cadastre import LireAnneesSiteCadastre
from DAO_layer.annee_dao import AnneeDAO
from DAO_layer.departement_dao import DepartementDAO
from fastapi import FastAPI
import config
import uvicorn


class ControlLayer:
    def lancer(self):
        app = FastAPI()

        @app.get("/communes_contigues_commune/{idCommune}")
        async def get_communes_contigues(idCommune: str, year: str = "latest"):
            """Renvoi les communes contigues a une commune donnée

            Args:
                idCommune (str) : l'identifiant de la commune dont on cherche les communes contigues
                year : Année souhaitée. Defaults "latest"

            Returns:
                list[dict] : liste des communes contigues
            """
            if len(idCommune) != 5:
                return "Erreur !! L'identifiant entré ne respecte pas la forme de l'identifiant d'une commune."
            elif year not in list(LireAnneesSiteCadastre().applique()[0].values())[0]:
                return "Cette date n'a pas de base sur le site du cadastre. Taper 'localhost/annees' pour voir les dates disponibles"
            else:
                communes = CommunesContiguesCommune().applique(
                    idCommune, config.chemin_local, year
                )
                return [{"communes contigues": communes}]

        @app.get("/parcelles_en_limite_commune/{idCommune}")
        async def get_parcelles_en_limite_commune(idCommune: str, year: str = "latest"):
            """Renvoi les parcelles en limite a une commune donnée

            Args:
                idCommune (str) : l'identifiant de la commune dont on cherche les parcelles en bordures
                year : Année souhaitée. Defaults "latest"

            Returns:
                list[dict] : liste des parcelles en limite à la commune
            """
            if len(idCommune) != 5:
                return "Erreur !! L'identifiant entré ne respecte pas la forme de l'identifiant d'une commune."
            elif year not in list(LireAnneesSiteCadastre().applique()[0].values())[0]:
                return "Cette date n'a pas de base sur le site du cadastre. Taper 'localhost/annees' pour voir les dates disponibles"
            else:
                parcelle = ParcellesEnLimiteCommune().applique(
                    id_commune=idCommune, chemin=config.chemin_local, annee=year
                )
                return [{"id_parcelle": parcelle}]

        @app.get("/parcelles_contigues_parcelle/{idParcelle}")
        async def get_parcelles_contigues_parcelle(
            idParcelle: str, year: str = "latest"
        ):
            """get_parcelles_contigues_parcelle

            Args:
                idParcelle (str): l'identifiant de la parcelle dont on cherche les parcelles
                                  adjacentes.
                year (str, optional): l'année souhaitée. Defaults to "latest".

            Returns:
                list[dict]: les parcelles adjacentes
            """
            if len(idParcelle) != 14:
                return "Erreur !! L'identifiant entré ne respecte pas la forme de l'identifiant d'une commune."
            elif year not in list(LireAnneesSiteCadastre().applique()[0].values())[0]:
                return "Cette date n'a pas de base sur le site du cadastre. Taper 'localhost/annees' pour voir les dates disponibles"
            else:
                parcelles = Parcelles_contigues_parcelle_donnee().applique(
                    id_parcelle=idParcelle, chemin=config.chemin_local, annee=year
                )
                return [{"parcelles": parcelles}]

        @app.get("/annees")
        async def get_annees():
            """
            Aide pour permettre à l'utilisateur de savoir les dates disponibles pour les bases
            de données et dans quel format doit il insérer l'argument date dans les fonctions
            précédentes.
            """
            return LireAnneesSiteCadastre().applique()

        @app.get("/bdd")
        async def bdd():
            """
            Aide pour permettre à l'utilisateur de voir la date dont les données sont en base.
            """
            return [
                {
                    "année en base: ": AnneeDAO().get_annee(),
                    "départements en base": DepartementDAO().get_all_departements(),
                }
            ]

        @app.get("/aide")
        async def aide():
            """
            Aide d'utilisation de l'API. Comment envoyer des requêtes à l'API.
            """
            return [
                {
                    "Afficher les années disponibles pour les requêtes (à mettre à la place de latest dans les exemples)": "localhost/annees",
                    "Afficher l'année et les départements chargés dans la base": "localhost/bdd",
                    "Afficher les codes insee des communes contigues à la commune 41001 pour la dernière date disponible sur le site": "localhost/communes_contigues_commune/41001?year=latest",
                    "Afficher les numeros de parcelles en bordure de la commune 41001 pour la dernière date disponible sur le site": "localhost/parcelles_en_limite_commune/41001?year=latest",
                    "Afficher les numeros de parcelles contigues à la parcelle 41001000ZI0027 pour la dernière date disponible sur le site": "localhost/parcelles_contigues_parcelle/41001000ZI0027?year=latest",
                }
            ]

        uvicorn.run(app, host="0.0.0.0", port=80)
