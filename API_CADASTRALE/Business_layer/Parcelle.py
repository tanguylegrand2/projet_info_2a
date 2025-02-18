from Business_layer.zone_geo import ZoneGeographique
from DAO_layer import parcelle_dao


class Parcelle(ZoneGeographique):
    def __init__(self, id_parcelle: str, id_commune: str, liste_segments: list):
        self.id_parcelle = id_parcelle
        super().__init__(id_commune)
        self.liste_segments = liste_segments

    def __get_id_parcelle__(self) -> str:
        return self.id_parcelle

    def __get_liste_segments__(self) -> list:
        return self.liste_segments

    def __set_id_parcelle__(self, id_parcelle):
        self.id_parcelle = id_parcelle

    def __set_liste_segments__(self, liste_segments):
        self.liste_segments = liste_segments

    def get_parcelles_contigues(self):
        liste_parcelles_contigues = []
        for segment in self.__get_liste_segments__():
            for parcelle in parcelle_dao.ParcelleDAO().get_all_parcelle():
                if (
                    (segment in parcelle.__get_liste_segments__())
                    and (parcelle.__get_id_commune__() != self.__get_id_commune__())
                    and (parcelle not in liste_parcelles_contigues)
                ):
                    liste_parcelles_contigues.append(parcelle)
        return liste_parcelles_contigues

    def etreEnLimmite(self):
        estEnLimite = False
        for parcelle in self.get_parcelles_contigues():
            if self.__get_id_commune__() != parcelle.__get_id_commune__():
                estEnLimite = True
                return estEnLimite
        return estEnLimite
