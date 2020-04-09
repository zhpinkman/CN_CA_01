import logging
import traceback
from socket import *
import base64
import time


class Mail_sender:
    # def __init__(self, to_email, subject, body):
    #     self.to_email = to_email
    #     self.subject = subject
    #     self.body = body

    def send(self):
        try:
            msg = "\r\n fuck this shit"
            endmsg = "\r\n.\r\n"
            mailserver = ("mail.ut.ac.ir", 25)

            clientSocket = socket(AF_INET, SOCK_STREAM)

            clientSocket.connect(mailserver)

            received_message = clientSocket.recv(1024).decode()

            # print("Message after connection request:" + received_message)
            # if received_message[:3] != '220':
            #     print('220 reply not received from server.')
            heloCommand = 'EHLO mail\r\n'
            clientSocket.send(heloCommand.encode())

            received_message = clientSocket.recv(1024).decode()

            # print("Message after EHLO command:" + received_message)
            # if received_message[:3] != '250':
            #     print('250 reply not received from server.')

            # Info for username and password
            username = "zh.sourati"
            password = "Pinkpanter1377"
            base64_str = ("\x00" + username + "\x00" + password).encode()
            base64_str = base64.b64encode(base64_str)
            authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
            clientSocket.send(authMsg)
            recv_auth = clientSocket.recv(1024)
            # print(recv_auth.decode())

            mailFrom = "MAIL FROM:<zh.sourati@ut.ac.ir>\r\n"
            clientSocket.send(mailFrom.encode())

            received_message = clientSocket.recv(1024).decode()

            # print("After MAIL FROM command: " + received_message)
            rcptTo = "RCPT TO:<zh.sourati@ut.ac.ir>\r\n"
            clientSocket.send(rcptTo.encode())

            # print("After RCPT TO command: " + received_message)
            data = "DATA\r\n"
            clientSocket.send(data.encode())

            received_message = clientSocket.recv(1024).decode()

            # print("After DATA command: " + received_message)
            subject = "Subject: testing my client\r\n\r\n"
            clientSocket.send(subject.encode())
            date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            date = date + "\r\n\r\n"
            clientSocket.send(date.encode())
            clientSocket.send(msg.encode())
            clientSocket.send(endmsg.encode())
            recv_msg = clientSocket.recv(1024)
            # print("Response after sending message body:" + recv_msg.decode())
            quit = "QUIT\r\n"
            clientSocket.send(quit.encode())

            received_message = clientSocket.recv(1024).decode()

            # print(received_message)
            clientSocket.close()

        except Exception:
            logging.error(traceback.format_exc())



Mail_sender().send()