from typing import List
from DAO_layer.db_connection import DBConnection


class DepartementDAO(object):
    def insert_departements(self, departements: List):
        """
        Insérer les départements
        """
        with DBConnection.connection as connection:
            with connection.cursor() as cursor:
                for dept in departements:
                    cursor.execute(
                        "INSERT INTO departements(departement) VALUES" "\n(%(ident)s)",
                        {"ident": dept},
                    )

    def get_all_departements(self) -> List:
        """
        Récupérer les départements avec lesquels la base a été initialisée
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM departements;")
                resultat = cursor.fetchall()
        departements = []
        if resultat:
            for row in resultat:
                departements.append(row["departement"])
        return departements
