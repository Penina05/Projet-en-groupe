# CINEMATIQUE INVERSE 
# Projet SED1515 – Contrôle du Brachiographe
# Ce module effectue :
# 1) La correction de la position réelle du bras (base à -50 mm)
# 2) Le calcul des angles mathématiques alpha (épaule) et beta (coude)
#    selon les équations officielles du LAB 8.
# 3) La conversion de ces angles en angles SERVOS, en tenant compte
#    de l’orientation réelle des servomoteurs.
# 4) La sécurisation des angles (entre 0° et 180°)

# Auteur : Penina Godeme

from fonction_valeur_potentiometre import adc_to_mm
import math

# Longueurs du bras (mm) utilisées dans le LAB 8
L1 = 100   # Longueur segment épaule
L2 = 100   # Longueur segment avant-bras

# ------------------------------------------------------------
#              FONCTION DE CINÉMATIQUE INVERSE
# ------------------------------------------------------------
def cinematics_inverse(x_user, y_user):
    """
    Calcule les angles des servomoteurs pour atteindre la position (x_user, y_user)
    en suivant les équations EXACTES du Lab 8.

    Entrées :
        x_user, y_user : Coordonnées cibles venant des potentiomètres

    Sorties :
        servo_epaule, servo_coude (en degrés)
    """

    # ---------------------------------------------
    # 1) Correction de la position de la base (Lab 8)
    # ---------------------------------------------
    # Le point (0,0) du papier n'est pas où se trouve la base du bras.
    # Le LAB 8 impose : base située 50 mm à gauche → X_real = X_user - 50.
    X = x_user - 50
    Y = y_user

    # ---------------------------------------------
    # 2) Vérification que la cible est atteignable
    # ---------------------------------------------
    distance = math.sqrt(X**2 + Y**2)

    if distance > (L1 + L2):
        raise ValueError("Position trop éloignée : le bras ne peut pas l’atteindre.")

    if distance < abs(L1 - L2):
        raise ValueError("Position trop proche : géométrie impossible.")

    # ---------------------------------------------
    # 3) Calcul de l’angle β (coude) – FORMULE LAB 8
    # ---------------------------------------------
    cos_beta = (X**2 + Y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_beta = max(min(cos_beta, 1), -1)  # éviter erreurs numériques

    # ⬇⬇ FORMULE OBLIGATOIRE DU LAB 8 ⬇⬇
    beta_math = math.pi - math.acos(cos_beta)

    # ---------------------------------------------
    # 4) Calcul de l’angle α (épaule) – FORMULE LAB 8
    # ---------------------------------------------
    alpha_math = math.atan2(Y, X) - math.atan2(
        L2 * math.sin(beta_math),
        L1 + L2 * math.cos(beta_math)
    )

    # Convertir en degrés
    alpha_deg = math.degrees(alpha_math)
    beta_deg  = math.degrees(beta_math)

    # ---------------------------------------------
    # 5) Conversion angles math → angles SERVOS
    #    (offsets imposés par le montage réel)
    #
    # Le Lab 8 impose :
    #    servo_epaule = 90° - alpha_deg
    #    servo_coude  = beta_deg - 90°
    # ---------------------------------------------
    servo_epaule = 90 - alpha_deg
    servo_coude  = beta_deg - 90

    # 6) Sécurisation des angles (0° → 180°)
    #---------------------------------------------
    servo_epaule = float(max(0, min(180, servo_epaule)))
    servo_coude  = float(max(0, min(180, servo_coude)))

    return servo_epaule, servo_coude



