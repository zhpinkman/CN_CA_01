import logging
import telnetlib as telnet
import base64
import traceback


class Mail_sender:
    def __init__(self, to_email, subject, body):
        self.to_email = to_email
        self.subject = subject
        self.body = body

    def send(self):
        try:
            tn = telnet.Telnet('mail.ut.ac.ir', 25)
            tn.read_until("220 mail.ut.ac.ir".encode())
            tn.write('helo mail\n'.encode())
            tn.read_until('250 mail.ut.ac.ir'.encode())
            tn.write(('auth plain ' + base64.b64encode(
                ("\x00" + "zh.sourati" + "\x00" + "Pinkpanter1377").encode()).decode() + '\n').encode())
            tn.read_until('235 2.7.0 Authentication successful'.encode())
            tn.write('mail from: <zh.sourati@ut.ac.ir>\n'.encode())
            tn.read_until('250 2.1.0 Ok'.encode())
            tn.write(('rcpt to: <' + self.to_email + '>\n').encode())
            tn.read_until('250 2.1.5 Ok'.encode())
            tn.write('data\n'.encode())
            tn.read_until('354 End data with <CR><LF>.<CR><LF>'.encode())
            tn.write(('Subject: ' + self.subject + '\n' + self.body + '\n' + '.' + "\n").encode())
            tn.read_until('250 2.0.0 Ok:'.encode())
            tn.write('quit\n'.encode())
        except Exception:
            logging.error(traceback.format_exc())

    def zhivar_old_code(self):
        tn = telnet.Telnet('mail.ut.ac.ir', 25)
        tn.read_until("220 mail.ut.ac.ir".encode())
        tn.write('helo mail\n'.encode())
        tn.read_until('250 mail.ut.ac.ir'.encode())
        tn.write(('auth plain ' + base64.b64encode(
            ("\x00" + "zh.sourati" + "\x00" + "Pinkpanter1377").encode()).decode() + '\n').encode())
        tn.read_until('235 2.7.0 Authentication successful'.encode())
        tn.write('mail from: <zh.sourati@ut.ac.ir>\n'.encode())
        tn.read_until('250 2.1.0 Ok'.encode())
        tn.write('rcpt to: <zh.sourati@ut.ac.ir>\n'.encode())
        tn.read_until('250 2.1.5 Ok'.encode())
        tn.write('data\n'.encode())
        tn.read_until('354 End data with <CR><LF>.<CR><LF>'.encode())
        tn.write(
            ('Subject: Test email' + '\n' + 'Hi, This is a test.txt message.Regards,Me' + '\n' + '.' + "\n").encode())
        tn.read_until('250 2.0.0 Ok:'.encode())
        tn.write('quit\n'.encode())
