# Import socket module
import socket
import pickle


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    data_port = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', data_port))
    data_socket.listen(5)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    print("starting mail server")

    while True:

        data = input()
        if not data:
            break

            # message sent to server

        if data == 'LIST':
            s.send('LIST 65432'.encode())
        else:
            s.send(data.encode())

        parsed_data = list(map(str, data.split()))
        if parsed_data[0] == 'LIST':
            server_socket, server_addr = data_socket.accept()
            data_recvd = server_socket.recv(1024)
            print(pickle.loads(data_recvd))
            data_socket.close()

        # messaga received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print(data.decode())

        # ask the client whether he wants to continue
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
