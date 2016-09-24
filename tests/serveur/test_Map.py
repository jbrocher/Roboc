
#encoding=utf8

import unittest
from lib.serveur.Map import Map

class TestMap(unittest.TestCase):
    """ class de test pour la classe Map"""


    def setUp(self):

        self.map_test_1 = Map("facile.txt")
        self.map_reference_1 = Map("facile.txt")
        self.client_positions = [(2,1),(1,4),(3,3)]


    def test_modifyMap(self):

        self.map_test_1.modifyMap(1,2,'.')
        for i,line in enumerate(self.map_test_1.map_data):
            for j,c in enumerate(line):
                if (i,j) == (1,2):
                    self.assertEqual(c,'.')
                else:
                    self.assertEqual(c,self.map_reference_1.map_data[i][j])

    def test_serializeMap(self):
        serialized_map = self.map_test_1.serializeMap(self.client_positions,1,1)
        with open('tests/serveur/maps_de_test/carte_de_test_1.txt') as testFile:
            expected_result = testFile.read()
        self.assertEqual(serialized_map,expected_result)
