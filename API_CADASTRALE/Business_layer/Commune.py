from logging import raiseExceptions
from Business_layer.figure_geometrique.rectangle import Rectangle
from Business_layer.fonctions.fonctions_multipolygon import Fonctions_Multipolygon
from DAO_layer import commune_contigue_dao, parcelle_dao
from Business_layer.zone_geo import ZoneGeographique


class Commune(ZoneGeographique):
    def __init__(
        self,
        id_commune: str,
        nom_commune: str = None,
        pos: int = None,
        multipolygon: list = None,
        oblong_only: bool = True,
    ):
        super().__init__(id_commune)
        self.nom_commune = nom_commune
        self.pos = pos
        if oblong_only == False and multipolygon != None:
            self.segments = Fonctions_Multipolygon().segments(multipolygon)
            self.rectangle = Fonctions_Multipolygon().rectangle(multipolygon)
        elif oblong_only == True and multipolygon != None:
            self.segments = None
            self.rectangle = Fonctions_Multipolygon().rectangle(multipolygon)
        else:
            self.segments = None
            self.rectangle = None

    def __eq__(self, autre_commune) -> bool:
        return self.id_commune == autre_commune.id_commune

    def __str__(self):
        return "id: {}, nom: {}, rectangle: point1={}, point2={}".format(
            self.id_commune,
            self.nom_commune,
            self.rectangle.__get_point1__(),
            self.rectangle.__get_point2__(),
        )

    def __get_nom_commune__(self) -> str:
        return self.nom_commune

    def __get_pos__(self) -> int:
        return self.pos

    def __get_rectangle__(self) -> Rectangle:
        return self.rectangle

    def __get_segments__(self) -> list:
        return self.segments

    def __set_nom_commune__(self, nom_commune: str):
        self.nom_commune = nom_commune

    def __set_pos__(self, pos: int):
        self.pos = pos

    def __set_rectangle__(self, rectangle: Rectangle):
        self.rectangle = rectangle

    def __set_segments__(self, segments):
        self.segments = segments

    def rectangles_des_communes_se_recoupent(self, autre_commune):
        try:
            return self.__get_rectangle__().se_recoupent(
                autre_commune.__get_rectangle__()
            )
        except:
            raiseExceptions(
                "module commune, fonction rectangles_des_communes_se_recoupent: Les rectangles semblent ne pas être définis."
            )

    def departement(self):
        return list(self.id_commune)[0] + list(self.id_commune)[1]

    def avoirDesParcellesContigues(self):
        return (
            len(
                commune_contigue_dao.CommuneContigueDAO().get_commune_contigue_by_id(
                    self.__get_id_commune__
                )
            )
            > 0
        )

    def get_parcelles_de_la_commune(self):
        liste_parcelles = []
        for parcelle in parcelle_dao.ParcelleDAO().get_all_parcelle():
            if parcelle.__get_id_commune__() == self.__get_id_commune__():
                liste_parcelles.append(parcelle)
        return liste_parcelles

    def get_parcelles_en_bordure(self):
        liste_parcelles_bordure = []
        if self.avoirDesParcellesContigues():
            for parcelle in self.get_parcelles_de_la_commune():
                if parcelle.etreEnLimite():
                    liste_parcelles_bordure.append(parcelle)
        return liste_parcelles_bordure
