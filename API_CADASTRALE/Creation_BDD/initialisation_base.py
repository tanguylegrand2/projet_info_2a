from Creation_BDD.execution_creation_bdd import Execution_creation_bdd
from DAO_layer.db_connection import DBConnection
from DAO_layer.parcelle_dao import ParcelleDAO
from DAO_layer.commune_contigue_dao import CommuneContigueDAO
from DAO_layer.commune_dao import CommuneDAO


class Initialisation_base:
    def __init__(
        self,
        chemin_local: str,
        date: str = "latest",
        departements: list = [],
        select_parcelles: bool = True,
    ):
        self.chemin_local = chemin_local
        self.date = date
        self.departements = departements
        self.select_parcelles = select_parcelles

    def applique(self):
        dictionnaire = Execution_creation_bdd(
            self.chemin_local, self.date, self.departements, self.select_parcelles
        ).applique()

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DROP TABLE IF EXISTS commune CASCADE;"
                    "\nCREATE TABLE commune (id_commune VARCHAR(20) NOT NULL PRIMARY KEY,nom_commune VARCHAR(50) NOT NULL);"
                    "\nDROP TABLE IF EXISTS parcelle CASCADE;"
                    "\nCREATE TABLE parcelle (id_parcelle VARCHAR(20) NOT NULL PRIMARY KEY,"
                    "\nid_commune VARCHAR(20) NOT NULL REFERENCES commune(id_commune) ON DELETE CASCADE ON UPDATE CASCADE);"
                    "\nDROP TABLE IF EXISTS commune_contigue CASCADE;"
                    "\nCREATE TABLE commune_contigue (id_commune1 VARCHAR(20) NOT NULL REFERENCES commune(id_commune) ON DELETE CASCADE ON UPDATE CASCADE,"
                    "\nid_commune2 VARCHAR(20) NOT NULL REFERENCES commune(id_commune) ON DELETE CASCADE ON UPDATE CASCADE,PRIMARY KEY (id_commune1, id_commune2));"
                    "\nDROP TABLE IF EXISTS annee CASCADE;"
                    "\nCREATE TABLE annee (annee VARCHAR(20) NOT NULL PRIMARY KEY);"
                    "\nINSERT INTO annee(annee) VALUES"
                    "\n(%(year)s)",
                    {"year": self.date},
                )
                cursor.execute(
                    "\nDROP TABLE IF EXISTS departements CASCADE;"
                    "\nCREATE TABLE departements (departement VARCHAR(20) NOT NULL PRIMARY KEY);"
                )

                for departement in self.departements:
                    cursor.execute(
                        "\nINSERT INTO departements(departement) VALUES" "\n(%(dep)s)",
                        {"dep": departement},
                    )

        if self.select_parcelles:
            CommuneDAO().insert_commune(dictionnaire["table id / nom"])
            CommuneContigueDAO().insert_commune_contigue(
                dictionnaire["table des communes adjacentes"]
            )
            ParcelleDAO().insert_parcelle(
                dictionnaire[
                    "tableau id commune / id parcelle en bordure de la commune"
                ]
            )
        else:
            CommuneDAO().insert_commune(dictionnaire["table id / nom"])
            CommuneContigueDAO().insert_commune_contigue(
                dictionnaire["table des communes adjacentes"]
            )
