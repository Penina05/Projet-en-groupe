from calibration.calibration import calibration_interactive, move_servo
from cinematique.cinematique import cinematics_inverse, calibration_configuration, envoyer_angles_compenses
from commande.commande import interprete_ligne, bouger_servo, servo_epaule, servo_coude

def main():
    print("=== PROGRAMME PRINCIPAL ===")
    print("Options disponibles :")
    print("  1 : Mode calibration manuelle")
    print("  2 : Mouvement vers une position cible (cinématique inverse)")
    print("  3 : Lecture d’un fichier de commandes servo")
    print("  q : Quitter")
    print("----------------------------")

    while True:
        choix = input("Choix : ").strip()

        if choix == "1":
            calibration_interactive()

        elif choix == "2":
            try:
                x = float(input("Entrez x (mm) : "))
                y = float(input("Entrez y (mm) : "))
                alpha, beta = cinematics_inverse(x, y)
                table_erreurs = calibration_configuration("data/calibration_donnees_X.txt")
                alpha_corr, beta_corr = envoyer_angles_compenses(alpha, beta, table_erreurs)
                bouger_servo(servo_epaule, alpha_corr)
                bouger_servo(servo_coude, beta_corr)
            except Exception as e:
                print("Erreur lors du calcul ou de l’envoi :", e)

        elif choix == "3":
            nom_fichier = input("Nom du fichier de commandes : ").strip()
            try:
                with open(nom_fichier, 'r') as f:
                    for ligne in f:
                        interprete_ligne(ligne)
            except FileNotFoundError:
                print(f"Fichier {nom_fichier} introuvable.")

        elif choix == "q":
            print("Programme terminé.")
            break

        else:
            print("Choix invalide.")