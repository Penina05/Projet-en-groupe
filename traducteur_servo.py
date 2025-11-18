def traduit(angle: float) -> int:
	"""
	Convertit un angle en degrés vers l'entrée correspondante
	pour la méthode duty_u16 de la classe servo

	Voir https://docs.micropython.org/en/latest/library/machine.PWM.html pour plus de
	détails sur la méthode duty_u16
	"""

	MIN = 1638 # 0 degrés
	MAX = 8192 # 180 degrés
	DEG = (MAX - MIN) / 180 # valeur par degré

	# l'angle de serrage doit être compris entre 0 et 180
	angle = max(0, min(180, angle))

	return int(angle * DEG + MIN)