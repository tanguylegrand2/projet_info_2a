import requests
import gzip
import json
import os


class Telechargement:
    """La classe Téléchargement est une classe qui appartient à la couche Client Layers. Elle permet de télécharger les données,
    et de les dézipper en lecture, ce qui permet aux restes du programmes de pouvoir utiliser ces fichiers.
    Cette classe communique avec la couche client Layer.
    """

    def telecharge_communes(self, chemin, annee="latest"):
        """Téléchage les communes de toute la France et les dézippent en lecture pour que le
        programme puisse les utiliser.

        Parameters :
        __________
        chemin : str
            Chemin du dossier où le fichier sera téléchargé
        annee : str, default= "latest"
            L'année des données

        Returns : list
        """

        if not os.path.exists(
            chemin + "/cadastre-france-communes" + annee + ".json.gz"
        ):
            with open(
                chemin + "/cadastre-france-communes" + annee + ".json.gz", "wb"
            ) as file:
                response = requests.get(
                    "https://cadastre.data.gouv.fr/data/etalab-cadastre/"
                    + annee
                    + "/geojson/france/cadastre-france-communes.json.gz"
                )
                file.write(response.content)

        with gzip.open(
            chemin + "/cadastre-france-communes" + annee + ".json.gz",
            mode="rt",
            encoding="UTF-8",
        ) as gzfile:
            data = json.load(gzfile)["features"]
        return data

    def telecharge_parcelles_par_commune(self, chemin, id_commune: str, annee="latest"):
        """Télécharge les parcelles d'une commune donnée et les dézippent en lecture
         pour que le programme puisse les utiliser.
        Parameters :
        __________
        chemin : str
            Chemin du dossier où le fichier sera téléchargé
        id_commune : str
            Identifiant de la commune dont l'utilisateur veut télécharger les parcelles
        annee : str, default = "latest"
            L'année des données

        Returns : list
        """
        if not os.path.exists(
            chemin + "/cadastre-" + id_commune + "-parcelles" + annee + ".json.gz"
        ):
            id_departement = id_commune[0:2]
            with open(
                chemin + "/cadastre-" + id_commune + "-parcelles" + annee + ".json.gz",
                "wb",
            ) as file:
                response = requests.get(
                    "https://cadastre.data.gouv.fr/data/etalab-cadastre/"
                    + annee
                    + "/geojson/communes/"
                    + id_departement
                    + "/"
                    + id_commune
                    + "/cadastre-"
                    + id_commune
                    + "-parcelles.json.gz"
                )
                file.write(response.content)

        with gzip.open(
            chemin + "/cadastre-" + id_commune + "-parcelles" + annee + ".json.gz",
            mode="rt",
            encoding="UTF-8",
        ) as gzfile:
            data = json.load(gzfile)["features"]
        return data

    def telecharge_parcelles_par_departement(
        self, chemin, id_departement: str, annee="latest"
    ):
        if not os.path.exists(
            chemin + "/cadastre-" + id_departement + "-parcelles" + annee + ".json.gz"
        ):
            with open(
                chemin
                + "/cadastre-"
                + id_departement
                + "-parcelles"
                + annee
                + ".json.gz",
                "wb",
            ) as file:
                response = requests.get(
                    "https://cadastre.data.gouv.fr/data/etalab-cadastre/{}/geojson/departements/{}/cadastre-{}-parcelles.json.gz".format(
                        annee, id_departement, id_departement
                    )
                )
                file.write(response.content)

        with gzip.open(
            chemin + "/cadastre-" + id_departement + "-parcelles" + annee + ".json.gz",
            mode="rt",
            encoding="UTF-8",
        ) as gzfile:
            data = json.load(gzfile)["features"]
        return data
