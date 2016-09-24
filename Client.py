#--encoding=utf-8--
from lib.client.Receive import Receive
from lib.client.Send import Send
from lib.client.ClientInterface import ClientInterface
import socket


try:
    with open("welcome_screen","r") as welcome_screen_file:
        welcome = welcome_screen_file.read()

    print(welcome)
    input("appuyez sur enter commencer")
    hote = "localhost"
    port = 12800
    end = ""
    my_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_Socket.connect((hote, port))
    print("Connexion établie avec le serveur sur le port {}".format(port))

    send_thread = Send(my_Socket)
    receive_thread = Receive(my_Socket)

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()
    my_Socket.send(b"end")


except:
    ClientInterface.cont = False
    send_thread.join()
    receive_thread.join()
    print("oups, un problème est survenu, aurevoir!")
