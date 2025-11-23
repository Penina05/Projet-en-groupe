# ============================================================
# LECTURE DES POTENTIOMÈTRES → COORDONNÉES X_user, Y_user
# Projet SED1515 – Contrôle du Brachiographe
#
# Ce module :
#   1) Lit les valeurs analogiques des potentiomètres (ADC 16 bits)
#   2) Convertit ces valeurs en distances X_user et Y_user (mm)
#   3) Renvoie les coordonnées utilisables par la cinématique inverse
#
# Auteur : NIKE
# ============================================================

from machine import ADC, Pin

# ------------------------------------------------------------
# CONFIGURATION DES POTENTIOMÈTRES
# ------------------------------------------------------------
# Exemple de câblage :
#   - Potentiomètre X → GPIO 26 (ADC0)
#   - Potentiomètre Y → GPIO 27 (ADC1)
#
#  Important :
#   - Les potentiomètres doivent être alimentés en 3.3 V (compatible Pico).
#   - La masse (GND) doit être commune.
# ------------------------------------------------------------

pot_X = ADC(Pin(26))  # Potentiomètre pour X
pot_Y = ADC(Pin(27))  # Potentiomètre pour Y

# ------------------------------------------------------------
# PARAMÈTRES DU BRAS ROBOTISÉ
# ------------------------------------------------------------
L1 = 100   # Longueur segment épaule (mm)
L2 = 100   # Longueur segment avant-bras (mm)

# On suppose que la zone de travail est un carré de 200 mm × 200 mm
X_max = L1 + L2   # 200 mm
Y_max = L1 + L2   # 200 mm

# ------------------------------------------------------------
# FONCTION DE CONVERSION ADC → DISTANCE (mm)
# ------------------------------------------------------------
def adc_to_mm(adc_value, max_distance):
    """
    Convertit une valeur ADC (0–65535) en distance (mm).
    
    Paramètres :
        adc_value (int) : valeur brute ADC (0–65535)
        max_distance (float) : distance maximale en mm (200 mm)
    
    Retour :
        distance (float) : distance en mm
    """
    return (adc_value / 65535.0) * max_distance
