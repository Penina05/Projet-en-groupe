# CINEMATIQUE INVERSE 
# Ce module effectue :
# 1) La correction de la position réelle du bras 
# 2) Le calcul des angles mathématiques alpha (épaule) et beta (coude)
# 3) La conversion de ces angles en angles SERVOS, en tenant compte
#    de l’orientation réelle des servomoteurs.
# 4) La sécurisation des angles (entre 0° et 180°)

# Auteur : Penina Godeme

from fonction_valeur_potentiometre import adc_to_mm
import math


L1 = 100   # Longueur segment épaule
L2 = 100   # Longueur segment avant-bras

def cinematics_inverse(x_user, y_user):

    # Ajustement de l'origine (décalage mécanique)
    X = x_user + 50.0
    Y = y_user

    # Distance du point cible
    r2 = X**2 + Y**2
    r = math.sqrt(r2)

    # Vérification que le point est atteignable par le bras
    if r > L1 + L2 or r < abs(L1 - L2):
        raise ValueError("Point hors de la zone atteignable.")

    # Calcul de l’angle du coude avec la loi des cosinus
    cos_theta2 = (r2 - L1*2 - L2*2) / (2 * L1 * L2)
    cos_theta2 = max(-1.0, min(1.0, cos_theta2))  # Sécurité numérique
    theta2 = math.acos(cos_theta2)

    # Calcul de l’angle de l’épaule
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(Y, X) - math.atan2(k2, k1)

    # Conversion en degrés
    angle_epaule = math.degrees(theta1)
    angle_coude  = math.degrees(theta2)

    # Ajustements mécaniques et limites des servos
    servo_ep = max(0, min(180, angle_epaule + 90))
    servo_co = max(0, min(180, angle_coude))

    return servo_ep, servo_co



