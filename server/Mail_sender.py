import logging
import traceback
from socket import *
import base64
import time
import ssl
from Logger import Logger
import smtplib


class Mail_sender:

    def __init__(self, to_email, subject, body, using_ssl):
        self.to_email = to_email
        self.subject = subject
        self.body = body
        self.using_ssl = using_ssl

    def get_normal_socket(self):
        return socket(AF_INET, SOCK_STREAM)

    def get_ssl_socket(self):
        return ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))

    def get_mail_server(self):
        return ("mail.ut.ac.ir", 465), "zh.sourati", "Pinkpanter1377", "@ut.ac.ir"
        # return ("mail.mahfell.com", 587), "fayyaz", "1qaz!QAZ", "@mahfell.com"

    def send(self):
        try:
            msg = "\r\n" + self.body
            end_msg = "\r\n.\r\n"
            mail_server, username, password, domain = self.get_mail_server()

            if self.using_ssl:
                client_socket = self.get_ssl_socket()
            else:
                client_socket = self.get_normal_socket()

            client_socket.connect(mail_server)

            received_message = client_socket.recv(1024).decode()

            # print("Message after connection request:" + received_message)
            # if received_message[:3] != '220':
            #     print('220 reply not received from server.')
            helo_command = 'EHLO mail\r\n'
            client_socket.send(helo_command.encode())

            received_message = client_socket.recv(1024).decode()

            # print("Message after EHLO command:" + received_message)
            # if received_message[:3] != '250':
            #     print('250 reply not received from server.')

            # Info for username and password

            base64_str = ("\x00" + username + "\x00" + password).encode()
            base64_str = base64.b64encode(base64_str)
            auth_msg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
            client_socket.send(auth_msg)
            recv_auth = client_socket.recv(1024)
            # print(recv_auth.decode())

            mail_from = "MAIL FROM:<" + username + domain + ">\r\n"
            client_socket.send(mail_from.encode())

            received_message = client_socket.recv(1024).decode()

            # print("After MAIL FROM command: " + received_message)
            rcpt_to = "RCPT TO:<" + self.to_email + ">\r\n"
            client_socket.send(rcpt_to.encode())

            # print("After RCPT TO command: " + received_message)
            data = "DATA\r\n"
            client_socket.send(data.encode())

            received_message = client_socket.recv(1024).decode()

            # print("After DATA command: " + received_message)
            subject = "Subject: " + self.subject + "\r\n\r\n"
            client_socket.send(subject.encode())
            date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
            date = date + "\r\n\r\n"
            client_socket.send(date.encode())
            client_socket.send(msg.encode())
            client_socket.send(end_msg.encode())
            recv_msg = client_socket.recv(1024)
            # print("Response after sending message body:" + recv_msg.decode())
            quit = "QUIT\r\n"
            client_socket.send(quit.encode())

            received_message = client_socket.recv(1024).decode()
            try:
                Logger.log("Mail service sent an email to " + self.to_email + " about " + self.subject)
            except Exception:
                print("Mail service sent an email to " + self.to_email + " about " + self.subject)
            # print(received_message)
            client_socket.close()

        except Exception:
            logging.error(traceback.format_exc())


# Mail_sender("zh.sourati@ut.ac.ir", "testing mail sender module", "another message is going to change your life.",
#             False).send()
#
Mail_sender("mohsen.fayyaz77@ut.ac.ir", "testing mail sender module", "another message is going to change your life.",
            True).send()

# try:
#     server = smtplib.SMTP_SSL('mail.ut.ac.ir:465')
#     server.starttls()
#     print("Successfully sent email")
# except smtplib.SMTPException:
#     print("Error: unable to send email")
