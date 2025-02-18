from unittest import TestCase
from DAO_layer.annee_dao import AnneeDAO


class testAnneeDao(TestCase):
    def test_get_annee(self):
        annee = AnneeDAO()
        annee_base = annee.get_annee()

        self.assertEqual("latest", annee_base)
