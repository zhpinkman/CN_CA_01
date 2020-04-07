from defines import *
from Utils import Utils
from Error import Error


# thread function
def threaded(client_handler):
    while True:

        # data received from client
        received_data = client_handler.receive_data_from_client()

        if client_handler.end_connection(received_data):
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
            elif command == 'QUIT':
                client_handler.handle_QUIT_command()
            else:
                raise Error(UNKNOWN_COMMAND)

        except Error as e:
            client_handler.send_message(e.message)

    client_handler.close_connection()
