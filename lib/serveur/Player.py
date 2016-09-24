#encoding=utf-8

import socket

class Player():

    """Cette classe représente un joueur de la partie. En plus des attributs
     correspondant aux informations de jeu, un player connait l'identifiant
     du socket du client qu'il représente"""

    def __init__(self, player_id,client_id,position, pseudo = None, symbole=None):

        #un string représentant l'id du socket associé
        self.client_id=client_id

        #informations du joueur
        self.player_id= player_id
        self.pseudo = pseudo,
        self.symbole = symbole

        #information de jeu
        self.position = position
