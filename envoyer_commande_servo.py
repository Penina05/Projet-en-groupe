#PROGRAMME envoyer_commande_servo
#Module de commande des servomoteurs

# Initialisation des servos
servo_epaule = PWM(Pin(0))
servo_coude = PWM(Pin(1))
servo_poignet = PWM(Pin(2))

#Frequence de fonctionnement en hertz
servo_epaule.freq(50)
servo_coude.freq(50)
servo_poignet.freq(50)

#Cette fonction permet de bouger le servomoteur en fonction des angles corriges 

def bouger_servo(servo, angle): #peut s’appeler envoyer_commande_servos
    pwm = traduit(angle) # la fonction traduit(angle) recupere les angles des servmoteurs et traduit en signal large impulsion (PWM) 
    servo.duty_u16(pwm)
    time.sleep(0.1) 

#Ici, nous lisons le fichier csv provenant de la calibration des valeurs des servomoteurs
#Le programme utilise le principe selon lequel les lettres G1 , M3 et M5 designent les positions des servomoteurs et leur etat
def interprete_ligne(ligne):
    ligne = ligne.strip()
    if ligne.startswith("G1"):
        # Mouvement des servos S (épaule) et E (coude)
        angle_s = None
        angle_e = None
        if "S" in ligne:
            s_index = ligne.find("S")
            angle_s = float(ligne[s_index+1:].split()[0])
        if "E" in ligne:
            e_index = ligne.find("E")
            angle_e = float(ligne[e_index+1:].split()[0])
        if angle_s is not None:
            bouger_servo(servo_epaule, angle_s)
        if angle_e is not None:
            bouger_servo(servo_coude, angle_e)

    elif ligne.startswith("M3"):
        # Baisser le stylo
        bouger_servo(servo_poignet, 30)

    elif ligne.startswith("M5"):
        # Lever le stylo
        bouger_servo(servo_poignet, 0)

    elif ligne.startswith("M18"):
        # Désactiver les servos
        servo_epaule.deinit()  
''' l'expression servo_coude.deinit() permet de desactiver les servos. En fait, cette fonction arrête le contrôle du servo et libère les ressources matérielles associées. C’est l’équivalent d’un “nettoyage” avant de passer à autre chose.'''
        servo_coude.deinit()
       
