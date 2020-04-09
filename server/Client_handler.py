import socket
import os
import shutil
import struct

from File_handler import File_handler
from defines import *
from Utils import Utils
from Error import Error
from Socket_handler import Socket_handler


class Client_handler:

    # private methods

    def __init__(self, client):
        self.base_dir = os.getcwd()
        self.curr_dir = self.base_dir
        self.logged_in = False
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

    def remove_command_signs(self, arg):
        return arg[1:len(arg) - 1]

    def send_message(self, message):
        self.client.send(message.encode())

    def close_connection(self):
        self.client.close()

    def check_for_existing_username(self):
        if (not self.username) or self.logged_in:
            raise Error(BAD_SEQUENCE_OF_COMMANDS)

    def validate_password(self, password):
        if password != self.user['password']:
            raise Error(INVALID_USERNAME_PASSWORD)

    def authenticate_user(self):
        if not self.logged_in:
            raise Error(NOT_AUTHORIZED)
        return True

    def get_base_path(self):
        return Utils().get_diff_path(self.base_dir, self.curr_dir)

    def check_for_existing_file_or_dir(self, name):
        if os.path.exists(self.get_base_path() + name):
            raise Error(FILE_EXISTED)

    def make_dir(self, arg):
        self.validate_arg(arg)
        dir_name = self.remove_command_signs(arg)
        self.check_for_existing_file_or_dir(dir_name)
        os.mkdir(self.get_base_path() + dir_name)
        self.send_message('257 <' + dir_name + '> created.')

    def validate_create_file_option(self, option):
        if option != '-i':
            raise Error(SYNTAX_ERROR)
        return True

    def make_file(self, arg):
        self.validate_arg(arg)
        file_name = self.remove_command_signs(arg)
        self.check_for_existing_file_or_dir(file_name)
        open(self.get_base_path() + file_name, 'w+').close()
        self.send_message('257 <' + file_name + '> created.')

    def check_for_not_existing_file_or_dir(self, name):
        if not os.path.exists(self.get_base_path() + name):
            raise Error(FILE_NOT_EXISTED)

    def remove_file(self, arg):
        self.validate_arg(arg)
        file_name = self.remove_command_signs(arg)
        self.check_for_not_existing_file_or_dir(file_name)
        try:
            os.remove(self.get_base_path() + file_name)
            self.send_message('250 <' + file_name + '> deleted.')
        except:
            raise Error(FILE_NOT_EXISTED)

    def validate_remove_dir_option(self, option):
        if option != '-f':
            raise Error(SYNTAX_ERROR)
        return True

    def remove_dir(self, arg):
        self.validate_arg(arg)
        dir_name = self.remove_command_signs(arg)
        self.check_for_not_existing_file_or_dir(dir_name)
        try:
            shutil.rmtree(self.get_base_path() + dir_name)
            self.send_message('250 <' + dir_name + '> deleted.')
        except:
            raise Error(FILE_NOT_EXISTED)

    def initiate_data_connection(self, data_port):
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.connect(('127.0.0.1', data_port))
        l_onoff = 1
        l_linger = 10
        self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                                    struct.pack('ii', l_onoff, l_linger))

    def close_data_connection(self):
        self.data_socket.close()

    def send_data(self, data):
        self.data_socket.send(data)

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

    # public methods

    def handle_USER_command(self, arg):
        self.check_for_previous_username()
        self.validate_arg(arg[1])
        username = self.remove_command_signs(arg[1])
        self.user = Utils().find_user(username)
        self.username = self.user['user']
        self.send_message(USERNAME_OK)

    def handle_PASS_command(self, arg):
        self.check_for_existing_username()
        self.validate_arg(arg[1])
        password = self.remove_command_signs(arg[1])
        self.validate_password(password)
        self.logged_in = True
        self.send_message(LOGIN_OK)

    def handle_PWD_command(self):
        # self.authenticate_user()
        self.send_message('257 <' + self.curr_dir + '>')

    def handle_MKD_command(self, args):
        # self.authenticate_user()
        if len(args) == 2:
            self.make_dir(args[1])
        elif len(args) == 3 and self.validate_create_file_option(args[1]):
            self.make_file(args[2])

    def handle_RMD_command(self, args):
        # self.authenticate_user()
        if len(args) == 2:
            self.remove_file(args[1])
        elif len(args) == 3 and self.validate_remove_dir_option(args[1]):
            self.remove_dir(args[2])

    def handle_LIST_command(self, args):
        # self.authenticate_user()
        client_data_port = int(args[1])
        self.initiate_data_connection(client_data_port)
        base_path = self.get_base_path()
        file_list = File_handler.get_directory_files_list(base_path)
        self.send_data(file_list)
        self.close_data_connection()
        self.send_message(LIST_TRANSFER_DONE)

    def handle_CWD_command(self, args):
        # self.authenticate_user()
        target_dir = None
        if len(args) > 1:
            self.validate_arg(args[1])
            target_dir = self.remove_command_signs(args[1])
        if target_dir is None:
            self.go_to_base_path()
        elif target_dir == '..':
            self.go_to_prev_path()
        else:
            self.go_to_path(target_dir)

    def handle_QUIT_command(self):
        # self.authenticate_user()
        self.username = None
        self.user = None
        self.logged_in = False
        self.send_message(QUIT_OK)

    def handle_DL_command(self, args):
        if len(args) != 2:
            raise Error(SYNTAX_ERROR)
        else:
            self.validate_arg(args[1])
            file_name = self.remove_command_signs(args[1])
            file_path = self.curr_dir + "/" + file_name
            Socket_handler.upload_file(file_path, Utils().get_data_channel_port())
            self.send_message(SUCCESSFUL_DOWNLOAD)
