from unittest import TestCase
from DAO_layer.commune_contigue_dao import CommuneContigueDAO


class testCommuneContigueDao(TestCase):
    def test_get_all_commune_contigue(self):
        commune = CommuneContigueDAO()
        communes = commune.get_all_commune_contigue(lim=10)

        self.assertEqual(5, len(communes))

    def test_get_commune_contigue_by_id_ok(self):
        commune = CommuneContigueDAO()
        communes = commune.get_commune_contigue_by_id("41002")

        self.assertEqual(5, len(communes))

    def test_get_commune_contigue_by_id_not_find(self):
        commune = CommuneContigueDAO()
        communes = commune.get_commune_contigue_by_id("-41002")

        self.assertIsNone(communes)

    def test_insert_commune_contigue(self):
        commune = CommuneContigueDAO()
        inserted = commune.insert_commune_contigue(
            [["41001", "41002"], ["41001", "41015"]]
        )

        self.assertTrue(inserted)
