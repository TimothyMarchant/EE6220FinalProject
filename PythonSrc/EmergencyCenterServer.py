"""
By Timothy Marchant

This program creates a TCP server that can accept the middleboxs.  Takes in a single packet (Pretend it's the image data of a crash)
The program opens a GUI on startup.  You pick which cam corresponds to an emergency.  
Unfortunately, it's not exactly well thought out so pressing CAM 2 also affects CAM 1 and likewise with CAM 3 and CAM 4
It serves its purpose of being a proof of concept.

Don't remember which site I specifically followed TCP examples from (I think stackoverflow?)
e.g. you don't want emergency data to get lost, corrupted or arrive out of order.

"""
#import libaries.
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
MayMarkEmergency1=False
MayMarkEmergency2=False
Middlebox1Emergency=False
Middlebox2Emergency=False



Midbox1Message='null'
Midbox2Message='null'
#Send data  to the middlebox letting it know the status of that particular event.
def RespondToMiddleBox(MiddleboxSocket,IsAccident):

    global Flag1
    global Flag2
    if (IsAccident):
        MiddleboxSocket.send('Accident'.encode())
    else:
        MiddleboxSocket.send('NonAccident'.encode())

#Handle middlebox socket as a new thread.
def HandleMiddlebox(MiddleboxSocket,BoxNumber):
    global Middlebox1Emergency
    global Middlebox2Emergency
    global Flag1
    global Flag2
    global MayMarkEmergency1
    global MayMarkEmergency2
    if (BoxNumber==1):
        MayMarkEmergency1=True
    else:
        MayMarkEmergency2=True
    try:
        with MiddleboxSocket:
            while True:
                  #Receive data indefinitely. 
                data=MiddleboxSocket.recv(1024).decode()
                print(data)
                if (BoxNumber==1):
                    while (Middlebox1Emergency == False):
                        pass
                elif (BoxNumber==2):
                    while (Middlebox2Emergency == False):
                        pass
                      
                print("Responding")
                #Respond to the middlebox depending on the response from the emergency center.
                if (BoxNumber==1 and Middlebox1Emergency):
                    RespondToMiddleBox(MiddleboxSocket,Flag1)
                    Flag1=0
                    Middlebox1Emergency=False
                    MayMarkEmergency1=False
                    print("Middlebox 1 emergency")
                    break
                elif (BoxNumber==2 and Middlebox2Emergency):
                    RespondToMiddleBox(MiddleboxSocket,Flag2)
                    Flag2=0
                    Middlebox2Emergency=False
                    MayMarkEmergency2=False
                    print("Middlebox 2 emergency")
                    break

                      

    except Exception as e:
        print(e)
#Create server
def EmergencyCenterServer():
    global EmergencyCenterIP
    global EmercenyCenterPort
    boxnumber=1
    try:
      #Create TCP server.
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ListeningSocket:
            ListeningSocket.bind((EmergencyCenterIP, EmercenyCenterPort))         
            print ("socket binded to %s" %(EmercenyCenterPort)) 
            ListeningSocket.listen()     
            print ("socket is listening")  

            while True: 
                    #Establish connection with middlebox
                    client, addr = ListeningSocket.accept()
                    print(addr)
                    AddressString=str(addr[0]).split('.')
                    #Change boxnumber based on IP.  IPs correspond to differnet middleboxes.
                    if (AddressString[-1]=="1"):
                        boxnumber=1
                    
                    elif(AddressString[-1]=="2"):
                        boxnumber=2
                    #ignore other clients that are not the middlebox.
                    if(AddressString[2]!="4"):
                        pass
                    else:
                        threading.Thread(target=HandleMiddlebox, args=(client,boxnumber,),daemon=True).start()
                    
    except Exception as e:
        print(e)
     
###Called from the GUI.  Responses accordingly to the caller.
###mark the correct middlebox and flag to mark the response as an emergency.
def EmergencyResponse(Caller):
    global Flag1
    global Flag2
    global Middlebox1Emergency
    global Middlebox2Emergency
    global MayMarkEmergency1
    global MayMarkEmergency2
    EmergencyString1='Emergency 1'
    EmergencyString2='Emergency 2'
    EmergencyString3='Emergency 3'
    EmergencyString4='Emergency 4'
    if ((Caller==EmergencyString1 or Caller==EmergencyString2) and MayMarkEmergency1):
        Middlebox1Emergency=True
        Flag1=1
    if ((Caller==EmergencyString3 or Caller==EmergencyString4) and MayMarkEmergency2):
        Middlebox2Emergency=True
        Flag2=1
    
###mark the correct middlebox and flag to mark the response as an nonemergency.
def NonEmergencyResponse(Caller):
    global Flag1
    global Flag2
    global Middlebox1Emergency
    global Middlebox2Emergency
    global MayMarkEmergency1
    global MayMarkEmergency2
    EmergencyString1='Emergency 1'
    EmergencyString2='Emergency 2'
    EmergencyString3='Emergency 3'
    EmergencyString4='Emergency 4'
    if ((Caller==EmergencyString1 or Caller==EmergencyString2) and MayMarkEmergency1):
        Middlebox1Emergency=True
        Flag1=0
    if ((Caller==EmergencyString3 or Caller==EmergencyString4) and MayMarkEmergency2):
        Middlebox2Emergency=True
        Flag2=0

#call emergency GUI    
def EmergencyGUI():
    GUI=GUIBase.EmergencyCenterGUI(EmergencyResponse,NonEmergencyResponse)
    threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()
#start programs.
EmergencyGUI()
EmergencyCenterServer()
