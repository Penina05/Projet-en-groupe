# ============================================================
# COMMANDE DES SERVOMOTEURS – VERSION DE BASE
# Projet SED1515 – Contrôle du Brachiographe
#
# Ce module :
# 1) Reçoit les angles calculés par la cinématique inverse
# 2) Convertit les angles en signaux PWM (1ms → 0°, 2ms → 180°)
# 3) Envoie les signaux aux servomoteurs (épaule, coude, stylo)
#
# Auteur : NIKE
# ============================================================

from machine import Pin, PWM
import time

# ------------------------------------------------------------
# CONFIGURATION DES SERVOS
# ------------------------------------------------------------
# Exemple : GPIO 0 → épaule, GPIO 1 → coude, GPIO 2 → stylo
servo_epaule = PWM(Pin(0))
servo_coude  = PWM(Pin(1))
servo_stylo  = PWM(Pin(2))

# Fréquence PWM = 50 Hz (période = 20 ms)
servo_epaule.freq(50)
servo_coude.freq(50)
servo_stylo.freq(50)

# ------------------------------------------------------------
# FONCTION DE CONVERSION ANGLE → SIGNAL PWM
# ------------------------------------------------------------
def angle_to_pwm(angle):
    """
    Convertit un angle (0° → 180°) en rapport cyclique PWM.
    0°  = 1 ms ON
    90° = 1.5 ms ON
    180°= 2 ms ON
    """
    # Durée ON en ms
    pulse_ms = 1 + (angle / 180.0) * 1.0  # entre 1 ms et 2 ms

    # Conversion en rapport cyclique (duty_u16)
    duty = int((pulse_ms / 20.0) * 65535)  # période = 20 ms
    return duty

# ------------------------------------------------------------
# FONCTION DE COMMANDE DES SERVOS
# ------------------------------------------------------------
def move_servos(angle_epaule, angle_coude, stylo_on=False):
    # Épaule
    servo_epaule.duty_u16(angle_to_pwm(angle_epaule))
    # Coude
    servo_coude.duty_u16(angle_to_pwm(angle_coude))
    # Stylo (interrupteur : ON = appuyé, OFF = relevé)
    if stylo_on:
        servo_stylo.duty_u16(angle_to_pwm(90))   # exemple : 90° = appuyé
    else:
        servo_stylo.duty_u16(angle_to_pwm(0))    # exemple : 0° = relevé
    return None
