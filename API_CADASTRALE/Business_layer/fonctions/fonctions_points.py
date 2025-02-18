from Business_layer.figure_geometrique.rectangle import Rectangle
import math
import config


class Fonctions_Points:
    def rectangle(self, points):
        x_list = [points[i][0] for i in range(len(points))]
        y_list = [points[i][1] for i in range(len(points))]
        xmin = min(x_list)
        xmax = max(x_list)
        ymin = min(y_list)
        ymax = max(y_list)
        return Rectangle([xmin, ymin], [xmax, ymax])

    def match(self, points1, points2):
        for pts1 in points1:
            for pts2 in points2:
                if pts1 == pts2:
                    return True
        return False

    def distance(self, point1, point2):
        """cette fonction a pour but de prendre deux coordonnées toutes deux sous forme
        de liste [latitude,longitude] et de renvoyer la distance qui sépare ces deux points.

        Remarque: Ce calcul fonctionne également pour de longues distances car il prend en compte la
        courbure de la terre.

        Attributes
        ----------
        point1 : list[float,float]
            La première coordonnée (latitude,longitude)

        point2 : list[float,float]
            La première coordonnée (latitude,longitude)

        Returns
        -------
        distance : float
            La distance séparant les deux points

        Examples
        --------
        >>> distance([1.047,8.021],[2.011,7.103])
        147510.09712353753
        """
        long1 = point1[0] * (math.pi / 180)
        lat1 = point1[1] * (math.pi / 180)
        long2 = point2[0] * (math.pi / 180)
        lat2 = point2[1] * (math.pi / 180)
        if long1 == long2 and lat1 == lat2:
            return 0
        Rt = 6378137
        d = math.acos(
            math.sin(lat1) * math.sin(lat2)
            + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)
        )
        return Rt * d

    def coord_appartient_a_liste_coord(self, coord, liste_coord):
        for coordonnee in liste_coord:
            if self.distance(coord, coordonnee) <= config.seuil:
                return True
        return False
