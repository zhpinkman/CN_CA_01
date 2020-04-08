from defines import *


class Socket_handler:

    def __init__(self, client):
        pass

    def receive_data_from_client(self):
        return (self.client.recv(MAX_SIZE)).decode()
