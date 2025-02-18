from typing import List
from DAO_layer.db_connection import DBConnection


class AnneeDAO(object):
    def get_annee(self) -> str:
        """
        Récupérer l'année de la base
        return : annee
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM annee;")
                resultat = cursor.fetchone()
        return resultat["annee"]
