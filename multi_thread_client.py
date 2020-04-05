# Import socket module
import socket
import json


bad_sequence_of_commands = '503 Bad sequence of commands.'
invalid_username_or_pass = '403 Invalid username or password.'
username_ok = '331 User name okey, need password.'
login_ok = '230 User logged in, proceed.'


config_data = None
logged_in = False


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


def login():
    username_inputs = list(map(str, input().split()))
    if (username_inputs[0] != 'USER'):
        print(bad_sequence_of_commands)
        return 0
    user_name = username_inputs[1][1:len(username_inputs[1]) - 1]
    user = find_user(user_name)
    if not user:
        print(invalid_username_or_pass)
        return 0
    password_inputs = list(map(str, input().split()))
    if (password_inputs[0] != 'PASS'):
        print(bad_sequence_of_commands)
        return 0
    password = password_inputs[1][1:len(password_inputs[1]) - 1]
    if password != user['password']:
        print(invalid_username_or_pass)
        return 0
    print(login_ok)


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    print("starting mail server")

    message = "zhivar mohsen"

    while True:

        if (not logged_in):
            print('pls login')
            login()

        # message sent to server
        s.send(message.encode('ascii'))

        # messaga received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('ascii')))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')

        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()


if __name__ == '__main__':
    read_config_file()
    Main()
