"""
By Timothy Marchant

This program is very simple.  all it does is handle connection requests with the middlebox.  It accepts constant traffic from them.

Don't remeber which sight I specifically followed TCP examples from (I think stackoverflow?)

"""

import socket
#For handling multiple sockets.
import threading
#Connection related definitions.
Localhost="127.0.0.1"
EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"

DataCenterPort=7777
DataCenterIP = "10.0.6.0"

###Handle middlebox socket to take data indefinitely.
def HandleMiddlebox(MiddleboxSocket):

  try:
    with MiddleboxSocket:

            while True:
                  #Receive data indefinitely. 
                  data=MiddleboxSocket.recv(1024).decode()

  except Exception as e:
     print(e)
#Create server
def DataCenterServer():
 global DataCenterIP
 global DataCenterPort
 try:
      #setup TCP socket.
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind((DataCenterIP, DataCenterPort))         
            print ("socket binded to %s" %(DataCenterPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  
            #listen forever.
            while True: 
                #Establish connection with middlebox
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr).split('.')
                  if(AddressString[2]!="4"):
                      pass
                  else:
                    #pass socket to seperate thread for processing it.
                    threading.Thread(target=HandleMiddlebox, args=(client)).start()
 except Exception as e:
     print(e)


DataCenterServer()
