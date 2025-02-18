from typing import List
from DAO_layer.db_connection import DBConnection


class CommuneDAO(object):
    def insert_commune(sef, liste: List) -> None:
        """
        Insérer une commune dans la base de données.

        liste : ensemble des communes à insérer de format [[id, nom], [id, nom]]
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE commune CASCADE;")
                for comm in liste:
                    cursor.execute(
                        "INSERT INTO commune(id_commune, nom_commune) VALUES"
                        "\n(%(ident)s, %(nom)s)",
                        {"ident": comm[0], "nom": comm[1]},
                    )

    def get_all_commune(self, lim: int = 100) -> List:
        """
        Récupérer toutes les communes de la base de données
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM commune" "\nLIMIT %(limit)s", {"limit": lim}
                )
                resultat = cursor.fetchall()
        commune = []
        if resultat:
            for row in resultat:
                commune.append([row["id_commune"], row["nom_commune"]])
        return commune

    def get_commune_by_id(self, ident) -> str:
        """
        Récupérer une commune en spécifiant son identifiant

        id : identifiant de la commune

        return : nom_commune
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom_commune FROM commune" "\nWHERE id_commune = %(ident)s",
                    {"ident": ident},
                )
                resultat = cursor.fetchall()
        commune = []
        if resultat:
            for row in resultat:
                commune = row["nom_commune"]
        return commune
