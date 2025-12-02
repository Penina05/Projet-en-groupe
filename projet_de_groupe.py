# Projet SED1515 - Brachiographe 
import math
import time
from machine import Pin, PWM, ADC
"""
Ce programme contrôle un bras robotique 2D composé de deux segments (épaule et coude)
et d’un stylo actionnable. 

Fonctionnalités principales :
- Lecture des potentiomètres pour récupérer une position (x, y) voulue par l’utilisateur.
- Conversion de cette position en angles de rotation pour les servomoteurs grâce à
  la cinématique inverse.
- Application d’une calibration (table d’erreurs corrigées par interpolation).
- Commande des servos PWM pour déplacer physiquement le bras.

Le programme permet de déplacer le bras en temps réel simplement en tournant deux
potentiomètres. Il utilise les notions essentielles de géométrie, PWM, cinématique
inverse et interpolation.
"""
# CONFIGURATION

# Servos
PIN_SERVO_EPAULE = 0
PIN_SERVO_COUDE  = 1
PIN_SERVO_STYLO  = 2

# Potentiomètres
PIN_POT_X = 26
PIN_POT_Y = 27

# Longueurs des segments du bras (mm)
L1 = 100.0
L2 = 100.0

# INITIALISATION SERVOS

servo_epaule = PWM(Pin(PIN_SERVO_EPAULE))
servo_coude  = PWM(Pin(PIN_SERVO_COUDE))
servo_stylo  = PWM(Pin(PIN_SERVO_STYLO))

servo_epaule.freq(50)
servo_coude.freq(50)
servo_stylo.freq(50)

# INITIALISATION POTENTIOMÈTRES

pot_X = ADC(Pin(PIN_POT_X))
pot_Y = ADC(Pin(PIN_POT_Y))

# CONVERSION ANGLE → PWM

def angle_to_pwm_duty(angle_deg):
    angle = max(0, min(180, float(angle_deg)))
    pulse_ms = 1.0 + (angle / 180.0)   # 1ms → 0°, 2ms → 180°
    return int((pulse_ms / 20.0) * 65535)

# COMMANDES SERVOS

def move_servos(a_epaule, a_coude, stylo_on=False):
    servo_epaule.duty_u16(angle_to_pwm_duty(a_epaule))
    servo_coude.duty_u16(angle_to_pwm_duty(a_coude))
    servo_stylo.duty_u16(angle_to_pwm_duty(90 if stylo_on else 0))

# CINÉMATIQUE INVERSE


def cinematics_inverse(x_user, y_user):
    X = x_user  # Décale l’origine vers le socle
    Y = y_user

    # Distance au point cible
    r2 = X**2 + Y**2  #Calcul du carré de la distance entre l’origine et le point cible.
    r = math.sqrt(r2)

    # Vérification de la portée
    if r > L1 + L2 or r < abs(L1 - L2):
        raise ValueError("Point hors de la zone atteignable.")

    # Calcul de l’angle du coude (theta2)
    cos_theta2 = (r2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = max(-1.0, min(1.0, cos_theta2)) 
    theta2 = math.acos(cos_theta2)  
    # Calcul de l’angle de l’épaule (theta1)
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(Y, X) - math.atan2(k2, k1)

    # Conversion en degrés servo
    angle_epaule = math.degrees(theta1)
    angle_coude  = math.degrees(theta2)

    # Mapping vers servos 
    servo_epaule = max(0, min(180, angle_epaule + 90))  # 0° robot → 90° servo
    servo_coude  = max(0, min(180, angle_coude))        # 0° robot → 0° servo

    return servo_epaule + 47, 168-servo_coude

# CALIBRATION

def charger_calibration(fichier="calibration.txt"):
    err_e, err_c = {}, {}
    try:
        with open(fichier, "r") as f:
            for line in f:
                if not line.strip() or line.startswith("#"):
                    continue
                a, e1, e2 = line.split()
                err_e[float(a)] = float(e1)
                err_c[float(a)] = float(e2)
        print("Calibration chargee.")
    except:
        print("Aucune calibration trouvee. Utilisation des valeurs defaut.")
        for a in range(0, 181, 10):
            err_e[a] = 0.5 * (1 - a/180)
            err_c[a] = 0.4 * (1 - a/180)

    return {"epaule": err_e, "coude": err_c}

def interpoler(angle, table):
    keys = sorted(table)
    if angle <= keys[0]: return table[keys[0]]
    if angle >= keys[-1]: return table[keys[-1]]
    for i in range(len(keys)-1):
        a0, a1 = keys[i], keys[i+1]
        if a0 <= angle <= a1:
            e0, e1 = table[a0], table[a1]
            return e0 + (e1 - e0) * (angle - a0) / (a1 - a0)
    return 0.0

def appliquer_calibration(a_ep, a_co, table):
    return (
        a_ep + interpoler(a_ep, table["epaule"]),
        a_co + interpoler(a_co, table["coude"])
    )

# POTENTIOMÈTRES → COORDONNÉES XY

X_max = L1 + L2
Y_max = L1 + L2

def adc_to_mm(raw, max_dist):
    return (raw / 65535.0) * max_dist

def valeur_potentiometre():
    return (
        adc_to_mm(pot_X.read_u16(), X_max),
        adc_to_mm(pot_Y.read_u16(), Y_max)
    )

# BOUCLE PRINCIPALE


def main():
    print("Tournez les potentiometres pour deplacer le bras.")
    print("CTRL-C pour arreter.\n")

    table = charger_calibration()

    while True:
        try:
            x, y = valeur_potentiometre()

            try:
                a_ep, a_co = cinematics_inverse(x, y)
            except:
                continue

            a_ep, a_co = appliquer_calibration(a_ep, a_co, table)
            move_servos(a_ep, a_co, stylo_on=False)

            time.sleep(0.03)

        except KeyboardInterrupt:
            print("\nArret du programme.")
            break



if __name__ == "__main__":
    main()