#--encoding=utf-8--

from lib.serveur.Interface import Interface

interface = Interface()

try:
    interface.loadMaps()
    interface.displayMaps()
    interface.setUp()

    winners = []

    while winners == []:

        winners = interface.processCommands()
        interface.display()
    interface.endGame(winners)
except Exception as exception:
    interface.endGame([])
    print(exception.message())
