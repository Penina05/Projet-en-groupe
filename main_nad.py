# ============================================================
# PROGRAMME PRINCIPAL – VERSION FINALE
# Projet SED1515 – Contrôle du Brachiographe
#
# Ce module propose un menu interactif permettant :
# 1) Lecture des potentiomètres
# 2) Calcul et mouvement via cinématique inverse
# 3) Commande directe des servos
# 4) Vérification de la calibration
# 5) Exécution d’un pattern prédéfini
# q) Quitter le programme

# Auteur : Nadia
# ============================================================

#  Importation des modules spécialisés 
from fonction_valeur_potentiometre_V2 import valeur_potentiometre
from inverse_kinematics import cinematics_inverse
from commande_servomoteur import move_servos
from calibration import charger_calibration, appliquer_calibration
from pattern.shambala import shambala_pattern

import time


def main():
    print("=== PROGRAMME PRINCIPAL ===")
    print("Options disponibles :")
    print("  1 : Lecture des potentiomètres")
    print("  2 : Cinématique inverse (calcul et mouvement)")
    print("  3 : Commande directe des servos")
    print("  4 : Vérification de la calibration")
    print("  5 : Exécution d’un pattern (Shambala)")
    print("  q : Quitter")
    print("----------------------------")

    # Charger la calibration une fois au démarrage
    table_erreurs = charger_calibration()

    while True:
        choix = input("Choix : ").strip()

        # OPTION 1 : Lecture des potentiomètres
        if choix == "1":
            X_user, Y_user = valeur_potentiometre()
            print(f"Lecture potentiomètres → X={X_user:.1f} mm | Y={Y_user:.1f} mm")

        # OPTION 2 : Cinématique inverse
        elif choix == "2":
            try:
                x = float(input("Entrez x (mm) : "))
                y = float(input("Entrez y (mm) : "))
                alpha, beta = cinematics_inverse(x, y)
                # Appliquer la calibration
                alpha_corr, beta_corr = appliquer_calibration(alpha, beta, table_erreurs)
                move_servos(alpha_corr, beta_corr, stylo_on=True)
                print(f"Cinématique inverse → Épaule={alpha_corr:.1f}° | Coude={beta_corr:.1f}°")
                time.sleep(2)
                move_servos(alpha_corr, beta_corr, stylo_on=False)
            except Exception as e:
                print("Erreur lors du calcul ou du mouvement :", e)

        # OPTION 3 : Commande directe des servos
        elif choix == "3":
            try:
                angle_epaule = float(input("Angle épaule (0–180°) : "))
                angle_coude  = float(input("Angle coude (0–180°) : "))
                stylo_state  = input("Stylo (on/off) : ").strip().lower() == "on"
                # Appliquer la calibration
                angle_epaule_corr, angle_coude_corr = appliquer_calibration(angle_epaule, angle_coude, table_erreurs)
                move_servos(angle_epaule_corr, angle_coude_corr, stylo_on=stylo_state)
                print("Commande envoyée aux servos (corrigée).")
            except Exception as e:
                print("Erreur lors de la commande :", e)

        # OPTION 4 : Vérification de la calibration
        elif choix == "4":
            print("Table de calibration actuellement chargée :")
            print("Épaule :", table_erreurs["epaule"])
            print("Coude  :", table_erreurs["coude"])

        # OPTION 5 : Exécution d’un pattern
        elif choix == "5":
            print("Exécution du pattern Shambala...")
            pattern_points = shambala_pattern(
                radius_step=15, num_circles=6, points_per_circle=200,
                wave_amplitude=5, wave_frequency=12)
            for (x, y) in pattern_points:
                alpha, beta = cinematics_inverse(x, y)
                alpha_corr, beta_corr = appliquer_calibration(alpha, beta, table_erreurs)
                move_servos(alpha_corr, beta_corr, stylo_on=True)
                time.sleep(0.05)
            print("Pattern terminé ")

        # OPTION q : Quitter
        elif choix == "q":
            print("Programme terminé.")
            break

        # OPTION invalide
        else:
            print("Choix invalide.")
