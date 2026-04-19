import socket
import sys
import threading
import GUIBase
Localhost="127.0.0.1"
EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"

DataCenterPort=7777
DataCenterIP = "10.0.6.0"
Flag1=0
Flag2=0


def HandleMiddlebox(MiddleboxSocket,BoxNumber):
  global Middlebox1Emergency
  global Middlebox2Emergency
  global Flag1
  global Flag2
  try:
    with MiddleboxSocket:

            while True:
             #     print()
                  #Receive data indefinitely. 
                  data=MiddleboxSocket.recv(1024).decode()

  except Exception as e:
     print(e)
#Create server thread
def DataCenterServer():
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind(('', DataCenterPort))         
            print ("socket binded to %s" %(DataCenterPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                #Establish connection with middlebox
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr).split('.')
                  boxnumber=1
                  if (AddressString[-1]=="1"):
                      boxnumber=1
                  elif(AddressString[-1]=="2"):
                      boxnumber=2
                  elif(AddressString[2]!="4"):
                      pass
                  else:
                    threading.Thread(target=HandleMiddlebox, args=(client,boxnumber)).start()
 except Exception as e:
     print(e)
  # Breaking once connection closed


DataCenterServer()