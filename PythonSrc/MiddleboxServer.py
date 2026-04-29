import socket
import GUIBase
import time
import sys
import threading         
import subprocess


Arguments = sys.argv[1:]

if (len(Arguments)!=4):
   print("Incorrect number of arguments")
   exit()

# first of all import the socket library 

# next create a socket object 
Localhost="127.0.0.1"
Middlebox1IP="10.0.4.1"
Middlebox2IP="10.0.4.2"
IP=Arguments[-1]
#portnumber 

MiddleboxPort = 9999

EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"

DataCenterPort=7777
DataCenterIP = "10.0.6.0"

##
EmergencyCarIPRange="10.1.0.0/16"
EmergencyCarsCount = 0
CarAvailable = False
EmergencyAvailable = False

EmergencyCaller=""
EmergencyCallerNumber=0
          
EmergencyText = ""

#SDN controller definitions
SDNControllerIP=Localhost
SDNPort = 6767
#SDN CMDs
CMDLength = 4
EmergencyPort = 5
StandardPort = 4
#CMD format
# CMDnumber, options
# Emergency, Switch, CameraAP, CameraIP
# NonEmergency, Switch, CameraAP, CameraIP
# The first command will increase the priority for that caller and that particular station
# The second command removes it.

#Emergency CMD string
EmergencyCMD = "Emergency"
NonEmergencyCMD = "Nonemergency"

def CameraConnection(CameraSocket):
  try:
    with CameraSocket:
            #CameraSocket.send('Thank you for connecting'.encode()) 
            while True:
             #     print()
                  #Receive data indefinitely. 
                  data=CameraSocket.recv(1024).decode()
                  CameraSocket.send(data.encode())

  except Exception as e:
     print(e)

def HandleEmergencyCar(CarSocket):
    global EmergencyAvailable
    global EmergencyCaller
    global EmergencyCarsCount
    global EmergencyCallerNumber
    global CarAvailable
    CarAvailable = True
    try:
        with CarSocket:
            print("Carsocket")
            while True:
                if (EmergencyAvailable==True):
                    print("Emergency")
                    temp="Accident detected at:"+EmergencyCaller
                    CarSocket.send(temp.encode())
                    response = CarSocket.recv(1024).decode()
                    print(response)
                    if (response == "Refuse"):
                        CarAvailable = False
                        while (CarAvailable == False):
                           pass
                    #Accept
                    else:
                        EmergencyAvailable = False
                        CallSDNController(NonEmergencyCMD,EmergencyCallerNumber)
                    break

    except Exception as e:
        
        print(e)

    print("Ran Finally block")
    EmergencyCarsCount-=1
    #should never happen
    if (EmergencyCarsCount<0):
        EmergencyCarsCount = 0

