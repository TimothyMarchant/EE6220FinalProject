"""
By Timothy Marchant

This program is very simple.  all it does is handle connection requests with the middlebox.  It accepts constant traffic from them.

Don't remember which site I specifically followed TCP examples from (I think stackoverflow?)
e.g. you don't want image data to get lost, corrupted or arrive out of order.

"""
#import libaries.
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
  '''
  This function establishes the middlebox socket to run indefinitely.
  '''
  try:
    with MiddleboxSocket:

            while True:
                  #Receive data indefinitely. 
                  data=MiddleboxSocket.recv(1024).decode()

  except Exception as e:
     print(e)
     

def DataCenterServer():
  '''
  This function creates a TCP socket for listening on the DataCenter ports
  defined in the topology. The socket is set up to listen until terminated.
  '''
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
                    threading.Thread(target=HandleMiddlebox, args=(client,),daemon=False).start()
  except Exception as e:
     print(e)

#Call the DataCenterServer function which then greats the threads for handle Middlebox
#Essentially this is the "main" section of the code
DataCenterServer()
