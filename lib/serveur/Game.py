#--encoding=utf-8--
""" Module qui définit la class "Game", qui sert correspond au moteur du jeu"""
from lib.serveur.Map import Map
import re
class Game:

    """La class "Game" correspond au moteur du jeu. Un objet Game
    possède une map et la position du joueur. Il gère ainsi les déplacements
    et les collisions"""

    def __init__(self, map =None):
        """ initialise l'objet avec la map, et la position initale associée
        à cette map"""
        if map != None:

            self.map = map
            self.i = self.map.i_init
            self.j = self.map.j_init
        else:
            self.map = None
            self.i= 0
            self.j= 0



    def getPosition(self):
        """ renvoie la position actuelle du joueur"""

        return dict(i = self.i , j = self.j)

    def setPosition(self,position):

        """ prend un dictionnaire en argument, et modifie
         la position du joueur"""

        self.i = position["i"]
        self.j = position["j"]

    def moveProcess(self, move):
        """Renvoi True si le mouvement est valide, False sinon. Si le mouvement,
        est valide, modifie la position du joueur en conséquence. Un mouvement
        est invalide si il sort des limites de la Map, ou si il ya un mur sur
        la trajectoire"""

        valid = True
        i= self.i
        j= self.j
        depl_vert= True
        pos = True

        if move["direction"] == "n":
            i -=  move["distance"]
            pos = False
        elif move["direction"] == "s":
            i += move["distance"]
        elif move["direction"] == "o":
            j -= move["distance"]
            pos = False
            depl_vert = False
        else:
            j += move["distance"]
            depl_vert = False


        if not (0<= i and i <self.map.i_max) or not(0<= j and j < self.map.j_max):
            valid = False
        elif depl_vert:
            if pos:
                for l in range(self.i, i+1):
                    if self.map.map_data[l][j] == "O": valid = False
            else:
                for l in range(i, self.i):
                    if self.map.map_data[l][j] == "O": valid = False
        else:
            if pos:
                for l in range(self.j, j+1):
                    if self.map.map_data[i][l] == "O": valid = False
            else:
                for l in range(j, self.j):

                    if self.map.map_data[i][l] == "O": valid = False

        if valid:

            self.i = i
            self.j = j
        return valid



    def checkWin(self):
        """ renvoi True si le joueur a gagné"""


        return ( self.map.map_data[self.i][self.j] == 'U')

    def display(self,client_ids):
        """renvoi le string représentant la carte"""

        return self.map.serializeMap(client_ids,self.i, self.j)