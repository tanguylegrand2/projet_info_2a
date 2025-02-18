from Creation_BDD.execution_creation_bdd_communes import Execution_creation_bdd_communes
from Creation_BDD.execution_creation_bdd_parcelles import (
    Execution_creation_bdd_parcelles,
)


class Execution_creation_bdd:
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
        (communes_adj, table_id_nom) = Execution_creation_bdd_communes(
            self.chemin_local, self.date, self.departements
        ).applique()
        id_communes = [table_id_nom[i][0] for i in range(len(table_id_nom))]
        if self.select_parcelles:
            id_commune_id_parcelle = Execution_creation_bdd_parcelles(
                self.chemin_local, self.date, id_communes
            ).applique()
            return {
                "table id / nom": table_id_nom,
                "table des communes adjacentes": communes_adj,
                "tableau id commune / id parcelle en bordure de la commune": id_commune_id_parcelle,
            }
        else:
            return {
                "table id / nom": table_id_nom,
                "table des communes adjacentes": communes_adj,
            }
