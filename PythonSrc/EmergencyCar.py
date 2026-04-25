import socket
import sys
import threading
import GUIBase

if (len(sys.argv)!=3):
    print("Incorrect number of arguments")
    exit()

Arguments = sys.argv[1:]

Localhost="127.0.0.1"
EmercenyCenterPort = 7777
EmercenyCarPort = 8999                
EmergencyCenterIP="10.0.5.0"
DataCenterPort=7777
DataCenterIP = "10.0.6.0"
Flag=0
MiddleboxEmergency=False




EmergencyCarIP = Arguments[0]

Title = Arguments[1]


def RespondToMiddleBox(MiddleboxSocket,IsAccident):
    if (IsAccident):
        MiddleboxSocket.send('Accident'.encode())
    else:
        MiddleboxSocket.send('NonAccident'.encode())


def HandleMiddlebox(MiddleboxSocket,BoxNumber):
  MiddleboxString = "Middlebox "+str(BoxNumber)
  global MiddleboxEmergency
  global Flag
  try:
    with MiddleboxSocket:
            #CameraSocket.send('Thank you for connecting'.encode()) 
            while True:
             #     print()
                  #Receive data indefinitely. 
                data=MiddleboxSocket.recv(1024).decode()
                print(data)
                EmergencyGUI(MiddleboxString,data)
                while (MiddleboxEmergency == False):
                    pass
                  
                      
                print("Responding")
                if (MiddleboxEmergency):
                    RespondToMiddleBox(MiddleboxSocket,Flag)
                    Flag=0
                    MiddleboxEmergency=False
                    print("Middlebox emergency")
                    break

                      

  except Exception as e:
     print(e)



#Create server thread
def EmergencyCarServer():
 global EmergencyCarIP
 global EmercenyCarPort
 boxnumber = 1
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind((EmergencyCarIP, EmercenyCarPort))         
            print ("socket binded to %s" %(EmercenyCarPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                #Establish connection with middlebox
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr[0]).split('.')


                  if (AddressString[-1]=="1"):
                      boxnumber=1
                  elif(AddressString[-1]=="2"):
                      boxnumber=2
                  if(AddressString[2]!="4"):
                      pass
                  else:
                    threading.Thread(target=HandleMiddlebox, args=(client,boxnumber,),daemon=True).start()
                    
 except Exception as e:
     print(e)
     
  # Breaking once connection closed

def EmergencyResponse(Caller):
    global Flag
    global MiddleboxEmergency
    MiddleboxEmergency=True
    Flag=1
    
    
def NonEmergencyResponse(Caller):
    global Flag
    global MiddleboxEmergency
    Flag=0
    MiddleboxEmergency=True


          
def EmergencyGUI(Caller,AccidentText):
     global Title
     GUI=GUIBase.EmergencyGUI(EmergencyResponse,NonEmergencyResponse,Title,Caller,AccidentText)
     threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()


EmergencyCarServer()