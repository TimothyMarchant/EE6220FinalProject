#!/usr/bin/python

import socket
import time
import sys
import threading     
import subprocess
OpenflowScripts=""

Arguments =sys.argv[1:]
if (len(Arguments)!=1):
    print("You need to give a source folder for openflow scripts.")
    exit()

# first of all import the socket library 

# next create a socket object 
Localhost="127.0.0.1"
Middlebox1IP="10.0.4.1"
Middlebox2IP="10.0.4.2"
#portnumber 

MiddleboxPort = 9999

EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"

DataCenterPort=7777
DataCenterIP = "10.0.6.0"

#SDN controller definitions
SDNControllerIP=Localhost
SDNPort = 6767
##
EmergencyCarIPRange="10.1.0.0/16"
EmergencyCarsCount = 0
CarAvailable = False
EmergencyAvailable = False

EmergencyCaller=""

          
EmergencyText = ""
CMDLength = 4
EmergencyPort = 4
#CMD format
# CMDnumber, options
# Emergency, Switch, CameraAP, CameraIP
# NonEmergency, Switch, CameraAP, CameraIP
# The first command will increase the priority for that caller and that particular station
# The second command removes it.

#Emergency CMD string
EmergencyCMD = "Emergency"
NonEmergencyCMD = "Nonemergency"
def RunOpenFlowCMD(CMD):
    subprocess.run(CMD, shell=True, executable="/bin/bash")

#Create server thread
def HandleCaller(CallerSocket):
    try:
        with CallerSocket:
            data=CallerSocket.recv(1024).decode()
            Command = data.split(',')
            print(Command)
            if (len(Command)!=CMDLength):
                print("Invalid CMD")
                CallerSocket.send('Invalid Command length'.encode())
                return
            if (Command[0] == EmergencyCMD):
                Switch = Command[1] #Get switch name
                CameraAP = Command[2] #Get corresponding CameraAP
                CameraIP = Command[3] #Get the camera of interest.  This matters more for when there is multiple cameras
                AddflowSwitch = "ovs-ofctl add-flow " + Switch + " priority=300,ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(EmergencyPort)
                AddflowAP = "ovs-ofctl add-flow " + CameraAP + " priority=200,ip,ip_src="+CameraIP+",actions=output:normal"
                RunOpenFlowCMD(AddflowAP)
                RunOpenFlowCMD(AddflowSwitch)

                #Run command 
            elif (Command[0] == NonEmergencyCMD):
                Switch = Command[1] #Get switch name
                CameraAP = Command[2] #Get corresponding CameraAP
                CameraIP = Command[3] #Get the camera of interest.  This matters more for when there is multiple cameras
                DelflowSwitch = "ovs-ofctl del-flows " + Switch + " ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(EmergencyPort)
                DelflowAP = "ovs-ofctl del-flows " + CameraAP + " ip,ip_src="+CameraIP+",actions=output:normal"
                RunOpenFlowCMD(DelflowAP)
                RunOpenFlowCMD(DelflowSwitch)
                
            else:
                print("Invalid CMD")
                CallerSocket.send("InvalidCMD".encode())
                return
            CallerSocket.send("Finished adding flows".encode())
            print("Finished adding flows")

    except Exception as e:
        print(e)
def SDNServer():
 global Localhost
 global IP
 try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind(('localhost', SDNPort))         
            print ("socket binded to %s" %(SDNPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                  client, addr = ListeningSocket.accept()
                  print(addr)

                  threading.Thread(target=HandleCaller, args=(client,),daemon=True).start()
 except Exception as e:
     print(e)
SDNServer()
