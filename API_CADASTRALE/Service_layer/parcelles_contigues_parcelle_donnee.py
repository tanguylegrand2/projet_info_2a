from DAO_layer.annee_dao import AnneeDAO
from DAO_layer.parcelle_dao import ParcelleDAO
import config
from Business_layer.fonctions.fonctions_points import Fonctions_Points
from Business_layer.figure_geometrique.rectangle import Rectangle
from Business_layer.fonctions.fonctions_multipolygon import Fonctions_Multipolygon
from Client_layer.telechargement import Telechargement
from DAO_layer.departement_dao import DepartementDAO
from DAO_layer.commune_contigue_dao import CommuneContigueDAO
from Creation_BDD.recherche_communes_autour_commune import (
    Recherche_communes_autour_commune,
)


class Parcelles_contigues_parcelle_donnee(object):
    def applique(
        self, id_parcelle: str, chemin: str = config.chemin_local, annee: str = "latest"
    ):

        """Parcelles contigues à une parcelle donnée

        La fonction prend en arguments un identifiant de parcelle et en option un chemin
        local où télécharger les données nécéssaires et une année. Elle va se servir du département
        et de l'année pour voir si la base de données peut être utile ou non pour trouver les
        parcelles contigues. Les données manquantes seront téléchargées et stockées au niveau du
        chemin spécifié. Si la base est utile, les calculs seront plus rapides, sinon, les calculs
        seront plus longs. Dans le cas ou la base de données est utile,
        il y a deux sous cas: la parcelle se trouve en bordure de commune et la parcelle se trouve
        au milieu. C'est dans ce second cas que les calculs
        sont les plus rapides.

        De manière générale, le programme a besoin de télécharger les parcelles de la commune associée
        à la parcelle entrée en paramètre car la base ne contient que les parcelles en bordure de commune.
        Si la base est utilisable, il n'est en revanche pas nécéssaire de télécharger les parcelles des
        communes contigues car les parcelles qui les entourent sont les seules qui peuvent être adjacentes
        à notre parcelle. Il suffit alors de les lire dans la base de données.

        Args:
                    id_parcelle (str): l'identifiant de la parcelle dont on cherche les parcelles
                                    adjacentes
                    chemin (str, optional): le chemin dans lequel sont téléchargés les fichiers associés
                                            au traitement
                    annee (str, optional): l'année des données auxquelles on s'intéresse

        Returns:
            list[str]: liste des parcelles adjacentes
        """

        num_commune = id_parcelle[:5]
        dep_commune = num_commune[:2]
        if (
            annee == AnneeDAO().get_annee()
            and dep_commune in DepartementDAO().get_all_departements()
        ):
            base_de_donnees_utilisable = True
        else:
            base_de_donnees_utilisable = False
        if base_de_donnees_utilisable:
            if id_parcelle in ParcelleDAO().get_parcelles_contigue_commune(num_commune):
                au_bord = True
            else:
                au_bord = False
        if base_de_donnees_utilisable and not au_bord:
            parcelles = Telechargement().telecharge_parcelles_par_departement(
                chemin, dep_commune, annee
            )
            pos_parcelles = []
            i = 0
            for parcelle in parcelles:
                if parcelle["properties"]["commune"] == num_commune:
                    pos_parcelles.append(i)
                i += 1
            parcelles = [parcelles[i] for i in pos_parcelles]
        elif base_de_donnees_utilisable and au_bord:
            parcelles = []
            id_communes_contigues = CommuneContigueDAO().get_commune_contigue_by_id(
                num_commune
            )
            id_communes_contigues = [
                id_communes_contigues[i][0] for i in range(len(id_communes_contigues))
            ]
            id_parcelles_en_bordure_de_communes_contigues = []
            departements = [dep_commune]
            for commune_contigue in id_communes_contigues:
                id_parcelles_en_bordure_de_communes_contigues += (
                    ParcelleDAO().get_parcelles_contigue_commune(commune_contigue)
                )
            for id in id_communes_contigues:
                departements.append(id[:2])
            departements = list(set(departements))
            for departement in departements:
                parcelles_departement = (
                    Telechargement().telecharge_parcelles_par_departement(
                        chemin, departement, annee
                    )
                )
                for parcelle in parcelles_departement:
                    if parcelle["properties"]["commune"] == num_commune or (
                        parcelle["properties"]["commune"] in id_communes_contigues
                        and parcelle["properties"]["id"]
                        in id_parcelles_en_bordure_de_communes_contigues
                    ):
                        parcelles.append(parcelle)
            parcelles_departement = None
        else:
            parcelles = []
            departements = [dep_commune]
            id_communes_contigues = []
            resultat_communes_contigues = Recherche_communes_autour_commune(
                chemin, num_commune, annee
            ).applique()[0]
            for ligne in resultat_communes_contigues:
                id_communes_contigues.append(ligne[0])
                id_communes_contigues.append(ligne[1])
            id_communes_contigues = list(set(id_communes_contigues))
            id_communes_contigues.remove(num_commune)
            for id in id_communes_contigues:
                departements.append(id[:2])
            departements = list(set(departements))
            for departement in departements:
                parcelles_departement = (
                    Telechargement().telecharge_parcelles_par_departement(
                        chemin, departement, annee
                    )
                )
                for parcelle in parcelles_departement:
                    if (
                        parcelle["properties"]["commune"] == num_commune
                        or parcelle["properties"]["commune"] in id_communes_contigues
                    ):
                        parcelles.append(parcelle)
            parcelles_departement = None
        for i in range(len(parcelles)):
            parcelles[i]["geometry"]["rectangle"] = Fonctions_Multipolygon().rectangle(
                parcelles[i]["geometry"]["coordinates"]
            )
        for i in range(len(parcelles)):
            if parcelles[i]["properties"]["id"] == id_parcelle:
                la_parcelle = parcelles.pop(i)
                break
        matchs = []
        for parcelle in parcelles:
            if la_parcelle["geometry"]["rectangle"].se_recoupent(
                parcelle["geometry"]["rectangle"]
            ):
                matchs.append(parcelle)
        parcelles = matchs.copy()
        matchs = []
        if config.passer_par_les_distances:
            la_parcelle["geometry"]["coordinates"] = Fonctions_Multipolygon().points(
                la_parcelle["geometry"]["coordinates"]
            )
            for parcelle in parcelles:
                parcelle["geometry"]["coordinates"] = Fonctions_Multipolygon().points(
                    parcelle["geometry"]["coordinates"]
                )
                for coord in parcelle["geometry"]["coordinates"]:
                    if Fonctions_Points().coord_appartient_a_liste_coord(
                        coord, la_parcelle["geometry"]["coordinates"]
                    ):
                        matchs.append(parcelle["properties"]["id"])
                        break
        if config.passer_par_les_segments:
            la_parcelle["geometry"]["coordinates"] = Fonctions_Multipolygon().segments(
                la_parcelle["geometry"]["coordinates"]
            )
            for parcelle in parcelles:
                parcelle["geometry"]["coordinates"] = Fonctions_Multipolygon().segments(
                    parcelle["geometry"]["coordinates"]
                )
                Trouve = False
                for segment1 in parcelle["geometry"]["coordinates"]:
                    for segment_de_la_parcelle in la_parcelle["geometry"][
                        "coordinates"
                    ]:
                        if segment1 == segment_de_la_parcelle:
                            matchs.append(parcelle["properties"]["id"])
                            Trouve = True
                            break
                    if Trouve:
                        break
        if config.conserver_les_matchs_par_rectangles_uniquement:
            for parcelle in parcelles:
                matchs.append(parcelle["properties"]["id"])
        return matchs
