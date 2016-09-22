#--encoding=utf-8--
from threading import Thread
import socket
from lib.client.ClientInterface import ClientInterface

class Receive(ClientInterface):

    def __init__(self,client_connexion):

        ClientInterface.__init__(self)
        self.client_connexion = client_connexion






    def run(self):


        msg_recu_d = ""
        while msg_recu_d != "end":



            msg_recu = self.client_connexion.recv(1024)

            msg_recu_d = msg_recu.decode()
            if msg_recu != "":
                print("message reçu:\n"+msg_recu_d)
        ClientInterface.end_threads = True
        return 0
