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


    def __init__(self, max_clients = 10, port=12800):

        self.max_clients = max_clients

        self.clients = {}


        self.serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverConnection.bind(("",port))
        self.serverConnection.listen(5)


    def getClients(self):
        return self.clients.values

    def getClientsIds(self):

        return self.clients.keys()

    def selectClients(self, clients_id):
        result =[]
        for client in self.clients:
            if client in clients_id:
                result.append(self.clients[client])
        return result

    def generateClientId(self,client):
        client_id  = str(client.getpeername()[0]) + str(client.getpeername()[1])
        return client_id

    def setUpConnect(self):

        print("setting up connection...")
        wait_user = True

        user_count = 0
        while wait_user:

            if user_count >= self.max_clients:
                wait_user = False
                print("connection set up")
            else:

                connexions_demandees, wlist, xlist = select.select([self.serverConnection],[], [], 0.05)

                for connexion in connexions_demandees:


                    connexion_avec_client, infos_connexion = connexion.accept()
                    client_id  = self.generateClientId(connexion_avec_client)
                    self.clients[client_id] = connexion_avec_client


                    user_count += 1

                try:
                    clients_a_lire, wlist, xlist = select.select(self.clients.values(),[], [], 0.05)
                except select.error:
                    pass
                else:

                    for client in clients_a_lire:

                        try:
                            msg_recu = client.recv(1024)
                            msg_recu = msg_recu.decode()
                            if msg_recu == 'c' :

                                wait_user = False
                                print("connection set up")
                        except ValueError:
                            pass





    def receiveCommand(self,clients_to_process):
        print("gathering commands..")

        clients_messages = {}
        to_process = len(clients_to_process)
        while to_process != 0:
            try:
                clients_a_lire, wlist, xlist = select.select(self.clients.values(),[], [], 0.05)
            except select.error:
                pass
            else:
                for client in clients_a_lire:
                    client_id = self.generateClientId(client)
                    if client_id in clients_to_process:
                        try:
                            print("bloc try")
                            if not (client_id in clients_messages.keys()):

                                msg_recu = client.recv(1024)
                                msg_recu_d = msg_recu.decode()

                                if re.search('^[n,s,o,e,q,N,S,O,E][0-9]*|[m,p,M,P][n,s,o,e,q,N,S,O,E]$', msg_recu_d) != None:

                                    if len(msg_recu_d) == 1:
                                        msg_recu_d += "1"
                                    clients_messages[client_id] = msg_recu_d
                                    client.send(b"commande recue, processing...")
                                    print("commande valide recue from {}".format(client_id))
                                    to_process -= 1
                                    print(str(to_process))

                                else:

                                    client.send(b"commande invalide")
                                    print("commande invalide recue from {}".format(client_id))
                            else:
                                msg_recu = client.recv(1024)
                                client.send(b"en attente des autres joueurs")
                                print("commande deja recue from {}".format(client_id))

                        except ValueError:

                            print("exception")
                            pass
                    else:
                        msg_recu = client.recv(1024)
                        client.send(b"attendez votre tour!")



        return clients_messages





    def clientsUpdate(self, message=None, messages=None):
        print("sending {}".format(messages))
        if message != None and messages == None:
            for client_id in self.clients:

                to_send = message.encode()
                self.clients[client_id].send(to_send)
        elif messages != None and message == None:

            for client_id in messages:

                to_send = messages[client_id].encode()
                self.clients[client_id].send(to_send)
        else:
            raise ValueError

    def close(self):
        for client in self.clients.values():
            client.close()
        self.serverConnection.close()
