import socket
#import GUIBase
import sys
Arguments = sys.argv[1:]

if (len(Arguments)!=3):
   print("Incorrect number of arguments")
   exit()

# first of all import the socket library 
import threading         

# next create a socket object 

#portnumber 

MiddleboxPort = 9999

EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"

DataCenterPort=7777
DataCenterIP = "10.0.6.0"

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
          

# a forever loop until we interrupt it or 
# an error occurs
def CheckImage(Image):
   print(Image)
def CameraConnection(CameraSocket):
  try:
    with CameraSocket:
            #CameraSocket.send('Thank you for connecting'.encode()) 
            while True:
             #     print()
                  #Receive data indefinitely. 
                  data=CameraSocket.recv(1024).decode()
                  CameraSocket.send('a'.encode())

  except Exception as e:
     print(e)

#ListeningSocket = socket.socket()         
#print ("Socket successfully created")


#Create server thread
def MiddleboxServer():
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind(('', MiddleboxPort))         
            print ("socket binded to %s" %(MiddleboxPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 

# Establish connection with client. 
            #print()
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr).split('.')

                  threading.Thread(target=CameraConnection, args=(client,)).start()
 except:
     print("Base error")
     print("Error")
  # Breaking once connection closed
def EmergencyLogic(Caller):
     print("MiddleboxEmergency")
     EmergenyCenterPort = 7777                
     EmergencyCenterIP="10.0.5.0"
     try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as EmergencySocket:
          while True:
            EmergencySocket.connect((EmergencyCenterIP,EmergenyCenterPort))
            EmergencyString='Accident detected at '+(Caller)
            EmergencySocket.send(EmergencyString.encode())
            Response=EmergencySocket.recv(1024).decode
            print(Response)
            if (Response == 'Accident'):
                pass
            elif (Response == 'NonAccident'):
                break



     except:
         print("error")

          
def MiddleboxGUI():
     global Arguments
     Title=Arguments[0]
     Camera1=Arguments[1]
     Camera2=Arguments[2]
     print("RAN")
     GUI=GUIBase.Middlebox_GUI(Title,Camera1,Camera2,EmergencyLogic,EmergencyLogic)
     print("RAN")

     threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()

MiddleboxServer()
#MiddleboxGUI()
