from unittest import TestCase
from DAO_layer.departement_dao import DepartementDAO


class testCommuneDao(TestCase):
    def test_get_all_departements(self):
        departement = DepartementDAO()
        departements = departement.get_all_departements()

        # self.assertEqual(5, len(com))

    def test_insert_departement(self):
        departement = DepartementDAO()
        inserted = departement.insert_departements(["41", "42", "43", "44"])

        self.assertTrue(inserted)
