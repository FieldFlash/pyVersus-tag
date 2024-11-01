import socket # importing socket to bind to the server's IP and Port
import pickle # importing pickle to serialize the client't player data and send it to the server

class Network:
    '''Network Class for information grabbing and sending'''
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()


    def getP(self):
        '''Getter for returning the position of your player'''
        return self.p

    def connect(self):
        '''Binds to the server and returns the starting object data'''
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        '''Sends player data and returns player2 data'''
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)