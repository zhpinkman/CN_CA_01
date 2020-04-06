# import socket programming library
import socket
import json
import os

# import thread module
from _thread import *
import threading


config_data = None

BAD_SEQUENCE_OF_COMMANDS = '503 Bad sequence of commands.'
INVALID_USERNAME_PASSWORD = '403 Invalid username or password.'
USERNAME_OK = '331 User name okey, need password.'
LOGIN_OK = '230 User logged in, proceed.'
NOT_AUTHORIZED = '332 Need account for login.'
MAX_SIZE = 1024
SYNTAX_ERROR = '501 Syntax error in parameters or arguments.'


# print_lock = threading.Lock()

# thread function


def read_config_file():
    global config_data
    config_file = open('config.json')
    config_data = json.load(config_file)


def get_users():
    return config_data['users']


def find_user(user_name):
    for user in get_users():
        if user['user'] == user_name:
            return user
    return None


def threaded(c):
    logged_in = False
    user_username = None
    user = None
    while True:

        # data received from client
        data = (c.recv(1024)).decode()

        if not data:
            print('Bye')
            # lock released on exit
            # print_lock.release()
            break

        parsed_data = list(map(str, data.split()))
        if (not logged_in) and (parsed_data[0] not in ['USER', 'PASS']):
            c.send(NOT_AUTHORIZED.encode())
            continue
        if (not logged_in) and (parsed_data[0] in ['USER', 'PASS']):
            if not user_username:
                if parsed_data[0] != 'USER':
                    c.send(BAD_SEQUENCE_OF_COMMANDS.encode())
                    continue
                if parsed_data[1][0] != '<' or parsed_data[1][len(parsed_data[1]) - 1] != '>':
                    c.send(SYNTAX_ERROR.encode())
                input_username = parsed_data[1][1:len(parsed_data[1]) - 1]
                user = find_user(input_username)
                if not user:
                    c.send(INVALID_USERNAME_PASSWORD.encode())
                    continue
                user_username = user['user']
                c.send(USERNAME_OK.encode())
                continue
            else:
                if parsed_data[0] != 'PASS':
                    c.send(BAD_SEQUENCE_OF_COMMANDS.encode())
                    continue
                if parsed_data[1][0] != '<' or parsed_data[1][len(parsed_data[1]) - 1] != '>':
                    c.send(SYNTAX_ERROR.encode())
                input_password = parsed_data[1][1:len(parsed_data[1]) - 1]
                if input_password != user['password']:
                    c.send(INVALID_USERNAME_PASSWORD.encode())
                    continue
                c.send(LOGIN_OK.encode())
                logged_in = True
                continue
        if(logged_in):
            if parsed_data[0] == 'PWD':
                c.send(os.getcwd().encode())
                continue

                # reverse the given string from client

                # send back reversed string to client

                # connection closed
    c.close()


def Main():

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    read_config_file()
    Main()
