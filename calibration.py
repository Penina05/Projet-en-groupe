# MODULE DE CALIBRATION – VERSION FINALE
# Ce module :
#   1) Charge une table d’erreurs de calibration (épaule + coude)
#   2) Interpole les corrections pour un angle donné
#   3) Applique la correction aux angles provenant de la cinématique inverse
#
# Auteur : Mariam Farota
# CHARGEMENT DE LA CALIBRATION

def charger_calibration(fichier="calibration.txt"):
    """
    Charge un fichier de calibration contenant :
        angle  erreur_epaule  erreur_coude

    Retour :
        {
            "epaule": {angle: erreur},
            "coude":  {angle: erreur}
        }
    Si le fichier n’existe pas → table simulée.
    """

    erreurs_epaule = {}
    erreurs_coude = {}

    try:
        with open(fichier, "r") as f:
            for ligne in f:
                if ligne.startswith("#") or ligne.strip() == "":
                    continue
                angle, err_e, err_c = map(float, ligne.split())
                erreurs_epaule[angle] = err_e
                erreurs_coude[angle] = err_c
        print("Calibration chargée :", fichier)
    except:
        # Table simulée si fichier absent
        print("⚠️ Aucun fichier de calibration trouvé — table simulée utilisée.")
        for a in range(0, 181, 10):
            erreurs_epaule[a] = 0.5 * (1 - a/180)
            erreurs_coude[a] = 0.4 * (1 - a/180)

    return {"epaule": erreurs_epaule, "coude": erreurs_coude}


# ------------------------------------------------------------
# INTERPOLATION LINÉAIRE
# ------------------------------------------------------------

def interpoler(angle, table):
    """Retourne la correction correspondante à un angle donné."""
    angles = sorted(table.keys())

    # Avant la borne minimum
    if angle <= angles[0]:
        return table[angles[0]]

    # Après la borne maximum
    if angle >= angles[-1]:
        return table[angles[-1]]

    # Interpolation linéaire
    for i in range(len(angles)-1):
        a0, a1 = angles[i], angles[i+1]
        if a0 <= angle <= a1:
            e0, e1 = table[a0], table[a1]
            # interpolation
            return e0 + (e1 - e0) * (angle - a0) / (a1 - a0)


# ------------------------------------------------------------
# FONCTION PRINCIPALE : appliquer_calibration()
# ------------------------------------------------------------

def appliquer_calibration(angle_epaule, angle_coude, table_erreurs):
    """
    Applique les corrections venant de la calibration.
    
    Entrées :
        angle_epaule, angle_coude : angles en degrés venant de la cinématique inverse
        table_erreurs : dictionnaire contenant les tables 'epaule' et 'coude'

    Sortie :
        (angle_epaule_corr, angle_coude_corr)
    """

    err_e = interpoler(angle_epaule, table_erreurs["epaule"])
    err_c = interpoler(angle_coude,  table_erreurs["coude"])

    angle_epaule_corr = angle_epaule + err_e
    angle_coude_corr  = angle_coude  + err_c

    # sécurisation
    angle_epaule_corr = max(0, min(180, angle_epaule_corr))
    angle_coude_corr  = max(0, min(180, angle_coude_corr))

    return angle_epaule_corr, angle_coude_corr