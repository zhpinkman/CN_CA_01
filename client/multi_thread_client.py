# Import socket module
import socket
import pickle
import sys
import select
from Utils import Utils


def main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = Utils().get_command_channel_port()
    data_port = Utils().get_data_channel_port()

    command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_lists = [sys.stdin, command_socket, data_socket]

    data_socket.bind(('', data_port))
    data_socket.listen(5)

    # connect to server on local computer
    command_socket.connect((host, port))

    # message you send to server
    print("starting mail server")

    while True:

        try:
            read_sockets, write_sockets, error_sockets = select.select(socket_lists, [], [])

            for sock in read_sockets:
                if sock is sys.stdin:
                    data = sys.stdin.readline()
                    if not data:
                        command_socket.close()
                        data_socket.close()
                        return
                    elif data == 'LIST\n':
                        command_socket.send(('LIST ' + str(data_port)).encode())
                    else:
                        command_socket.send(data.encode())
                elif sock is command_socket:
                    data = sock.recv(1024)
                    print(data.decode())
                elif sock is data_socket:
                    server_socket, server_addr = sock.accept()
                    socket_lists.append(server_socket)
                else:
                    data_recvd = sock.recv(1024)
                    print(pickle.loads(data_recvd))
                    socket_lists.remove(sock)
                    sock.close()

        except:
            print("Exiting")
            break

    # close the connection
    command_socket.close()
    data_socket.close()


if __name__ == '__main__':
    Utils().read_config_file()
    main()
