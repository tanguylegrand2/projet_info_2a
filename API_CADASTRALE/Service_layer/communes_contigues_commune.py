from DAO_layer.commune_contigue_dao import CommuneContigueDAO
from DAO_layer.annee_dao import AnneeDAO
from DAO_layer.departement_dao import DepartementDAO
from Creation_BDD.recherche_communes_autour_commune import (
    Recherche_communes_autour_commune,
)
import config


class CommunesContiguesCommune(object):
    def applique(
        self, id_commune: str, chemin: str = config.chemin_local, annee: str = "latest"
    ):
        """Communes contigues à une commune donnée

        Etant donné que notre base de données contient une table donnant la liste des communes
        contigues entre elles pour un département et une année donnés, cette fonction prend en entrée
        l'identifiant de la commune et l'année des données que veux l'utilisateur, et extrait le département,
        obtenu par les deux premiers caractères de l'identifiant de la commune, pour voir si la base de données
        est utilisable. Dans ce cas, on fait appel à une fonction de la DAO qui nous renvera le résultat. Dans
        le cas contraire, la fonction ajoute en option un chemin local où télécharger les données nécéssaires
        et utilise des fonctions de la couche création de la base de données pour obtenir les communes contigues
        à notre commune donnée.

        Args:
            id_commune (str): l'identifiant de la commune dont on cherche les communes adjacentes
            chemin (str, optional): le chemin dans lequel sont téléchargés les fichiers associés au traitement
            annee (str, optional): l'année des données auxquelles on s'intéresse

        Returns:
            list[str]: liste des communes adjacentes
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
            return CommuneContigueDAO().get_commune_contigue_by_id(id_commune)
        else:
            communes_contigues = Recherche_communes_autour_commune(
                chemin_local=chemin, id_commune=id_commune, date=annee
            ).applique()[1]
            for i in range(len(communes_contigues)):
                if communes_contigues[i][0] == id_commune:
                    communes_contigues.pop(i)
                    break
            return communes_contigues
