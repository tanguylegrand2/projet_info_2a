from Business_layer.Parcelle import Parcelle


class PermisDeConstruire:
    """La classe PermisDeConstruire permet de donner des indications sur les permis de constuire.
    Cette classe va permettre d'implémenter la méthode contigue() de la classe Parcelle et est construite
    pour répondre aux questions optionnels du sujet.

    Attributes :
    ___________

    description : str
        décrit le périmètre du permis de construire
    id_commune : str
        identifiant de la commune sur laquelle est déposée le permis de construire
    id_permis : str
        identifiant des permis de construire.
    liste_parcelles : list
        Liste de parcelles
    """

    def __init__(self, description, id_commune, id_permis, liste_parcelles):
        """Constructeur de la classe PermisDeConstruire.
        Parameters :
        ____________
        description_permis : str
            décrit le périmètre concernant le permis
        id_commune : str
            identifiant de la commune sur laquelle est déposée le permis de construire
        id_permis : str
            identifiant des permis de construire.
        liste_parcelles : list
            Liste de parcelles
        """
        self.description = description
        self.id_commune = id_commune
        self.id_permis = id_permis
        self.liste_parcelles = liste_parcelles

    def __get_description__(self) -> str:
        """Permet de retourner la description d'un permis de construire"""
        return self.description

    def __get_id_permis__(self) -> str:
        """Permet de retourner l'identifiaint d'un permis de construire"""
        return self.id_permis

    def __get_id_commune__(self) -> str:
        """Permet de retourner l'identifiaint de la commune du permis de construire"""
        return self.id_commune

    def __get_liste_parcelles__(self) -> list:
        """Permet de retourner la liste de parcelles"""
        return self.liste_parcelles

    def __set_description__(self, description):
        """Permet de redéfinir la description d'un permis de construire"""
        self.description = description

    def __set_id_commune__(self, id_commune):
        """Permet de redéfinir l'idifiant de la commune d'un permis de construire"""
        self.id_commune = id_commune

    def __set_id_permis__(self, id_permis):
        """Permet de redéfinir l'identifiant un permis de construire"""
        self.id_permis = id_permis

    def __set_liste_parcelles__(self, liste_parcelles):
        """Permet de redéfinir une liste de parcelles"""
        self.liste_parcelles = liste_parcelles

    def etreIdentique(self, permis):
        if self.__eq__(permis):
            return True
        else:
            for parcelle in permis.__get_liste_parcelles():
                if Parcelle.etreEnLimmite(parcelle):
                    if Parcelle.__get_id_commune__() != self.__get_id_commune__():
                        for self_parcelle in self.__get_liste_parcelles__():
                            for segment in parcelle.__get_liste_segments__():
                                if segment in self_parcelle.__get_liste_segments__():
                                    if (
                                        self.__get_description__()
                                        == permis.__get_description__()
                                    ):
                                        return True
        return False

    def __eq__(self, permis):
        """Savoir si deux permis sont les mêmes"""
        return self.__get_id_permis__() == permis.__get_id_permis__()
