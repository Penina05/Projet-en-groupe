import math
import time

# =========================
# 1️⃣ Génération du pattern
# =========================
def shambala_pattern(radius_step=10, num_circles=5, points_per_circle=100, wave_amplitude=5, wave_frequency=6):
    points = []
    for n in range(1, num_circles + 1):
        radius = n * radius_step
        for i in range(points_per_circle):
            theta = 2 * math.pi * i / points_per_circle
            r = radius + wave_amplitude * math.sin(wave_frequency * theta)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
    return points

# =========================
# 2️⃣ Cinématique inverse
# =========================
def cinematique_inverse(x, y, L1=10, L2=10):
    D = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(D) > 1:
        return None, None  # point hors de portée
    theta2 = math.atan2(math.sqrt(1 - D**2), D)
    theta1 = math.atan2(y, x) - math.atan2(L2*math.sin(theta2), L1 + L2*math.cos(theta2))
    return math.degrees(theta1), math.degrees(theta2)

# =========================
# 3️⃣ Initialisation servos
# =========================
# Exemple générique : à remplacer par ta librairie
class Servo:
    def __init__(self, name):
        self.name = name
        self.angle = 0
    def write(self, angle):
        self.angle = angle
        print(f"{self.name} -> angle: {angle:.1f}°")  # simule le servo

servo_epaule = Servo("Epaule")
servo_coude = Servo("Coude")

# =========================
# 4️⃣ Exécution du pattern
# =========================
pattern_points = shambala_pattern(radius_step=15, num_circles=6, points_per_circle=200,
                                  wave_amplitude=5, wave_frequency=12)

for (x, y) in pattern_points:
    angle_epaule, angle_coude = cinematique_inverse(x, y, L1=10, L2=10)
    if angle_epaule is not None:
        servo_epaule.write(angle_epaule)
        servo_coude.write(angle_coude)
        time.sleep(0.05)  # contrôle de la vitesse du crayon

print("Pattern terminé !")
