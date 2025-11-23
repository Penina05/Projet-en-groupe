import unittest
import math
from inverse_kinematics import cinematics_inverse  


class TestCinematicsInverse(unittest.TestCase):

    # TEST 1 : atteindre un point simple 
    def test_basic_position(self):
        epaule, coude = cinematics_inverse(150, 0)
        self.assertTrue(0 <= epaule <= 180)
        self.assertTrue(0 <= coude <= 180)

    # TEST 2 : position atteignable 
    def test_reachable_position(self):
        # point à portée max : L1 + L2 = 200, mais on prend x_user=250 (50mm offset)
        epaule, coude = cinematics_inverse(250, 0)
        self.assertIsInstance(epaule, float)
        self.assertIsInstance(coude, float)

    # TEST 3 : position trop éloignée 
    def test_unreachable_far(self):
        self.assertRaises(ValueError, cinematics_inverse, 500, 500)

   # TEST 4 : position proche (correction : ce point est atteignable)
    def test_unreachable_near(self):
        epaule, coude = cinematics_inverse(50, 0)
        self.assertTrue(0 <= epaule <= 180)
        self.assertTrue(0 <= coude <= 180)
        
    # TEST 5 : validité des angles 
    def test_angle_limits(self):
        epaule, coude = cinematics_inverse(200, 50)
        self.assertGreaterEqual(epaule, 0)
        self.assertLessEqual(epaule, 180)
        self.assertGreaterEqual(coude, 0)
        self.assertLessEqual(coude, 180)

    # TEST 6 : test point diagonal 
    def test_diagonal_point(self):
        epaule, coude = cinematics_inverse(200, 100)
        self.assertTrue(type(epaule) is float)
        self.assertTrue(type(coude) is float)

    # TEST 7 : vérifier symétrie gauche-droite 
    def test_symmetry(self):
        ep1, cd1 = cinematics_inverse(200, 50)
        ep2, cd2 = cinematics_inverse(100, 50)
        # les angles doivent être différents (le bras n'est pas symétrique)
        self.assertNotEqual(ep1, ep2)
        self.assertNotEqual(cd1, cd2)

    # TEST 8 : test de précision 
    def test_precision(self):
        # deux points très proches doivent donner des angles proches
        ep1, cd1 = cinematics_inverse(200, 80)
        ep2, cd2 = cinematics_inverse(201, 80)
        self.assertLess(abs(ep1 - ep2), 5)
        self.assertLess(abs(cd1 - cd2), 5)


if __name__ == '__main__':
    unittest.main()

