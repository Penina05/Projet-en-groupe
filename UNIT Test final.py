# ============================================================
# TESTS UNITAIRES – Projet SED1515
# Auteur : Nadia
# ============================================================

import unittest

# Importation des fonctions à tester
from fonction_valeur_potentiometre_V2 import valeur_potentiometre
from inverse_kinematics import cinematics_inverse
from commande.commande import move_servos
from calibration import charger_calibration, appliquer_calibration
from pattern.shambala import shambala_pattern


class TestBrachiographe(unittest.TestCase):

 # --- TEST POTENTIOMÈTRES ---
    def test_valeur_potentiometre(self):
        x, y = valeur_potentiometre()
        self.assertIsInstance(x, (int, float))
        self.assertIsInstance(y, (int, float))
    
    # --- TEST CINÉMATIQUE INVERSE ---
    def test_cinematics_inverse(self):
        alpha, beta = cinematics_inverse(50, 50)  # point atteignable
        self.assertIsInstance(alpha, (int, float))
        self.assertIsInstance(beta, (int, float))

         # --- TEST CALIBRATION ---
    def test_charger_calibration(self):
        table = charger_calibration()
        self.assertIn("epaule", table)
        self.assertIn("coude", table)
        self.assertGreater(len(table["epaule"]), 0)
        self.assertGreater(len(table["coude"]), 0)

    def test_appliquer_calibration(self):
        table = charger_calibration()
        angle_e, angle_c = appliquer_calibration(90, 90, table)
        self.assertTrue(0 <= angle_e <= 180)
        self.assertTrue(0 <= angle_c <= 180)

    # --- TEST COMMANDE SERVOS ---
    def test_move_servos(self):
        try:
            move_servos(90, 90, stylo_on=False)
            ok = True
        except Exception:
            ok = False
        self.assertTrue(ok)

    # --- TEST PATTERN ---
    def test_shambala_pattern(self):
        points = shambala_pattern(
            radius_step=15, num_circles=2, points_per_circle=10,
            wave_amplitude=5, wave_frequency=12)
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)
        self.assertIsInstance(points[0], tuple)
        self.assertEqual(len(points[0]), 2)


if __name__ == "__main__":
    unittest.main()