from typing import List
from DAO_layer.db_connection import DBConnection


class ParcelleDAO(object):
    def insert_parcelle(sef, liste: List) -> None:
        """
        Insérer une parcelle dans la base de données.

        liste : ensemble des parcelles à insérer de format [[id_commune, id_parcelle], [id_commune, id_parcelle]]
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE parcelle CASCADE;")
                for parcel in liste:
                    cursor.execute(
                        "INSERT INTO parcelle(id_parcelle, id_commune) VALUES"
                        "\n(%(ident1)s, %(ident2)s)",
                        {"ident1": parcel[1], "ident2": parcel[0]},
                    )

    def get_all_parcelle(self, lim: int = 100) -> List:
        """
        Récupérer toutes les parcelles de la base de données
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM parcelle" "\nLIMIT %(limit)s", {"limit": lim}
                )
            resultat = cursor.fetchall()
        parcelle = []
        if resultat:
            for row in resultat:
                parcelle.append([row["id_parcelle"], row["id_commune"]])
        return parcelle

    def get_parcelles_contigue_commune(self, ident: str) -> List:
        """
        Renvoyer les parcelles en bordure d'une commune donnée

        ident : identifiant de la commune

        return : ensemble des parcelles en bordure de la commune
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_parcelle FROM parcelle" "\nWHERE id_commune = %(ident)s",
                    {"ident": ident},
                )
                resultat = cursor.fetchall()
        parcelle = []
        if resultat:
            for row in resultat:
                parcelle.append(row["id_parcelle"])
        return parcelle
