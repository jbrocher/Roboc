#--encoding=utf-8--

from lib.serveur.Interface import Interface

interface = Interface()

try:
    interface.loadMaps()
    interface.displayMaps()
    interface.setUp()
    interface.display()
    winners = []

    while winners == []:

        winners = interface.processCommands()

    interface.endGame(winners)
except:
    interface.endGame([])
