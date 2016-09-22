#--encoding=utf-8--


from threading import Thread
import socket
from lib.client.ClientInterface import ClientInterface
class Send(ClientInterface):

    def __init__(self,client_connexion):

        ClientInterface.__init__(self)
        self.client_connexion = client_connexion






    def run(self):


        while not ClientInterface.end_threads:

            user_input = input(">")
            user_input_e = user_input.encode()
            self.client_connexion.send(user_input_e)
        return 0
