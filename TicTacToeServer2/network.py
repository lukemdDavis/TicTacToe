import socket
import pickle


class Network:
    """
    This class sends information between clients and the server

    Attributes:
        client: socket
            A socket for the connection
        server: str
            The location the server will be hosted
        port: int
            The port specific for this network
        address: tuple
            A tuple consisting of the server and port
        p : int
            The id of the player it's connected to
    """
    def __init__(self):
        """
        client: socket
            A socket for the connection
        server: str
            The location the server will be hosted based on IPv4
        port: int
            The port specific for this network
        address: tuple
            A tuple consisting of the server and port
        p : int
            The id of the player it's connected to
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 6000
        self.address = (self.server, self.port)
        self.p = self.connect()

    def get_player(self):
        """Returns the players id"""
        return self.p

    def connect(self):
        """
        Try's to receive the players id if it exists

        Raises
        ------
        ConnectionError
            If there is no client to connect to an exception is raised and caught to avoid
            the program terminating
        """
        try:
            self.client.connect(self.address) # Connecting to the server
            return self.client.recv(2048).decode() # Receiving the player id
        except Exception as e:
            print(e)
            pass

    def send(self, data):
        """
        Sends data using the pickle library to the server
        :param data: The information to send
        :return: An object of information given as the response from the server

        :raises socket.error: Occurs when it can't connect to the client
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 10))
        except socket.error as e:
            print(e)
