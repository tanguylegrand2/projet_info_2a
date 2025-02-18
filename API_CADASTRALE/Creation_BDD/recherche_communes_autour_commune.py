from logging import raiseExceptions
from Business_layer.Commune import Commune
from Business_layer.fonctions.fonctions_multipolygon import Fonctions_Multipolygon
from Business_layer.fonctions.fonctions_points import Fonctions_Points
from Client_layer.telechargement import Telechargement
import config


class Recherche_communes_autour_commune:
    def __init__(self, chemin_local: str, id_commune: str, date: str = "latest"):
        self.chemin_local = chemin_local
        self.date = date
        self.id_commune = id_commune

    def applique(self):

        data = Telechargement().telecharge_communes(self.chemin_local, self.date)
        communes = []
        for i in range(len(data)):
            communes.append(
                Commune(
                    id_commune=data[i]["properties"]["id"],
                    pos=i,
                    multipolygon=data[i]["geometry"]["coordinates"],
                    oblong_only=True,
                )
            )
        matchs = []
        for commune1 in communes:
            if commune1.__get_id_commune__() == self.id_commune:
                matchs.append([commune1.__get_pos__(), []])
                for commune2 in communes:
                    if (
                        commune1.rectangles_des_communes_se_recoupent(commune2)
                        and commune1 != commune2
                    ):
                        matchs[-1][1].append(commune2.__get_pos__())

        liste_pos = []
        for ligne in matchs:
            liste_pos.append(ligne[0])
            for id in ligne[1]:
                liste_pos.append(id)
        liste_pos = list(set(liste_pos))

        if config.passer_par_les_distances:
            for pos in liste_pos:
                data[pos]["geometry"]["coordinates"] = Fonctions_Multipolygon().points(
                    data[pos]["geometry"]["coordinates"]
                )
            for ligne in matchs:
                voisins = []
                for pos in ligne[1]:
                    for coord in data[pos]["geometry"]["coordinates"]:
                        if Fonctions_Points().coord_appartient_a_liste_coord(
                            coord, data[ligne[0]]["geometry"]["coordinates"]
                        ):
                            voisins.append(pos)
                            break
                ligne[1] = voisins

        if config.passer_par_les_segments:
            for pos in liste_pos:
                data[pos]["geometry"][
                    "coordinates"
                ] = Fonctions_Multipolygon().segments(
                    data[pos]["geometry"]["coordinates"]
                )
            for ligne in matchs:
                voisins = []
                for pos in ligne[1]:
                    Trouve = False
                    for segment in data[ligne[0]]["geometry"]["coordinates"]:
                        for segment2 in data[pos]["geometry"]["coordinates"]:
                            if segment == segment2:
                                voisins.append(pos)
                                Trouve = True
                                break
                        if Trouve:
                            break
                    ligne[1] = voisins

        if config.conserver_les_matchs_par_rectangles_uniquement:
            pass

        for i in range(len(matchs)):
            id_com1 = matchs[i][0]
            matchs[i][0] = data[id_com1]["properties"]["id"]
            for j in range(len(matchs[i][1])):
                id_com2 = matchs[i][1][j]
                matchs[i][1][j] = data[id_com2]["properties"]["id"]
        communes_adj = []
        for ligne in matchs:
            for id_commune in ligne[1]:
                if [ligne[0], id_commune] not in communes_adj and [
                    id_commune,
                    ligne[0],
                ] not in communes_adj:
                    communes_adj.append([ligne[0], id_commune])
        table_id_nom = []
        for pos in liste_pos:
            table_id_nom.append(
                [data[pos]["properties"]["id"], data[pos]["properties"]["nom"]]
            )
        return (communes_adj, table_id_nom)
