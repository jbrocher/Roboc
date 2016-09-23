#--encoding=utf-8--
""" Module qui définit la class "Game", qui sert correspond au moteur du jeu"""
from lib.serveur.Map import Map
import random
import re
class Game:

    """La class "Game" correspond au moteur du jeu. Un objet Game
    possède une map et la position du joueur. Il gère ainsi les déplacements
    et les collisions"""

    def __init__(self, client_ids, map = None,):
        """ initialise l'objet avec la map, et la position initale associée
        à cette map"""
        self.map = map
        self.players = {}

        for client_id in client_ids:
            valid = False
            (i,j) = (random.randrange(0,self.map.i_max),random.randrange(0,self.map.j_max))

            while not valid:

                if not (self.map.map_data[i][j] == 'O' or (i,j) in self.players.values()):

                    valid = True
                    self.players[client_id] = (i,j)

                else:
                    (i,j) = (random.randrange(0,self.map.i_max),random.randrange(0,self.map.j_max))







    def getPosition(self):
        """ renvoie la position actuelle du joueur"""

        return self.players

    def setPosition(self,positions):

        """ prend un dictionnaire en argument, et modifie
         la position du joueur"""

        self.players = positions



    def newPos(self,i,j,move):
        if len(move) == 1 :
            move += '1'

        if move[0] == "n":
            i -=  int(move[1])
            pos = False
        elif move[0] == "s":
            i += int(move[1])
        elif move[0] == "o":
            j -= int(move[1])
            pos = False
            depl_vert = False
        else:
            j += int(move[1])
            depl_vert = False
        return(i,j)

    def validMove(self, i_init, j_init, i,j):
        valid = True
        if not (0<= i and i <self.map.i_max) or not(0<= j and j < self.map.j_max):
            valid = False
        elif (i,j) in self.players.values():
            valid = False
        elif i != i_init:
            if i - i_init >0:
                for l in range(i_init, i+1):
                    if self.map.map_data[l][j] == "O": valid = False
            else:
                for l in range(i, i_init):
                    if self.map.map_data[l][j] == "O": valid = False
        else:
            if j - j_init > 0:
                for l in range(j_init, j+1):
                    if self.map.map_data[i][l] == "O": valid = False
            else:
                for l in range(j, j_init):

                    if self.map.map_data[i][l] == "O": valid = False
        return valid

    def moveProcess(self, move, client_id):
        """Renvoi True si le mouvement est valide, False sinon. Si le mouvement,
        est valide, modifie la position du joueur en conséquence. Un mouvement
        est invalide si il sort des limites de la Map, ou si il ya un mur sur
        la trajectoire"""

        valid = True

        i_client,j_client =self.players[client_id]

        if re.search('^[n,s,o,e,q,N,S,O,E][0-9]*$', move) != None:
            i,j = self.newPos(i_client,j_client,move)
            valid = self.validMove(i_client, j_client,i,j)
            if valid:

                self.players[client_id] = (i,j)

        elif re.search('^[m,p,M,P][n,s,o,e,q,N,S,O,E]$', move) != None:

            i,j = self.newPos(i_client, j_client, move[1])
            if (i,j) in self.players.values():
                valid = False
            elif move[0] == 'm' or move[0] == 'M':
                if self.map.map_data[i][j] != '.':
                    valid = False
                else:
                    self.map.modifyMap(i,j,'O')
            else:

                if self.map.map_data[i][j] != 'O':
                    valid = False
                else:
                    self.map.modifyMap(i,j,'.')



        return valid



    def checkWin(self,client_id):
        """ renvoi True si le joueur a gagné"""

        i,j = self.players[client_id]
        return ( self.map.map_data[i][j] == 'U')

    def display(self):
        """renvoi le string représentant la carte"""
        payload = {}
        for client_id in self.players:
            i,j = self.players[client_id]
            payload[client_id] = self.map.serializeMap(self.players.values(),i, j)
        return payload
