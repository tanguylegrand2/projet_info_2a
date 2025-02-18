from abc import ABC


class ZoneGeographique(ABC):
    def __init__(self, id_commune):
        self.id_commune = id_commune

    def __get_id_commune__(self) -> str:
        return self.id_commune

    def __set_id_commune__(self, id_commune):
        self.id_commune = id_commune
