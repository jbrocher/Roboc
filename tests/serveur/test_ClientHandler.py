#encoding=utf8

from lib.serveur.Game import Game
from lib.serveur.Map import Map
from lib.serveur.ClientsHandler import ClientsHandler
import socket
import unittest


class TestClientHandler(unittest.TestCase):

    def setUp(self):
        self.client_handler_test_1 = ClientsHandler(max_clients = 3, port=12800)
        self.hote="localhost"
        self.port = 12800
        self.socket_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client_1.connect((self.hote, self.port))
        self.socket_client_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client_2.connect((self.hote, self.port))
        self.socket_client_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client_3.connect((self.hote, self.port))
        self.socket_client_4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client_4.connect((self.hote, self.port))






    def test_setUpConnect(self):

        self.client_handler_test_1.setUpConnect()
        clients = self.client_handler_test_1.clients
        self.assertEqual(len(clients),3)



        self.socket_client_1.send(b"test_1")
        self.socket_client_2.send(b"test_2")
        self.socket_client_3.send(b"test_3")

        self.client_1_id  = str(self.socket_client_1.getsockname()[0]) +'.'+ str(self.socket_client_1.getsockname()[1])
        self.client_2_id  = str(self.socket_client_2.getsockname()[0]) +'.'+ str(self.socket_client_2.getsockname()[1])
        self.client_3_id  = str(self.socket_client_2.getsockname()[0]) +'.'+ str(self.socket_client_2.getsockname()[1])



        result = []
        for client_id in clients:


            result.append( clients[client_id].recv(1024))

        self.assertEqual(len(result), 3)
        self.assertIn(b"test_1",result)
        self.assertIn(b"test_2",result)
        self.assertIn(b"test_3",result)
