#--encoding=utf-8--
""" module qui définie la calss interface"""
import os

from lib.serveur.Game import Game
from lib.serveur.Map import Map
import re
import socket
import select
import re

class ClientsHandler:

    """ La classe ClientsHandler gère les connexions avec les différents clients
     du serveur. Elle possède en attribut un dictionnaire dont les clés sont des
     ids composées de l'addresse ip et du port du client, et les valeurs sont
     les sockets correespondant"""

     #note: on pourrait rajouter un séparateur lors de l'envoie
     #des messages côtés clients pour être certain que chaque message
     #soit traité comme un message indépendant


    def __init__(self, max_clients = 10, port=12800):

        #Nombre de connexion maximum autorisées
        self.max_clients = max_clients

        #dictionnaire des clients
        self.clients = {}

        #setUp du socket serveut
        self.serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverConnection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 12800)
        self.serverConnection.bind(("",port))

        self.serverConnection.listen(5)


    def getClients(self):

        """renvoie la liste des sockets clients"""
        return self.clients.values

    def getClientsIds(self):

        """renvoie la liste des ids clients"""
        return self.clients.keys()

    def selectClients(self, clients_id):

        """ renvoie les sockets correspondant aux ids de la liste clients_id"""

        result =[]
        for client in self.clients:
            if client in clients_id:
                result.append(self.clients[client])
        return result

    def generateClientId(self,client):

        """renvoie l'id du socket client. Celle-ci est crée par concaténation de
         l'adresse ip et du port"""
        client_id  = str(client.getpeername()[0]) +'.'+ str(client.getpeername()[1])
        return client_id

    def setUpConnect(self):

        """Parcours les connection demandées et accepte des connections tant
        qu'aucun client n'appuie sur c, ou que le sueil de connections est
        dépassé"""
        print("setting up connection...")
        wait_user = True

        user_count = 0
        while wait_user:

            if user_count >= self.max_clients:
                wait_user = False
                print("connection set up")
            else:

                #La première partie du while parcours les connections en attente
                #d'acceptation
                connexions_demandees, wlist, xlist = select.select([self.serverConnection],[], [], 0.05)

                for connexion in connexions_demandees:

                    #on vérifie qu'on ne dépasse pas le maximum avant d'accepter
                    # la connection.
                    if user_count < self.max_clients:

                        connexion_avec_client, infos_connexion = connexion.accept()

                        #on met à jour le dictionnaire des clients
                        client_id  = self.generateClientId(connexion_avec_client)
                        self.clients[client_id] = connexion_avec_client

                        user_count += 1

                        #on informe le client
                        self.clientsUpdate(messages ={client_id : "\nbienvenue joueur{}\nen attente d'autres joueurs, appuyez sur 'c' pour commencer".format(str(user_count))})
                try:
                    clients_a_lire, wlist, xlist = select.select(self.clients.values(),[], [], 0.05)
                except select.error:
                    pass
                else:
                    #la deuxième partie du while vérifie si le message "c" a été
                    #reçu parmis les connections déjà acceptées


                    for client in clients_a_lire:

                        try:
                            msg_recu = client.recv(1024)
                            msg_recu = msg_recu.decode()
                            if msg_recu == 'c' :

                                wait_user = False
                                print("connection set up")
                            else:

                                client.send(b"invalid input")

                        except ValueError:
                            pass





    def receiveCommand(self,clients_to_process):

        """ cette fonction prend en entrée une liste d'id clients, et attend d'
        avoir reçu exactement un message par client, avant de retourner
        le dictionnaire des commandes reçues.

        Ici la liste sera toujours
        constituées d'un seul id, mais cette fonction est plus générale pour
        permettre de synchroniser les commandes utilisateurs, pour qu'il puisse
        'jouer en même temps'. par exemple pour implémenter un jeu par équipe"""

        print("gathering commands..")

        clients_messages = {}
        to_process = len(clients_to_process)

        #temps qu'il reste des commandes à recevoir, on vérifie l'ensemble des
        #sockets
        while to_process != 0:
            try:
                clients_a_lire, wlist, xlist = select.select(self.clients.values(),[], [], 0.05)
            except select.error:
                pass
            else:
                for client in clients_a_lire:
                    client_id = self.generateClientId(client)

                    #on vérifie que le message provient d'un id présent dans
                    #la liste donnée en argument. C'est à dire un client dont
                    #c'est le tour

                    if client_id in clients_to_process:
                        try:

                            #si le client n'a pas déjà envoyé une commande
                            #valide
                            if not (client_id in clients_messages.keys()):

                                msg_recu = client.recv(1024)
                                msg_recu_d = msg_recu.decode()

                                #si la commande reçue est valide
                                if re.search('^[n,s,o,e,q,N,S,O,E][0-9]*$|^[m,p,M,P][n,s,o,e,q,N,S,O,E]$', msg_recu_d) != None:

                                    if len(msg_recu_d) == 1:
                                        msg_recu_d += "1"
                                    clients_messages[client_id] = msg_recu_d
                                    client.send(b"commande recue, processing...")
                                    print("commande valide recue from {}".format(client_id))
                                    to_process -= 1
                                    print(str(to_process))

                                #si la commande valide, le client n'est pas ajoutée
                                #a la liste des id déjà traitées
                                else:

                                    client.send(b"commande invalide")
                                    print("commande invalide recue from {}".format(client_id))

                            #si une commande valide a déjà été reçue de la part de ce client
                            else:
                                msg_recu = client.recv(1024)
                                client.send(b"en attente des autres joueurs")
                                print("commande deja recue from {}".format(client_id))

                        except ValueError:

                            print("exception")
                            pass
                    #si l'id ne correspond pas à un client dont c'est le tour
                    else:
                        msg_recu = client.recv(1024)
                        client.send(b"attendez votre tour!")



        return clients_messages





    def clientsUpdate(self, message=None, messages=None):
        """ arguments:
                message: chaine de charactère
                messages: dictionnaire client_id : message

            return: None
            envoie l'arguement message à tous les clients, ou des messages
            différents répertoriés dans 'messages' """

        if message != None and messages == None:

            print("sending {} to all clients".format(repr(message)))

            for client_id in self.clients:
                to_send = message.encode()
                self.clients[client_id].send(to_send)

        elif messages != None and message == None:
            print(r"sending {}".format(messages))
            for client_id in messages:

                to_send = messages[client_id].encode()
                self.clients[client_id].send(to_send)
        else:
            raise ValueError

    def close(self):
        """ferme toutes les connections"""
        for client in self.clients.values():
            fin = b""
            #côté client, l'envoie de "end" sert a vérifié que les Threads ont
            #ont bien terminé avant de fermer la connection
            while fin != b"end":
                fin = client.recv(1024)

            print("closing {}".format(self.generateClientId(client)))
            client.close()


        self.serverConnection.close()
        print("server connection closed")
