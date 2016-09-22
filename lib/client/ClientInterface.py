from threading import Thread


class ClientInterface(Thread):

    end_threads = False
    def __init__(self):

        Thread.__init__(self)
