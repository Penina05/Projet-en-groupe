from datetime import datetime   #Permet d’obtenir la date et l’heure actuelles pour horodater les erreurs.

def journaliser_erreur(message: str):  #Elle prend un message d’erreur en entrée et ne retourne rien. Le type "str" précise que l’argument est une chaîne de caractères.
    """
    Responsable : Tresor
    -----------------------------------------------------------
    Entrée :
        - message : texte décrivant l’erreur
    Sortie :
        - aucune
    Description :
        Écrit un message d’erreur dans un fichier de log pour
        le suivi et le débogage des tests futurs.
    """
  #Fournit des informations sur le rôle de la fonction, ses paramètres, sa sortie, et son objectif. Très utile pour la documentation et la maintenance.
    try:    #Démarre une tentative d’exécution protégée pour éviter que l’écriture dans le fichier ne provoque une erreur non gérée.
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #Récupère la date et l’heure actuelles, puis les formate en une chaîne lisible (ex. "2025-11-17 20:23:00"). 
        with open("log_erreurs.txt", "a", encoding="utf-8") as fichier_log:   #Ouvre (ou crée) le fichier "log_erreurs.txt"  en mode ajout ("a"), avec encodage UTF-8. Le mot-clé "with"  garantit que le fichier sera bien fermé après usage.
            fichier_log.write(f"[{horodatage}] ERREUR : {message}\n")   #Insère dans le fichier une ligne contenant l’horodatage et le message d’erreur, précédé du mot-clé "ERREUR".
    except Exception as e:   #Si une erreur survient pendant l’écriture (ex. fichier inaccessible), elle est capturée ici.
        print(f"Échec de journalisation de l’erreur : {e}")    #Affiche dans la console un message indiquant que la journalisation a échoué, avec le détail de l’exception.
