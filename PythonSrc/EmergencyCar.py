"""
By Timothy Marchant

This program creates a TCP client to connect to the middlebox.  It does this by trying to connect to them in the order of
Middlebox 1 and then middlebox 2.  It stays connected to the first one it can connect to.
It waits for data from the server before having a GUI pop up.
The user can accept or refuse the request depending on the scenario.  For this project it just acts as a proof of concept of how the network should work.
It makes more sense to handle this in the application layer not L3.  


Don't remember which site I specifically followed TCP examples from (I think stackoverflow?)
e.g. you don't want emergency data to get lost, corrupted or arrive out of order.

"""
#import libaries.
import socket
import sys
import threading
import GUIBase
import time


if (len(sys.argv)!=2):
    print("Incorrect number of arguments")
    exit()
##Take in the title of the GUI.  This was meant for mutiple cars.
Arguments = sys.argv[1:]

Localhost="127.0.0.1"
EmercenyCenterPort = 7777
EmercenyCarPort = 8999                
EmergencyCenterIP="10.0.5.0"
DataCenterPort=7777
DataCenterIP = "10.0.6.0"
ACCEPTFLAG=1
REFUSEFLAG=0
Flag=0
MiddleboxEmergency=False

Middlebox1IP = "10.0.4.1"
Middlebox2IP = "10.0.4.2"
MiddleboxPort = 9999
MiddleboxIPs = [Middlebox1IP, Middlebox2IP]


Title = Arguments[0]

#Create Client.  It connects to the middlebox and waits for a response at some point (if one is ever given)
def EmergencyCarClient():
    global EmercenyCarPort
    global MiddleboxPort
    global MiddleboxEmergency
    global Flag
    global ACCEPTFLAG
    global REFUSEFLAG
    response="defaultmsg" #Should never get send like this
    #Run forever until an emergency is accepted or refused.
    while True:
    #Try connecting to each middlebox.
        for i in MiddleboxIPs:
            try:
                #Create TCP client.
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as MiddleboxSocket:
                    MiddleboxSocket.connect((i,MiddleboxPort))      
                    while True:
            
                        #Get middlebox response.
                        MiddleboxQuestion = MiddleboxSocket.recv(1024).decode()
                        print("RAN")
                        Caller=MiddleboxQuestion.split(':')[-1]
                        #open GUI
                        EmergencyGUI(Caller,MiddleboxQuestion)
                        #Wait for a response in the GUI.  I know this should not be blocking.
                        while (MiddleboxEmergency==False):
                            time.sleep(0.01)
                            pass
                        #Change response based on flag
                        if (Flag == ACCEPTFLAG):
                            response = "Accept"
                        elif (Flag == REFUSEFLAG):
                            response = "Refuse"
                        else:
                            response = "This shouldn't happen"
                        #Send response
                        MiddleboxSocket.send(response.encode())
                        MiddleboxEmergency=False
                        return


                    
            except Exception as e:
                print(e)
     
##GUI button functions.
##Reused from other code, but essentially meant to change certain flags in the main server program. (that's why caller is unused)
#Change flags for emergency.
def EmergencyResponse(Caller):
    global Flag
    global MiddleboxEmergency
    global ACCEPTFLAG
    global REFUSEFLAG
    MiddleboxEmergency=True
    Flag=ACCEPTFLAG
    
#change flags for nonemergency.
def NonEmergencyResponse(Caller):
    global Flag
    global MiddleboxEmergency
    global ACCEPTFLAG
    global REFUSEFLAG
    MiddleboxEmergency=True
    Flag=REFUSEFLAG



          
def EmergencyGUI(Caller,AccidentText):
     global Title
     GUI=GUIBase.EmergencyGUI(EmergencyResponse,NonEmergencyResponse,Title,Caller,AccidentText)
     #Start thread for response.
     threading.Thread(target=GUI.RunGUI,args=(),daemon=True).start()

#Run client.
EmergencyCarClient()

exit()