"""
By Timothy Marchant

All this program does is send data forever to the middleboxes.  
There is a slight delay between transmissions due to performance problems with mininet.

Don't remeber which sight I specifically followed TCP examples from (I think stackoverflow?)
"""
import socket
import time
import sys
#take middlebox IP address.
IpAddress=sys.argv[1]
#check for correct number of arguments.
if (len(sys.argv)!=2):
   exit()
#middlebox port number
MiddleboxPort = 9999
try:
    #create TCP client.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as CameraSocket:
        CameraSocket.connect((IpAddress,MiddleboxPort))
        #Inform that there is a connection.
        print("Connected")
        #send data forever.
        while True:
            #dummy data to send.
            CameraSocket.send('Send this string a bunch'.encode())
            #sleep to prevent overloading performance.
            time.sleep(0.01)
#Print error.
except Exception as e:
    print(e)

exit()

