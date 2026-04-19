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

Middlebox1Emergency=False
Middlebox2Emergency=False



Midbox1Message='null'
Midbox2Message='null'
def RespondToMiddleBox(MiddleboxSocket,IsAccident):

    global Flag1
    global Flag2
    if (IsAccident):
        MiddleboxSocket.send('Accident'.encode())
        return True
    else:
        MiddleboxSocket.send('NonAccident'.encode())
        return True
    return False


def HandleMiddlebox(MiddleboxSocket,BoxNumber):
  global Middlebox1Emergency
  global Middlebox2Emergency
  global Flag1
  global Flag2
  print(BoxNumber)
  try:
    with MiddleboxSocket:
            #CameraSocket.send('Thank you for connecting'.encode()) 
            while True:
             #     print()
                  #Receive data indefinitely. 
                  data=MiddleboxSocket.recv(1024).decode()
                  print(data)
                  while (Middlebox1Emergency ==False and Middlebox2Emergency == False):
                     pass
                  if (BoxNumber==1 and Middlebox1Emergency):
                      RespondToMiddleBox(MiddleboxSocket,Flag1)
                      Flag1=0
                      Middlebox1Emergency=False
                      break
                  if (BoxNumber==2 and Middlebox2Emergency):
                      RespondToMiddleBox(MiddleboxSocket,Flag2)
                      Flag2=0
                      break

                      

  except Exception as e:
     print(e)
#Create server thread
def EmergencyCenterServer():
 global EmergencyCenterIP
 global EmercenyCenterPort
 boxnumber=1
 print(boxnumber)
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind(('', EmercenyCenterPort))         
            print ("socket binded to %s" %(EmercenyCenterPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                #Establish connection with middlebox
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr).split('.')
                  
                  if (AddressString[-1]=="1"):
                      boxnumber=1
                  elif(AddressString[-1]=="2"):
                      boxnumber=2
                  if(AddressString[2]!="0"):
                      pass
                  else:
                    print(boxnumber)
                    threading.Thread(target=HandleMiddlebox, args=(client,boxnumber,),daemon=True).start()
                    
 except:
     print("Base error")
     print("Error")
  # Breaking once connection closed

def EmergencyResponse(Caller):
    global Flag1
    global Flag2
    global Middlebox1Emergency
    global Middlebox2Emergency
    EmergencyString1='Emergency 1'
    EmergencyString2='Emergency 2'
    EmergencyString3='Emergency 3'
    EmergencyString4='Emergency 4'
    if (Caller==EmergencyString1 or Caller==EmergencyString2):
        print("Emergency")
        Middlebox1Emergency=True
        Flag1=1
    if (Caller==EmergencyString3 or Caller==EmergencyString4):
        Middlebox2Emergency=True
        Flag2=1
    
    
def NonEmergencyResponse(Caller):
    global Flag1
    global Flag2
    global Middlebox1Emergency
    global Middlebox2Emergency
    EmergencyString1='Emergency 1'
    EmergencyString2='Emergency 2'
    EmergencyString3='Emergency 3'
    EmergencyString4='Emergency 4'
    if (Caller==EmergencyString1 or Caller==EmergencyString2):
        Middlebox1Emergency=True
        Flag1=0
    if (Caller==EmergencyString3 or Caller==EmergencyString4):
        Middlebox2Emergency=True
        Flag2=0

          
def EmergencyGUI():
     print("RAN")
     GUI=GUIBase.EmergencyCenterGUI(EmergencyResponse,NonEmergencyResponse)
     print("RAN")

     threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()
EmergencyGUI()
threading.Thread(target=EmergencyCenterServer,args=(),daemon=False).start()
