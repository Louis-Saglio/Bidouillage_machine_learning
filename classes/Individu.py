"""
Sens : Récupère des informations extèrieures
Action : méthodes
Raison : analyse les données pour déterminer l'action à executer
Gênes : un gene par action donnant une probabilité d'accomplir l'action
Actions : se reproduire, mourrir, attaquer, se déplacer
Générateur d'actions aléatoires
Metadonnées, inaccessible directement (ex position)
"""
from Carte import Carte


class Individu:

    def __init__(self, position):
        self.sens = {}
        self.metadata = {}
        self.data = {}
        self.actions = {}
        self.genes = {}