#Create server thread
def MiddleboxServer():
 global EmergencyCarsCount
 global IP
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind((IP, MiddleboxPort))         
            print ("socket binded to %s" %(MiddleboxPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                  client, addr = ListeningSocket.accept()
                  print(addr)
                  AddressString=str(addr).split('.')
                  print(AddressString)
                  if (AddressString[1]!='0'):
                      print("IP:"+str(addr))
                      threading.Thread(target=HandleEmergencyCar, args=(client,), daemon=True).start()
                      EmergencyCarsCount += 1
                  else:
                    threading.Thread(target=CameraConnection, args=(client,),daemon=True).start()
 except Exception as e:
     print(e)

  # Breaking once connection closed
def CallEmergencyCenter(Caller):
    global EmergencyCallerNumber
    global EmergencyAvailable
    EmergenyCenterPort = 7777                
    EmergencyCenterIP="10.0.5.0"
     #EmergencyCenterIP=Localhost
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as EmergencySocket:
          EmergencySocket.connect((EmergencyCenterIP,EmergenyCenterPort))      
          while True:
            
            EmergencyString='Accident detected at '+(Caller)
            EmergencySocket.send(EmergencyString.encode())
            Response=EmergencySocket.recv(1024).decode()
            #print(Response)
            if (Response == 'Accident'):
                print("Accident Confirmed")
                break
            elif (Response == 'NonAccident'):
                print("Nonaccident confirmed")
                break
            else:
                print("Message not received correctly")
                break



    except Exception as e:
        print(e)
    CallSDNController(NonEmergencyCMD,EmergencyCallerNumber)

def RunOpenFlowCMD(CMD):
    subprocess.run(CMD, shell=True, executable="/bin/bash")

def CallSDNController(MSGType,CameraNumber):
    global IP
    global SDNControllerIP
    global SDNPort
    global EmergencyPort
    SDNMsg=""
    Switch=""
    CameraAP="Camera"
    CameraIP=""
    if (IP==Middlebox1IP):
        Switch="s1"
        CameraAP=CameraAP+str(CameraNumber)+"AP"
        CameraIP="10.0.0."+str(CameraNumber)
    elif(IP==Middlebox2IP):
        Switch="s2"
        CameraAP=CameraAP+str(CameraNumber+2)+"AP"
        CameraIP="10.0.1."+str(CameraNumber+2)
    try:
        if (MSGType == EmergencyCMD):
                DelflowSwitch = "ovs-ofctl del-flows " + Switch + " ip,ip_dst="+EmergencyCenterIP
                AddflowSwitch = "ovs-ofctl add-flow " + Switch + " priority=300,ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(EmergencyPort)
                AddflowAP = "ovs-ofctl add-flow " + CameraAP + " priority=200,ip,ip_src="+CameraIP+",actions=output:normal"
                RunOpenFlowCMD(AddflowAP)
                RunOpenFlowCMD(DelflowSwitch)
                RunOpenFlowCMD(AddflowSwitch)

                #Run command 
        elif (MSGType == NonEmergencyCMD):
                DelflowSwitch = "ovs-ofctl del-flows " + Switch + " ip,ip_dst="+EmergencyCenterIP
                DelflowAP = "ovs-ofctl del-flows " + CameraAP + " ip,ip_src="+CameraIP
                AddflowSwitch = "ovs-ofctl add-flow " + Switch + " priority=300,ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(StandardPort)

                RunOpenFlowCMD(DelflowAP)
                RunOpenFlowCMD(DelflowSwitch)
                RunOpenFlowCMD(AddflowSwitch)
        
    except Exception as e:
        print(e)
     
    


def EmergencyLogic(Caller,Number):
  global EmergencyCaller
  global EmergencyAvailable
  global EmergencyCallerNumber
  EmergencyCaller = Caller
  EmergencyCallerNumber = Number
  CallSDNController(EmergencyCMD,Number)
  EmergencyAvailable = True



def Main():
    global EmergencyCarsCount
    global EmergencyAvailable
    global EmergencyCaller
    global CarAvailable
    while True:
        if (EmergencyAvailable and (EmergencyCarsCount <=0 or CarAvailable == False)):
            CallEmergencyCenter(EmergencyCaller)
            EmergencyAvailable=False
            if (EmergencyCarsCount>0):
                CarAvailable = True
        time.sleep(0.01)
            

          
def MiddleboxGUI():
     global Arguments
     Title=Arguments[0]
     Camera1=Arguments[1]
     Camera2=Arguments[2]
     GUI=GUIBase.Middlebox_GUI(Title,Camera1,Camera2,EmergencyLogic,EmergencyLogic)

     threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()
def SendDataToDataCenter():
    global DataCenterIP
    global DataCenterPort

    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as DataCenterSocket:
        DataCenterSocket.connect((DataCenterIP,DataCenterPort))
        while True:
            DataCenterSocket.send('Send this string a bunch'.encode())
            time.sleep(0.01)

    except:
      exit()
threading.Thread(target=SendDataToDataCenter,args=(),daemon=True).start()
MiddleboxGUI()
threading.Thread(target=MiddleboxServer,args=(),daemon=True).start()
Main()
