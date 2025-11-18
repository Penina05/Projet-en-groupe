# Ce programme permet de :
# 1) Calculer les angles de la cinematique inverse (epaule et coude)
# 2) Lire un fichier de calibration contenant les erreurs des servos
# 3) Appliquer les corrections avant d'envoyer les angles corriges

import math

# Fonction : CINEMATIQUE INVERSE
def cinematics_inverse(x, y, L1=100, L2=100):
    cos_beta = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_beta = max(min(cos_beta, 1), -1)  # eviter les erreurs numeriques
    
    beta = math.acos(cos_beta)
    alpha = math.atan2(y, x) - math.atan2(L2 * math.sin(beta), L1 + L2 * math.cos(beta))
    
    alpha_deg = math.degrees(alpha)
    beta_deg = math.degrees(beta)
    
    return alpha_deg, beta_deg

# Fonction : CHARGEMENT DE LA CALIBRATION
def calibration_configuration(fichier):
    erreurs_epaule = {}
    erreurs_coude = {}
    
    try:
        with open(fichier, 'r') as f:
            for ligne in f:
                if ligne.startswith('#') or ligne.strip() == "":
                    continue
                angle, err_e, err_c = map(float, ligne.split())
                erreurs_epaule[angle] = err_e
                erreurs_coude[angle] = err_c
                
        print(f"Donnees de calibration chargees depuis {fichier}")
    except FileNotFoundError:
        print(f"Fichier {fichier} non trouve, utilisation de valeurs simulees.")
        for a in range(0, 181, 10):
            erreurs_epaule[a] = max(0, 6 - 0.03 * a)
            erreurs_coude[a] = max(0, 5 - 0.025 * a)
    
    return {"epaule": erreurs_epaule, "coude": erreurs_coude}

# Fonction : INTERPOLATION DES ERREURS
def interpoler(angle, table):
    angles = sorted(table.keys())
    
    if angle <= angles[0]:
        return table[angles[0]]
    if angle >= angles[-1]:
        return table[angles[-1]]
    
    for i in range(len(angles) - 1):
        if angles[i] <= angle <= angles[i + 1]:
            x0, x1 = angles[i], angles[i + 1]
            y0, y1 = table[x0], table[x1]
            return y0 + (y1 - y0) * (angle - x0) / (x1 - x0)

# Fonction : ENVOYER LES ANGLES COMPENSES
def envoyer_angles_compenses(angle_epaule, angle_coude, table_erreurs):
    erreur_epaule = interpoler(angle_epaule, table_erreurs["epaule"])
    erreur_coude = interpoler(angle_coude, table_erreurs["coude"])
    
    angle_epaule_corrige = angle_epaule + erreur_epaule
    angle_coude_corrige = angle_coude + erreur_coude
    
    print("\n--- Envoi des angles corriges ---")
    print(f"Angle epaule demande : {angle_epaule:.2f}, corrige : {angle_epaule_corrige:.2f}")
    print(f"Angle coude demande  : {angle_coude:.2f}, corrige : {angle_coude_corrige:.2f}")
    
    return angle_epaule_corrige, angle_coude_corrige