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


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


BAD_SEQUENCE_OF_COMMANDS = '503 Bad sequence of commands.'
INVALID_USERNAME_PASSWORD = '403 Invalid username or password.'
USERNAME_OK = '331 User name okey, need password.'
LOGIN_OK = '230 User logged in, proceed.'
NOT_AUTHORIZED = '332 Need account for login.'
MAX_SIZE = 1024
SYNTAX_ERROR = '501 Syntax error in parameters or arguments.'
FILE_EXISTED = '500 File or directory already existed in this path.'
FILE_NOT_EXISTED = '500 File or directory not existed in this path.'
NOT_DIRECTORY = '500 Not a directory.'
LIST_TRANSFER_DONE = '226 List transfer done.'
CWD_SUCCESS = '250 Successful Change.'


# print_lock = threading.Lock()

# thread function

class Client_handler:
    def __init__(self, client):
        self.base_dir = os.getcwd()
        self.curr_dir = self.base_dir
        self.logged_in = True
        self.username = None
        self.user = None
        self.client = client
        self.data_socket = None

    def validate_arg(self, arg):
        if arg[0] != '<' or arg[len(arg) - 1] != '>':
            raise Error(SYNTAX_ERROR)

    def receive_data_from_client(self):
        return (self.client.recv(MAX_SIZE)).decode()

    def end_connection(self, data):
        if not data:
            return True
        return False

    def check_for_previous_username(self):
        if self.username:
            raise Error(BAD_SEQUENCE_OF_COMMANDS)

    def get_neat_data(self, arg):
        return arg[1:len(arg) - 1]

    def send_message(self, message):
        self.client.send(message.encode())

    def close_connection(self):
        self.client.close()

    def check_for_existing_username(self):
        if (not self.username) or self.logged_in:
            raise Error(BAD_SEQUENCE_OF_COMMANDS)

    def handle_USER_command(self, arg):
        self.check_for_previous_username()
        self.validate_arg(arg[1])
        username = self.get_neat_data(arg[1])
        self.user = Utils().find_user(username)
        self.username = self.user['user']
        self.send_message(USERNAME_OK)

    def validate_password(self, password):
        if password != self.user['password']:
            raise Error(INVALID_USERNAME_PASSWORD)

    def handle_PASS_command(self, arg):
        self.check_for_existing_username()
        self.validate_arg(arg[1])
        password = self.get_neat_data(arg[1])
        self.validate_password(password)
        self.logged_in = True
        self.send_message(LOGIN_OK)

    def authenticate_user(self):
        if not self.logged_in:
            raise Error(NOT_AUTHORIZED)

    def handle_PWD_command(self):
        self.authenticate_user()
        self.send_message('257 <' + self.curr_dir + '>')

    def get_base_path(self):
        return Utils().get_diff_path(self.base_dir, self.curr_dir)

    def check_for_existing_file_or_dir(self, name):
        if os.path.exists(self.get_base_path() + name):
            raise Error(FILE_EXISTED)

    def make_dir(self, arg):
        self.validate_arg(arg)
        dir_name = self.get_neat_data(arg)
        self.check_for_existing_file_or_dir(dir_name)
        os.mkdir(self.get_base_path() + dir_name)
        self.send_message('257 <' + dir_name + '> created.')

    def validate_create_file_option(self, option):
        if option != '-i':
            raise Error(SYNTAX_ERROR)
        return True

    def make_file(self, arg):
        self.validate_arg(arg)
        file_name = self.get_neat_data(arg)
        self.check_for_existing_file_or_dir(file_name)
        open(self.get_base_path() + file_name, 'w+').close()
        self.send_message('257 <' + file_name + '> created.')

    def handle_MKD_command(self, args):
        self.authenticate_user()
        if len(args) == 2:
            self.make_dir(args[1])
        elif len(args) == 3 and self.validate_create_file_option(args[1]):
            self.make_file(args[2])

    def check_for_not_existing_file_or_dir(self, name):
        if not os.path.exists(self.get_base_path() + name):
            raise Error(FILE_NOT_EXISTED)

    def remove_file(self, arg):
        self.validate_arg(arg)
        file_name = self.get_neat_data(arg)
        self.check_for_not_existing_file_or_dir(file_name)
        os.remove(self.get_base_path() + file_name)
        self.send_message('257 <' + file_name + '> deleted.')

    def validate_remove_dir_option(self, option):
        if option != '-f':
            raise Error(SYNTAX_ERROR)
        return True

    def remove_dir(self, arg):
        self.validate_arg(arg)
        dir_name = self.get_neat_data(arg)
        self.check_for_not_existing_file_or_dir(dir_name)
        shutil.rmtree(self.get_base_path() + dir_name)
        self.send_message('257 <' + dir_name + '> deleted.')

    def handle_RMD_command(self, args):
        self.authenticate_user()
        if len(args) == 2:
            self.remove_file(args[1])
        elif len(args) == 3 and self.validate_remove_dir_option(args[1]):
            self.remove_dir(args[2])

    def initiate_data_connection(self, data_port):
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect(('', data_port))
        print(11)

    def close_data_connection(self):
        self.data_socket.close()

    def get_file_list(self, base_path):
        if not base_path:
            return pickle.dumps(os.listdir())
        else:
            return pickle.dumps(os.listdir(base_path))

    def send_data(self, data):
        self.data_socket.send(data)

    def handle_LIST_command(self, args):
        self.authenticate_user()
        client_data_port = int(args[1])
        self.initiate_data_connection(client_data_port)
        base_path = self.get_base_path()
        file_list = self.get_file_list(base_path)
        self.send_data(file_list)
        self.close_data_connection()
        self.send_message(LIST_TRANSFER_DONE)

    def go_to_prev_path(self):
        if self.base_dir != self.curr_dir:
            curr_dir_list = self.curr_dir.split('/')
            curr_dir_list.pop()
            self.curr_dir = '/'.join(curr_dir_list)
        self.send_message(CWD_SUCCESS)

    def go_to_path(self, target_dir):
        diff_path = self.get_base_path()
        if os.path.isdir(diff_path + target_dir):
            self.curr_dir += '/' + target_dir
            self.send_message(CWD_SUCCESS)
        else:
            self.send_message(NOT_DIRECTORY)

    def go_to_base_path(self):
        self.curr_dir = self.base_dir
        self.send_message(CWD_SUCCESS)

    def handle_CWD_command(self, args):
        self.authenticate_user()
        self.validate_arg(args[1])
        target_dir = self.get_neat_data(args[1])
        if not target_dir:
            self.go_to_base_path()
        elif target_dir == '..':
            self.go_to_prev_path()
        else:
            self.go_to_path(target_dir)


