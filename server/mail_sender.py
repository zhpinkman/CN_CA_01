import telnetlib as telnet
import base64

tn = telnet.Telnet('mail.ut.ac.ir', 25)

tn.read_until("220 mail.ut.ac.ir".encode())


tn.write('helo mail\n'.encode())


tn.read_until('250 mail.ut.ac.ir'.encode())

tn.write(('auth plain ' + base64.b64encode(("\x00" + "zh.sourati" + "\x00" + "Pinkpanter1377").encode()).decode() + '\n').encode())


tn.read_until('235 2.7.0 Authentication successful'.encode())

tn.write('mail from: <zh.sourati@ut.ac.ir>\n'.encode())

tn.read_until('250 2.1.0 Ok'.encode())

tn.write('rcpt to: <zh.sourati@ut.ac.ir>\n'.encode())

tn.read_until('250 2.1.5 Ok'.encode())

tn.write('data\n'.encode())

tn.read_until('354 End data with <CR><LF>.<CR><LF>'.encode())


tn.write(('Subject: Test email' + '\n' + 'Hi, This is a test message.Regards,Me' + '\n' + '.' + "\n").encode())


tn.read_until('250 2.0.0 Ok:'.encode())

tn.write('quit\n'.encode())

