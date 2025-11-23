import unittest

# ============================
# MOCKS pour remplacer machine.Pin et machine.PWM
# ============================
class MockPWM:
    def __init__(self, pin):
        self.pin = pin
        self.freq_value = None
        self.duty_value = None

    def freq(self, f):
        self.freq_value = f

    def duty_u16(self, duty):
        self.duty_value = duty


class MockPin:
    def __init__(self, num):
        self.num = num


# ============================
# CODE SOURCE SIMPLIFIÉ (injecté avec mocks)
# ============================
servo_epaule = MockPWM(MockPin(0))
servo_coude  = MockPWM(MockPin(1))
servo_stylo  = MockPWM(MockPin(2))

servo_epaule.freq(50)
servo_coude.freq(50)
servo_stylo.freq(50)

def angle_to_pwm(angle):
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    pulse_ms = 1 + (angle / 180.0) * 1.0
    duty = int((pulse_ms / 20.0) * 65535)
    return duty

def move_servos(angle_epaule, angle_coude, stylo_on=False):
    servo_epaule.duty_u16(angle_to_pwm(angle_epaule))
    servo_coude.duty_u16(angle_to_pwm(angle_coude))
    if stylo_on:
        servo_stylo.duty_u16(angle_to_pwm(90))
    else:
        servo_stylo.duty_u16(angle_to_pwm(0))


# ============================
# UNITTESTS
# ============================
class TestMotorControl(unittest.TestCase):

    # TEST 1 : conversion angle 0°
    def test_angle_zero(self):
        duty = angle_to_pwm(0)
        expected = int((1/20)*65535)
        self.assertAlmostEqual(duty, expected, delta=100)

    # TEST 2 : conversion angle 90°
    def test_angle_mid(self):
        duty = angle_to_pwm(90)
        expected = int((1.5/20)*65535)
        self.assertAlmostEqual(duty, expected, delta=100)

    # TEST 3 : conversion angle 180°
    def test_angle_max(self):
        duty = angle_to_pwm(180)
        expected = int((2/20)*65535)
        self.assertAlmostEqual(duty, expected, delta=100)

    # TEST 4 : angle négatif saturé
    def test_angle_negative(self):
        duty = angle_to_pwm(-10)
        duty_zero = angle_to_pwm(0)
        self.assertEqual(duty, duty_zero)

    # TEST 5 : angle > 180 saturé
    def test_angle_overflow(self):
        duty = angle_to_pwm(200)
        duty_max = angle_to_pwm(180)
        self.assertEqual(duty, duty_max)

    # TEST 6 : move_servos avec stylo relevé
    def test_move_servos_up(self):
        move_servos(90, 90, stylo_on=False)
        self.assertEqual(servo_epaule.duty_value, angle_to_pwm(90))
        self.assertEqual(servo_coude.duty_value, angle_to_pwm(90))
        self.assertEqual(servo_stylo.duty_value, angle_to_pwm(0))

    # TEST 7 : move_servos avec stylo appuyé
    def test_move_servos_down(self):
        move_servos(90, 90, stylo_on=True)
        self.assertEqual(servo_epaule.duty_value, angle_to_pwm(90))
        self.assertEqual(servo_coude.duty_value, angle_to_pwm(90))
        self.assertEqual(servo_stylo.duty_value, angle_to_pwm(90))


if __name__ == '__main__':
    unittest.main()