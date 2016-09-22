#--encoding=utf-8--
"""Module qui définie la class Map"""
class Map:
    """ Objet correspondant à une carte. possède les attributs correspondant
    à la position initale du joueur sur la carte, et les limites de la carte"""

    def __init__(self,map_name = None):
        """ lit le fichier map et construit l'objet Map correspondant"""
        self.i_init = 0
        self.j_init=0
        self.i_max = 0
        self.j_max = 0
        self.map_data = ()
        self.map_name=""
        if map_name != None:
            self.map_name = map_name[:len(map_name)-4]

            deserialize_map = []
            possible_chars = ['O',' ','X', 'U', '.']
            with open("maps/{}".format(map_name),"r") as myMap:
                current_line = myMap.readline()
                i = 0

                while current_line != "":
                    j=0
                    clean_line = ""
                    for c in current_line:

                        if c in possible_chars:

                            if c == 'X':


                                clean_line = clean_line + "_"
                                self.i_init = i
                                self.j_init = j
                            else:
                                clean_line = clean_line + c
                        j = j+1

                    deserialize_map.append(tuple(clean_line[0:len(clean_line)]))

                    current_line = myMap.readline()
                    i = i+1

            deserialize_map = tuple(deserialize_map)



            self.map_data = deserialize_map
            self.i_max = len(self.map_data)
            self.j_max = len(self.map_data[0])


    def modifyMap(self,i,j,c):

        line = self.map_data(i)
        map_l = list(self.map_data)
        line_l = list(line)
        line_l[j] = c
        map_l[i] = tuple(line_l)
        self.map_data = tuple(map_l)







    def serializeMap(self,client_positions,i,j):
        """ renvoie une string représentant la map, avec un X à la position(i,j)
        """
        result = ""
        for k,line in enumerate(self.map_data):
            for l,c in enumerate(line):
                if k == i and l == j:
                    result += 'X'
                elif (k,l) in client_positions:
                    result+='x'
                else:
                    result += c
            result += '\n'
        return result
