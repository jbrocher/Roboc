#--encoding=utf-8--
from threading import Thread
import socket
from lib.client.ClientInterface import ClientInterface

class Receive(ClientInterface):

    def __init__(self,client_connexion):

        ClientInterface.__init__(self)
        self.client_connexion = client_connexion







    def run(self):


        while ClientInterface.cont:

            msg_recu = self.client_connexion.recv(1024)
            ClientInterface.msg_recu = msg_recu.decode()
            if ClientInterface.msg_recu == "0" or ClientInterface.msg_recu == "1":
                ClientInterface.cont = False
                if ClientInterface.msg_recu == "1":
                    print("félicitations vous avez gagné!")
                else:
                    print("désolé, c'est perdu")
                print("\nfin de la partie, deconnexion en cours\nappuyez sur enter pour fermer")

            else:

                print("\n"+ClientInterface.msg_recu)
