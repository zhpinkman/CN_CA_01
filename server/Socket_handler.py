import pickle

from defines import *
import socket
from Error import Error

class Socket_handler:

    def __init__(self, client):
        pass

    @staticmethod
    def upload_file(file_path, data_port):
        print("Start Sending '" + file_path + "' To " + str(data_port))
        data_socket = Socket_handler.initiate_data_connection(data_port)
        try:
            f = open(file_path, 'rb')
        except:
            data_socket.close()
            raise Error(FILE_NOT_EXISTED)

        chunk = f.read()
        data_socket.send(pickle.dumps(chunk))

        # chunk = f.read(1024)
        # counter = 0
        # while chunk:
        #     counter += 1
        #     print("Sending chunk " + str(counter))
        #     data_socket.send(pickle.dumps(chunk))
        #     chunk = f.read(1024)

        data_socket.close()

    @staticmethod
    def initiate_data_connection(data_port):
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((IP, data_port))
        return data_socket