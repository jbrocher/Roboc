#--encoding=utf-8--
""" Module qui définit la class "Game", qui sert correspond au moteur du jeu"""
from lib.serveur.Map import Map
from lib.serveur.Player import Player
import random
import re
class Game:

    """La class "Game" repérésente une partie.Un objet Game
    possède une map et des Players. Il gère ainsi les déplacements
    et les collisions"""

    def __init__(self, client_ids, map = None):
        """ initialise l'objet avec la map, et construits les Players à partir
            del la liste client_id. Pour chaque joueur on choisit des coordonnées
            aléatoires jusqu'à ce qu'ell correspondent à une position valide"""
        self.map = map
        self.players = []
        player_counter = 1
        for client_id in client_ids:
            valid = False
            (i,j) = (random.randrange(0,self.map.i_max),random.randrange(0,self.map.j_max))

            while not valid:

                if not (self.map.map_data[i][j] == 'O' or (i,j) in self.players):

                    valid = True
                    self.players.append(Player(player_counter,client_id,(i,j)))
                    player_counter += 1

                else:
                    (i,j) = (random.randrange(0,self.map.i_max),random.randrange(0,self.map.j_max))





    def getPlayerId(self,client_id):

        """renvoi le player_id correpondant au client_id"""
        player_id = 0
        for player in self.players:

            if player.client_id == client_id:

                player_id = player.player_id
        return player_id

    def getPosition(self):
        """ renvoie la liste des positions"""
        positions = []
        for player in self.players:
            positions.append(player.position)
        return positions

    def getDictPositions(self):
        """renvoie un dictionnaire dont les clés sont les clients_id et les
            valeurs sont les positions correspondantes"""
        result = {}
        for player in self.players:

            result[player.client_id] = player.position
        return result
    def setPosition(self,position,client_id):

        """ donne la valeur position à l'attrobut position du player
            correspondant au client_id """

        for player in self.players:

            if player.client_id == client_id:

                player.position = position





    def newPos(self,i,j,move):
        """arguments:
            i(int): ligne initiale
            j(int): colonne initale
            move(String): movement a effectué
            renvoi
                (i,j) tuples représentant la nouvelle position """
        if len(move) == 1 :
            move += '1'

        if move[0] == "n":
            i -=  int(move[1:])
            pos = False
        elif move[0] == "s":
            i += int(move[1:])
        elif move[0] == "o":
            j -= int(move[1:])
            pos = False
            depl_vert = False
        else:
            j += int(move[1:])
            depl_vert = False
        return(i,j)

    def validMove(self, i_init, j_init, i,j):
        """ Renvoi True si le déplacement de (i_init, j_init) vers (i,j)
        est valide.
        Mouvements invaide:
            - Mur ou joueur sur la trajectoire
            - percer autre chose qu'un mur
            - murer autre chose qu'une porte """

        valid = True
        positions = self.getPosition()
        if not (0<= i and i <self.map.i_max) or not(0<= j and j < self.map.j_max):
            valid = False
        elif (i,j) in positions:
            valid = False
        elif i != i_init:
            if i - i_init >0:
                for l in range(i_init +1, i+1):
                    if self.map.map_data[l][j] == "O" or (l,j) in positions: valid = False
            else:
                for l in range(i, i_init-1):
                    if self.map.map_data[l][j] == "O" or (l,j) in  positions: valid = False
        else:
            if j - j_init > 0:
                for l in range(j_init+1, j+1):
                    if self.map.map_data[i][l] == "O" or (i,l) in  positions: valid = False
            else:
                for l in range(j, j_init-1):

                    if self.map.map_data[i][l] == "O" or (i,l) in  positions: valid = False
        return valid

    def moveProcess(self, move, client_id):
        """Renvoi True si le mouvement est valide, False sinon. Si le mouvement,
        est valide, modifie la position du joueur correspondand au client_id
         en conséquence. """

        valid = True

        i_client,j_client =self.getDictPositions()[client_id]

        #si c'est un déplacement
        if re.search('^[n,s,o,e,q,N,S,O,E][0-9]*$', move) != None:
            i,j = self.newPos(i_client,j_client,move)
            valid = self.validMove(i_client, j_client,i,j)
            if valid:

                self.setPosition((i,j),client_id)

        #si c'est une modification de la Map
        elif re.search('^[m,p,M,P][n,s,o,e,q,N,S,O,E]$', move) != None:

            i,j = self.newPos(i_client, j_client, move[1])

            # j'ai choisi d'empécher l'emmurage des autres joueurs :)
            if (i,j) in self.getPosition():
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

        i,j = self.getDictPositions()[client_id]
        return ( self.map.map_data[i][j] == 'U')

    def display(self):
        """renvoi le string représentant la carte"""
        payload = {}
        positions_dict = self.getDictPositions()
        for client_id in positions_dict:
            i,j = positions_dict[client_id]
            payload[client_id] = self.map.serializeMap(self.getPosition(),i, j)
        return payload
