from DAO_layer.parcelle_dao import ParcelleDAO
from DAO_layer.annee_dao import AnneeDAO
from DAO_layer.departement_dao import DepartementDAO
from Creation_BDD.execution_creation_bdd_parcelles import (
    Execution_creation_bdd_parcelles,
)
import config


class ParcellesEnLimiteCommune(object):
    def applique(
        self, id_commune: str, chemin: str = config.chemin_local, annee: str = "latest"
    ):
        """Parcelles en limite à une commune donnée

        Notre base de données contient une table donnant la liste des parcelles en limites de chaque
        communes pour un département donné et une année donnée. Ainsi, cette fonction prend en entrée
        l'identifiant de la commune et l'année des données que veux l'utilisateur, et extrait le
        département, obtenu par les deux premiers caractères de l'identifiant de la commune, pour voir
        si la base de données est utilisable. Dans ce cas, on fait appel à une fonction de la DAO qui
        va nous renvoyer la liste des parcelles en bordures de la commune donnée résultat. Dans le cas
        contraire, la fonction ajoute en option un chemin local où télécharger les données nécéssaires
        et utilise des fonctions de la couche création de la base de données pour obtenir les parcelles
        qui sont au bord de la commune donnée.

        Args:
            id_commune (str): l'identifiant de la commune dont on cherche les communes adjacentes
            chemin (str, optional): le chemin dans lequel sont téléchargés les fichiers associés au traitement
            annee (str, optional): l'année des données auxquelles on s'intéresse

        Returns:
            list[str]: liste des parcelles adjacentes
        """
        dep_commune = id_commune[:2]
        if (
            annee == AnneeDAO().get_annee()
            and dep_commune in DepartementDAO().get_all_departements()
        ):
            base_de_donnees_utilisable = True
        else:
            base_de_donnees_utilisable = False

        if base_de_donnees_utilisable:
            return ParcelleDAO().get_parcelles_contigue_commune(id_commune)
        else:
            parcelles = Execution_creation_bdd_parcelles(
                chemin, annee, [id_commune]
            ).applique()
            parcelles = [parcelles[i][1] for i in range(len(parcelles))]
            return parcelles
