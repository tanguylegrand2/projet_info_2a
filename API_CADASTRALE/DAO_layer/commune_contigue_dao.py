from typing import List
from DAO_layer.db_connection import DBConnection
from DAO_layer.commune_dao import CommuneDAO


class CommuneContigueDAO(object):
    def insert_commune_contigue(self, liste: List):
        """
        Insertion des différentes communes dans la base de données

        liste : Liste des différentes communes adjacentes du format [[id1, id2], [id2, id3]]

        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE commune_contigue CASCADE;")
                for comm in liste:
                    cursor.execute(
                        "INSERT INTO commune_contigue(id_commune1, id_commune2) VALUES"
                        "\n(%(ident1)s, %(ident2)s)",
                        {"ident1": comm[0], "ident2": comm[1]},
                    )

    def get_all_commune_contigue(self, lim: int = 100) -> List:
        """
        Obtenir l'ensemble des communes contigues
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM commune_contigue"
                    "\nORDER BY id_commune1"
                    "\nLIMIT %(limit)s",
                    {"limit": lim},
                )
                resultat = cursor.fetchall()
        communes = []
        if resultat:
            for row in resultat:
                communes.append([row["id_commune1"], row["id_commune2"]])
        return communes

    def get_commune_contigue_by_id(self, ident) -> List:
        """
        Obtenir les communes contigues à une commune donnée

        ident : identifiant de la commune

        Return : liste contenant les communes contigues à id
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_commune2 FROM commune_contigue"
                    "\nWHERE id_commune1 = %(ident)s",
                    {"ident": ident},
                )
                resultat1 = cursor.fetchall()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_commune1 FROM commune_contigue"
                    "\nWHERE id_commune2 = %(ident)s",
                    {"ident": ident},
                )
                resultat2 = cursor.fetchall()
        communes = []
        if resultat1:
            for row in resultat1:
                communes.append(row["id_commune2"])
        if resultat2:
            for row in resultat2:
                communes.append(row["id_commune1"])
        commune = []
        if len(communes) != 0:
            for ids in communes:
                commune.append([ids, CommuneDAO().get_commune_by_id(ids)])
        return commune
