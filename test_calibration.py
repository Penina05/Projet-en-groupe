import unittest
from calibration import charger_calibration, interpoler, appliquer_calibration

class TestCalibration(unittest.TestCase):

    # --------------------------------------------------------
    # TESTS POUR interpoler()
    # --------------------------------------------------------

    def test_interpoler_exact_value(self):
        table = {0: 0, 90: 10, 180: 20}
        self.assertEqual(interpoler(90, table), 10)

    def test_interpoler_between_points(self):
        table = {0: 0, 100: 20}
        # À 50 → exact milieu → 10
        self.assertAlmostEqual(interpoler(50, table), 10)

    def test_interpoler_below_min(self):
        table = {10: 5, 20: 10}
        self.assertEqual(interpoler(0, table), 5)

    def test_interpoler_above_max(self):
        table = {10: 5, 20: 10}
        self.assertEqual(interpoler(200, table), 10)

    # --------------------------------------------------------
    # TESTS POUR appliquer_calibration()
    # --------------------------------------------------------

    def test_appliquer_calibration_basic(self):
        table = {
            "epaule": {0: 0, 180: 10},
            "coude":  {0: 0, 180: -10}
        }

        epaule_corr, coude_corr = appliquer_calibration(90, 90, table)

        # interpolation : epaule = 5, coude = -5
        self.assertAlmostEqual(epaule_corr, 95)
        self.assertAlmostEqual(coude_corr, 85)

    def test_appliquer_calibration_bounds(self):
        table = {
            "epaule": {0: 100, 180: 100},
            "coude":  {0: -100, 180: -100}
        }

        e, c = appliquer_calibration(10, 10, table)

        # 10 + 100 = 110 → dans les bornes
        self.assertEqual(e, 110)

        # 10 - 100 = -90 → ramené à 0
        self.assertEqual(c, 0)

    # --------------------------------------------------------
    # TESTS POUR charger_calibration()
    # --------------------------------------------------------

    def test_charger_calibration_valid_file(self):
        contenu = """
        0 0 0
        90 5 -3
        180 10 -6
        """

        with open("calibration_test.txt", "w") as f:
            f.write(contenu)

        table = charger_calibration("calibration_test.txt")

        self.assertIn(90.0, table["epaule"])
        self.assertEqual(table["epaule"][90.0], 5)
        self.assertEqual(table["coude"][90.0], -3)


if __name__ == "__main__":
    unittest.main()