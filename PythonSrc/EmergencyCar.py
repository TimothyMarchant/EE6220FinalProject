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

Middlebox1IP = "10.0.4.1"
Middlebox2IP = "10.0.4.2"
MiddleboxPort = 9999
MiddleboxIPs = [Middlebox1IP, Middlebox2IP]

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
def EmergencyCarClient():
 global EmergencyCarIP
 global EmercenyCarPort
 global MiddleboxPort
 boxnumber = 1
 response="defaultmsg" #Should never get send like this

 while True:
    try:
        for i in MiddleboxIPs:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as MiddleboxSocket:
                MiddleboxSocket.connect((i,MiddleboxPort))      
                while True:
            
            
                    MiddleboxQuestion = MiddleboxSocket.recv(1024).decode()
                    print("RAN")
                    Caller=MiddleboxQuestion.split(':')[-1]
                    EmergencyGUI(Caller,MiddleboxQuestion)
                    while (MiddleboxEmergency==False):
                        pass
                    if (Flag == 1):
                        response="Accept"
                    else:
                        response="Refuse"
                    #Send response
                    MiddleboxSocket.send(response.encode())


                    
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


EmergencyCarClient()