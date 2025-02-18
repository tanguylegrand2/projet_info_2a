from logging import raiseExceptions
from Creation_BDD.execution_creation_bdd_communes import Execution_creation_bdd_communes
from Client_layer.telechargement import Telechargement
from Business_layer.fonctions.fonctions_multipolygon import Fonctions_Multipolygon
from Business_layer.fonctions.fonctions_points import Fonctions_Points
from Business_layer.figure_geometrique.segment import Segment
import config
from Business_layer.figure_geometrique.rectangle import Rectangle


class Execution_creation_bdd_parcelles:
    def __init__(
        self,
        chemin_local: str,
        date: str = "latest",
        liste_communes: list = [],
        data_pos: list = None,
    ):
        if data_pos != None:
            self.liste_communes = [
                data_pos[i]["properties"]["id"] for i in range(len(data_pos))
            ]
        elif liste_communes != []:
            self.liste_communes = liste_communes
        else:
            raiseExceptions(
                "sur quelles communes appliquer Execution_creation_bdd_parcelles.applique() ?"
            )
        self.chemin_local = chemin_local
        self.date = date
        self.data_pos = data_pos

    def applique(self):
        departements = list(set([ident[0:2] for ident in self.liste_communes]))
        tableau_parcelles = []
        for departement in departements:
            parcelles_departement = (
                Telechargement().telecharge_parcelles_par_departement(
                    self.chemin_local, departement, self.date
                )
            )
            for parcelle in parcelles_departement:
                if parcelle["properties"]["commune"] in self.liste_communes:
                    tableau_parcelles.append(parcelle)
        parcelles_departement = None
        if self.data_pos == None:
            self.data_pos = Telechargement().telecharge_communes(
                self.chemin_local, self.date
            )
            indices_communes = []
            for i in range(len(self.data_pos)):
                if self.data_pos[i]["properties"]["id"] in self.liste_communes:
                    indices_communes.append(i)
            self.data_pos = [self.data_pos[i] for i in indices_communes]
        pos_communes_pos_parcelles = []
        for i in range(len(self.data_pos)):
            pos_communes_pos_parcelles.append([i, []])
            for j in range(len(tableau_parcelles)):
                if (
                    tableau_parcelles[j]["properties"]["commune"]
                    == self.data_pos[i]["properties"]["id"]
                ):
                    pos_communes_pos_parcelles[-1][1].append(j)

        tableau_id_commune_id_parcelles = []
        for i in range(len(self.data_pos)):
            tableau_id_commune_id_parcelles.append(
                [self.data_pos[i]["properties"]["id"], []]
            )

        for pos_commune in range(len(self.data_pos)):
            self.data_pos[pos_commune]["geometry"][
                "points"
            ] = Fonctions_Multipolygon().points(
                self.data_pos[pos_commune]["geometry"]["coordinates"]
            )
            pos_parcelles_candidates = []
            for pos_parcelle in pos_communes_pos_parcelles[pos_commune][1]:
                tableau_parcelles[pos_parcelle]["geometry"][
                    "rectangle"
                ] = Fonctions_Multipolygon().rectangle(
                    tableau_parcelles[pos_parcelle]["geometry"]["coordinates"]
                )
                for point in self.data_pos[pos_commune]["geometry"]["points"]:
                    if tableau_parcelles[pos_parcelle]["geometry"][
                        "rectangle"
                    ].point_a_l_interieur_du_rectangle(point):
                        pos_parcelles_candidates.append(pos_parcelle)
                        break
            pos_communes_pos_parcelles[pos_commune][1] = pos_parcelles_candidates

        if config.passer_par_les_distances:
            for pos_commune in range(len(self.data_pos)):
                for pos_parcelle in pos_communes_pos_parcelles[pos_commune][1]:
                    tableau_parcelles[pos_parcelle]["geometry"][
                        "coordinates"
                    ] = Fonctions_Multipolygon().points(
                        tableau_parcelles[pos_parcelle]["geometry"]["coordinates"]
                    )
                    for coord in tableau_parcelles[pos_parcelle]["geometry"][
                        "coordinates"
                    ]:
                        if Fonctions_Points().coord_appartient_a_liste_coord(
                            coord, self.data_pos[pos_commune]["geometry"]["points"]
                        ):
                            tableau_id_commune_id_parcelles[pos_commune][1].append(
                                tableau_parcelles[pos_parcelle]["properties"]["id"]
                            )
                            break

        if config.passer_par_les_segments:
            for pos_commune in range(len(self.data_pos)):
                self.data_pos[pos_commune]["geometry"][
                    "coordinates"
                ] = Fonctions_Multipolygon().segments(
                    self.data_pos[pos_commune]["geometry"]["coordinates"]
                )
                for pos_parcelle in pos_communes_pos_parcelles[pos_commune][1]:
                    trouve = False
                    tableau_parcelles[pos_parcelle]["geometry"][
                        "coordinates"
                    ] = Fonctions_Multipolygon().segments(
                        tableau_parcelles[pos_parcelle]["geometry"]["coordinates"]
                    )
                    for segment1 in tableau_parcelles[pos_parcelle]["geometry"][
                        "coordinates"
                    ]:
                        for segment2 in self.data_pos[pos_commune]["geometry"][
                            "coordinates"
                        ]:
                            if segment1 == segment2:
                                tableau_id_commune_id_parcelles[pos_commune][1].append(
                                    tableau_parcelles[pos_parcelle]["properties"]["id"]
                                )
                                trouve = True
                                break
                        if trouve:
                            break

        if config.conserver_les_matchs_par_rectangles_uniquement:
            for pos_commune in range(len(self.data_pos)):
                for pos_parcelle in pos_communes_pos_parcelles[pos_commune][1]:
                    tableau_id_commune_id_parcelles[pos_commune][1].append(
                        tableau_parcelles[pos_parcelle]["properties"]["id"]
                    )

        self.data_pos = None
        self.liste_communes = None

        id_commune_id_parcelle = []
        for i in range(len(tableau_id_commune_id_parcelles)):
            for parcelle in tableau_id_commune_id_parcelles[i][1]:
                id_commune_id_parcelle.append(
                    [tableau_id_commune_id_parcelles[i][0], parcelle]
                )
            tableau_id_commune_id_parcelles[i] = None
        tableau_id_commune_id_parcelles = None
        return id_commune_id_parcelle
