from unittest.case import TestCase
import unittest
from Business_layer.figure_geometrique.rectangle import Rectangle


class TestRectangle(TestCase):
    def test(self):
        # given
        rec1 = Rectangle([2, 2], [20, 20])
        rec2 = Rectangle([1, 1], [10, 10])

        # when
        d = rec1.se_recoupent(rec2)

        # Then
        self.assertTrue(d)


if __name__ == "__main__":
    unittest.main()
