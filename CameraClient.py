import socket
import time
import sys

MiddleboxIP = "10.0.4.1"
Localhost="127.0.0.1"
MiddleboxPort = 9999
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as CameraSocket:
        CameraSocket.connect((Localhost,MiddleboxPort))
        while True:
            CameraSocket.send('Send this string a bunch'.encode())
            #time.sleep(0.1)
            #CameraSocket.recv(1024).decode()

except socket.error as err:
    print(err)
except:
    exit()
#s.connect(Localhost,MiddleboxPort)

#s.send('message'.encode())

#print (s.recv(1024).decode)
