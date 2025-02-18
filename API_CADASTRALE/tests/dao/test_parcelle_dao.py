from unittest import TestCase
from DAO_layer.parcelle_dao import ParcelleDAO


class testParcelleDao(TestCase):
    def test_get_all_parcelle(self):
        parcelle = ParcelleDAO()
        parcelles = parcelle.get_all_parcelle(lim=20)

        self.assertEqual(20, len(parcelles))

    def test_get_parcelles_contigue_commune_ok(self):
        parcelle = ParcelleDAO()
        parcelles = parcelle.get_parcelles_contigue_commune("41002")

        self.assertEqual(10, len(parcelles))

    def test_get_parcelles_contigue_commune_not_find(self):
        parcelle = ParcelleDAO()
        parcelles = parcelle.get_parcelles_contigue_commune("-41002")

        self.assertIsNone(parcelles)

    def test_insert_parcelle(self):
        parcelle = ParcelleDAO()
        inserted = parcelle.insert_parcelle(
            [["41001", "41001001"], ["41002", "41002058"]]
        )

        self.assertTrue(inserted)
