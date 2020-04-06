# import socket programming library
import socket
import json
import os
import shutil
import pickle

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
FILE_EXISTED = '500 File or directory already existed in this path.'
FILE_NOT_EXISTED = '500 File or directory not existed in this path.'
NOT_DIRECTOR = '500 Not a directory.'
LIST_TRANSFER_DONE = '226 List transfer done.'
CWD_SUCCESS = '250 Successful Change.'


# print_lock = threading.Lock()

# thread function

def get_diff_path(base_dir, curr_dir):
    base_dir_list = base_dir.split('/')
    curr_dir_list = curr_dir.split('/')
    result_dir_list = []
    for path in curr_dir_list:
        if path not in base_dir_list:
            result_dir_list.append(path)
    result_dir = '/'.join(result_dir_list)
    if result_dir:
        return result_dir + '/'
    return result_dir


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
    base_dir = os.getcwd()
    curr_dir = base_dir
    logged_in = True
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
                    continue
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
                    continue
                input_password = parsed_data[1][1:len(parsed_data[1]) - 1]
                if input_password != user['password']:
                    c.send(INVALID_USERNAME_PASSWORD.encode())
                    continue
                c.send(LOGIN_OK.encode())
                logged_in = True
                continue
        if(logged_in):
            if parsed_data[0] == 'PWD':
                c.send(('257 <' + curr_dir + '>').encode())
                continue
            if parsed_data[0] == 'MKD':
                if len(parsed_data) == 2:
                    if parsed_data[1][0] != '<' or parsed_data[1][len(parsed_data[1]) - 1] != '>':
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    dir_name = parsed_data[1][1:len(parsed_data[1]) - 1]
                    if os.path.exists(dir_name):
                        c.send(FILE_EXISTED.encode())
                        continue
                    os.mkdir(dir_name)
                    c.send(('257 <' + dir_name + '> created.').encode())
                    continue

                elif len(parsed_data) == 3:
                    if parsed_data[1] != '-i':
                        print('1')
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    if parsed_data[2][0] != '<' or parsed_data[2][len(parsed_data[2]) - 1] != '>':
                        print(2)
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    file_name = parsed_data[2][1:len(parsed_data[2]) - 1]
                    if os.path.exists(file_name):
                        c.send(FILE_EXISTED.encode())
                        continue
                    open(file_name, 'w+').close()
                    c.send(('257 <' + file_name + '> created.').encode())
                    continue
            if parsed_data[0] == 'RMD':
                if len(parsed_data) == 2:
                    if parsed_data[1][0] != '<' or parsed_data[1][len(parsed_data[1]) - 1] != '>':
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    file_name = parsed_data[1][1:len(parsed_data[1]) - 1]
                    if not os.path.exists(file_name):
                        c.send(FILE_NOT_EXISTED.encode())
                        continue
                    os.remove(file_name)
                    c.send(('257 <' + file_name + '> deleted.').encode())
                    continue

                elif len(parsed_data) == 3:
                    if parsed_data[1] != '-f':
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    if parsed_data[2][0] != '<' or parsed_data[2][len(parsed_data[2]) - 1] != '>':
                        c.send(SYNTAX_ERROR.encode())
                        continue
                    dir_name = parsed_data[2][1:len(parsed_data[2]) - 1]
                    if not os.path.exists(dir_name):
                        c.send(FILE_NOT_EXISTED.encode())
                        continue
                    shutil.rmtree(dir_name)
                    c.send(('257 <' + dir_name + '> deleted.').encode())
                    continue
            if parsed_data[0] == 'LIST':
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect(('', int(parsed_data[1])))
                diff_path = get_diff_path(base_dir, curr_dir)
                if not diff_path:
                    data_socket.send(pickle.dumps(os.listdir()))
                else:
                    data_socket.send(pickle.dumps(os.listdir(diff_path)))
                data_socket.close()
                c.send(LIST_TRANSFER_DONE.encode())
                continue
            if parsed_data[0] == 'CWD':
                if parsed_data[1][0] != '<' or parsed_data[1][len(parsed_data[1]) - 1] != '>':
                    c.send(SYNTAX_ERROR.encode())
                    continue
                target_dir = parsed_data[1][1:len(parsed_data[1]) - 1]
                if not target_dir:
                    curr_dir = base_dir
                    c.send(CWD_SUCCESS.encode())
                    continue
                elif target_dir == '..':
                    if base_dir != curr_dir:
                        curr_dir_list = curr_dir.split('/')
                        curr_dir_list.pop()
                        curr_dir = '/'.join(curr_dir_list)
                    c.send(CWD_SUCCESS.encode())
                    continue
                else:
                    diff_path = get_diff_path(base_dir, curr_dir)
                    print(diff_path + target_dir)
                    if os.path.isdir(diff_path + target_dir):
                        curr_dir += '/' + target_dir
                        c.send(CWD_SUCCESS.encode())
                        continue
                    else:
                        c.send(NOT_DIRECTOR.encode())
                        continue

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
