#--encoding=utf-8--
""" module qui définie la calss interface"""
import os
import pickle
from lib.serveur.Game import Game
from lib.serveur.Map import Map
from lib.serveur.ClientsHandler import ClientsHandler
import re
import socket
import select

class Interface:

    """ Cette class sert d'interface entre le joueur et le jeu. Elle gère les entrées/sorties ainsi que la sauvegarde et le chargement des cartes"""


    tour = 1
    def __init__(self):

        self.maps = []
        self.client_ids=[]
        self.selected_map = Map()
        self.client_handler = None






    def loadMaps(self):
        """ parcours le dossier Map, et charge les cartes dans l'attribut maps"""
        files = os.listdir('maps')
        for file_name in files:
            self.maps.append(Map(file_name))



    def displayMaps(self):
        """ affiche la liste des cartes disponibles"""
        for i, m in enumerate(self.maps):
            print("{}: {}\n".format(i,m.map_name))



    def setUp(self):
        """gère le choix de la map et initilise le "Game"""

        maps_number = len(self.maps)
        choice = int(self.checkUserInput('^[0-{}]$'.format(maps_number), "please type the number of the map you'd like to play: ", "invalid input"))

        self.selected_map = self.maps[choice]


        max_clients = int(self.checkUserInput('^[0-9]*$', "please type the max number of players: ", "invalid input"))
        self.client_handler = ClientsHandler(max_clients = max_clients)
        self.client_handler.setUpConnect()
        self.client_ids = self.client_handler.getClientsIds()
        for client_id in self.client_ids:

            self.game = Game(self.client_ids,self.selected_map)




    def checkUserInput(self,pattern,input_message,error_message,error_function = None):
        """ vérifie que l'input de l'utilisateur match la regex pattern, sinon
        redemande un input avec le message 'input_message' et affiche le message
        d'erreur. Si elle est définie, execute error_function"""
        command = input(input_message)
        while re.search(pattern,command) is None:
            print(error_message)
            if error_function != None : error_function()
            command = input(input_message)
        return command



    def processCommands(self):
        """ gère les commandes de l'utilisateurs, utilise l'objet Game pour
        analyser les directions"""

        self.client_handler.clientsUpdate(message = "\ndebut du tour {}".format(Interface.tour))
        winners = []

        commands = {}
        clients_to_process = self.client_ids

        for client_id in clients_to_process:
            invalid = True
            self.client_handler.clientsUpdate(messages = {client_id: "\na vous de jouer! entrez votre commande"})
            while invalid:

                commands = self.client_handler.receiveCommand([client_id])
                print("processing command from {}".format(client_id))

                if self.game.moveProcess( commands[client_id], client_id):

                    invalid = False
                    if self.game.checkWin(client_id):
                        winners.append(client_id)
                else:
                    self.client_handler.clientsUpdate(messages = {client_id: "mouvement invalide entrez une autre commande"})
                print(" command from {} processed".format(client_id))
            self.display()
        Interface.tour +=1
        return winners


    def endGame(self,winners):
        messages = {}
        print("les gagnants sont:")
        print(winners)
        for client_id in self.client_ids:
            if client_id in winners:
                messages[client_id] = "1"
            else:
                messages[client_id] = "0"
        self.client_handler.clientsUpdate(messages = messages)

        self.client_handler.close()

    def display(self):
        print("displaying game")
        clients_positions = []
        maps_to_send= self.game.display()

        self.client_handler.clientsUpdate(messages = maps_to_send)