class Utils:
    def get_diff_path(self, base_dir, curr_dir):
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

    def read_config_file(self):
        global config_data
        config_file = open('config.json')
        config_data = json.load(config_file)

    def get_users(self):
        return config_data['users']

    def find_user(self, user_name):
        for user in self.get_users():
            if user['user'] == user_name:
                return user
        raise Error(INVALID_USERNAME_PASSWORD)

    def get_parsed_data(self, data):
        return list(map(str, data.split()))

    def get_command(self, data):
        return data[0]


def threaded(client_handler):
    while True:

        # data received from client
        received_data = client_handler.receive_data_from_client()

        if (client_handler.end_connection(received_data)):
            print('Bye')
            break

        parsed_data = Utils().get_parsed_data(received_data)

        command = Utils().get_command(parsed_data)

        try:
            if command == 'USER':
                client_handler.handle_USER_command(parsed_data)
            elif command == 'PASS':
                client_handler.handle_PASS_command(parsed_data)
            elif command == 'PWD':
                client_handler.handle_PWD_command()
            elif command == 'MKD':
                client_handler.handle_MKD_command(parsed_data)
            elif command == 'RMD':
                client_handler.handle_RMD_command(parsed_data)
            elif command == 'LIST':
                client_handler.handle_LIST_command(parsed_data)
            elif command == 'CWD':
                client_handler.handle_CWD_command(parsed_data)

        except Error as e:
            client_handler.send_message(e.message)

    client_handler.close_connection()


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
        start_new_thread(threaded, (Client_handler(c),))
    s.close()


if __name__ == '__main__':
    Utils().read_config_file()
    Main()
