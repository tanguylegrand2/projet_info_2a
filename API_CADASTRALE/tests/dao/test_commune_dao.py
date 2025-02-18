from unittest import TestCase
from DAO_layer.commune_dao import CommuneDAO


class testCommuneDao(TestCase):
    def test_get_all_commune(self):
        commune = CommuneDAO()
        communes = commune.get_all_commune(lim=5)

        self.assertEqual(5, len(communes))

    def test_get_commune_by_id_ok(self):
        commune = CommuneDAO()
        communes = commune.get_commune_by_id("41002")

        self.assertEqual("Rennes", communes)

    def test_get_commune_by_id_not_find(self):
        commune = CommuneDAO()
        communes = commune.get_commune_by_id("-41002")

        self.assertIsNone(communes)

    def test_insert_commune(self):
        commune = CommuneDAO()
        inserted = commune.insert_commune([["41001", "Bruz"], ["41002", "Rennes"]])

        self.assertTrue(inserted)
