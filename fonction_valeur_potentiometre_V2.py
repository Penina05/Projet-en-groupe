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
#   Important :
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

# Zone de travail supposée : carré de 200 mm × 200 mm
X_max = L1 + L2   # 200 mm
Y_max = L1 + L2   # 200 mm

# ------------------------------------------------------------
# FONCTION DE CONVERSION ADC → DISTANCE (mm)
# ------------------------------------------------------------
def adc_to_mm(adc_value, max_distance):
    """
    Convertit une valeur ADC (0–65535) en distance (mm).
    """
    return (adc_value / 65535.0) * max_distance

# ------------------------------------------------------------
# FONCTION PRINCIPALE : valeur_potentiometre
# ------------------------------------------------------------
def valeur_potentiometre():
    """
    Lit les potentiomètres et renvoie les coordonnées X_user, Y_user en mm.
    
    Retour :
        (X_user, Y_user) : tuple de coordonnées en mm
    """
    # Lecture brute ADC (16 bits)
    adc_X = pot_X.read_u16()
    adc_Y = pot_Y.read_u16()
    
    # Conversion en distances (mm)
    X_user = adc_to_mm(adc_X, X_max)
    Y_user = adc_to_mm(adc_Y, Y_max)
    
    return X_user, Y_user
