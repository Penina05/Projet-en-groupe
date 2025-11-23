import unittest

# ============================
# MOCKS pour remplacer machine.ADC et machine.Pin
# ============================
class MockADC:
    def __init__(self, pin, value=0):
        self.pin = pin
        self._value = value

    def read_u16(self):
        return self._value

    def set_value(self, v):
        self._value = v


class MockPin:
    def __init__(self, num):
        self.num = num


# ============================
# CODE SOURCE SIMPLIFIÉ (injecté avec mocks)
# ============================
L1 = 100
L2 = 100
X_max = L1 + L2   # 200 mm
Y_max = L1 + L2   # 200 mm

# Mocks pour les potentiomètres
pot_X = MockADC(MockPin(26))
pot_Y = MockADC(MockPin(27))

def adc_to_mm(adc_value, max_distance):
    return (adc_value / 65535.0) * max_distance

def valeur_potentiometre():
    adc_X = pot_X.read_u16()
    adc_Y = pot_Y.read_u16()
    X_user = adc_to_mm(adc_X, X_max)
    Y_user = adc_to_mm(adc_Y, Y_max)
    return X_user, Y_user


# ============================
# UNITTESTS COMMENTÉS
# ============================
class TestValeurPotentiometre(unittest.TestCase):

    # TEST 1 : valeurs ADC minimales (0 → 0 mm)
    def test_adc_min(self):
        pot_X.set_value(0)
        pot_Y.set_value(0)
        X, Y = valeur_potentiometre()
        self.assertEqual(X, 0.0)
        self.assertEqual(Y, 0.0)

    # TEST 2 : valeurs ADC maximales (65535 → 200 mm)
    def test_adc_max(self):
        pot_X.set_value(65535)
        pot_Y.set_value(65535)
        X, Y = valeur_potentiometre()
        self.assertAlmostEqual(X, 200.0, delta=0.1)
        self.assertAlmostEqual(Y, 200.0, delta=0.1)

    # TEST 3 : valeurs ADC milieu (32768 → ~100 mm)
    def test_adc_mid(self):
        pot_X.set_value(32768)
        pot_Y.set_value(32768)
        X, Y = valeur_potentiometre()
        self.assertAlmostEqual(X, 100.0, delta=1.0)
        self.assertAlmostEqual(Y, 100.0, delta=1.0)

    # TEST 4 : asymétrie X et Y
    def test_adc_asymmetry(self):
        pot_X.set_value(16384)   # ~25% → ~50 mm
        pot_Y.set_value(49152)   # ~75% → ~150 mm
        X, Y = valeur_potentiometre()
        self.assertAlmostEqual(X, 50.0, delta=1.0)
        self.assertAlmostEqual(Y, 150.0, delta=1.0)

    # TEST 5 : type de sortie
    def test_output_type(self):
        pot_X.set_value(10000)
        pot_Y.set_value(20000)
        X, Y = valeur_potentiometre()
        self.assertIsInstance(X, float)
        self.assertIsInstance(Y, float)


if __name__ == '__main__':
    unittest.main()