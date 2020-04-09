import socket
from _thread import *
from threaded import threaded
from Client_handler import Client_handler
from Utils import Utils
from Accounting_handler import Accounting_handler

config_data = None


# print_lock = threading.Lock()

def main():
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = Utils().get_command_channel_port()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        try:
            c, addr = s.accept()

            # lock acquired by client
            # print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            start_new_thread(threaded, (Client_handler(c),))
        except:
            print("Exiting")
            break

    print("Closing socket")
    s.close()


if __name__ == '__main__':
    Utils().read_config_file()
    Accounting_handler().start()
    main()
