#encoding=utf8

from lib.serveur.Game import Game
from lib.serveur.Map import Map
import unittest

class TestGame(unittest.TestCase):

    def setUp(self):
        self.map_test_1 = Map('facile.txt')
        self.client_ids = ['127.0.0.1.4986','127.0.0.1.4987','127.0.0.1.4988','127.0.0.1.4989']
        self.game_test_1 = Game(self.client_ids,self.map_test_1)

        #les positions crées avec le constructeur sont aléatoire, on les choisit
        #nous même pour le test

        self.game_test_1.players[0].position=(1,2)
        self.game_test_1.players[1].position=(3,2)
        self.game_test_1.players[2].position=(4,5)
        self.game_test_1.players[3].position=(6,5)

    def test_getPlayerID(self):

        player_id  = self.game_test_1.getPlayerId('127.0.0.1.4987')
        self.assertEqual(player_id,2)

    def test_getPosition(self):


        positions = self.game_test_1.getPosition()
        self.assertEqual(positions,[(1,2),(3,2),(4,5),(6,5)])

    def test_getDictPosition(self):

        dict_positions = self.game_test_1.getDictPositions()
        self.assertEqual(dict_positions,{'127.0.0.1.4986':(1,2),'127.0.0.1.4987':(3,2),'127.0.0.1.4988':(4,5),'127.0.0.1.4989':(6,5)})

    def test_setPosition(self):

        self.game_test_1.setPosition((5,8),'127.0.0.1.4988')
        self.assertEqual((5,8),self.game_test_1.players[2].position)

    def test_newPos(self):

        (i1,j1) = self.game_test_1.newPos(1,3,'n')
        (i2,j2) =self.game_test_1.newPos(6,4,'s')
        (i3,j3) =self.game_test_1.newPos(8,9,'e')
        (i4,j4) =self.game_test_1.newPos(6,7,'o')

        (i5,j5) =self.game_test_1.newPos(4,3,'n3')
        (i6,j6) =self.game_test_1.newPos(8,5,'s4')
        (i7,j7) =self.game_test_1.newPos(9,4,'e2')
        (i8,j8) =self.game_test_1.newPos(8,20,'o19')

        self.assertEqual((i1,j1),(0,3))
        self.assertEqual((i2,j2),(7,4))
        self.assertEqual((i3,j3),(8,10))
        self.assertEqual((i4,j4),(6,6))

        self.assertEqual((i5,j5),(1,3))
        self.assertEqual((i6,j6),(12,5))
        self.assertEqual((i7,j7),(9,6))
        self.assertEqual((i8,j8),(8,1))

    def test_validMove(self):

        not_valid = self.game_test_1.validMove(1,1,1,5)
        valid = self.game_test_1.validMove(1,1,4,1)
        self.assertEqual(not_valid, False)
        self.assertEqual(valid, True)

    def test_checkValid(self):
        self.game_test_1.players[1].position = (5,9)
        not_winner = self.game_test_1.checkWin('127.0.0.1.4986')
        winner = self.game_test_1.checkWin('127.0.0.1.4987')
        self.assertEqual(not_winner,False)
        self.assertEqual(winner,True)
