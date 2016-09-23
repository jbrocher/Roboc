from threading import Thread


class ClientInterface(Thread):


    cont = True
    msg_recu =""
    def __init__(self):

        Thread.__init__(self)
