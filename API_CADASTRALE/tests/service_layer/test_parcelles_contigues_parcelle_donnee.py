from unittest.case import TestCase
import unittest
from Service_layer.parcelles_contigues_parcelle_donnee import (
    Parcelles_contigues_parcelle_donnee,
)


class Test_Parcelles_contigues_parcelle_donnee(TestCase):
    def test(self):

        attendu = [
            "410090000A0211",
            "410090000A0218",
            "410090000A0047",
            "410090000A0068",
            "410090000A0046",
            "410350000E0025",
            "410090000A0036",
            "410350000E0022",
            "410570000B0291",
            "410570000B0290",
            "410570000B0289",
        ]
        obtenu = Parcelles_contigues_parcelle_donnee().applique("410090000A0048")
        self.assertTrue(attendu == obtenu)


if __name__ == "__main__":
    unittest.main()
