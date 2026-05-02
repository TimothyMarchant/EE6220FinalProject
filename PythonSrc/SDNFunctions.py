#!/usr/bin/python
"""
The purpose of this file is to host all the automated SDN functions.  we are not using Ryu due to time constraints.  

"""

import subprocess


OpenflowScripts=""

Localhost="127.0.0.1"
Middlebox1IP="10.0.4.1"
Middlebox2IP="10.0.4.2"
#portnumber 
MiddleboxPort = 9999
#Image port number
EmercenyCenterPort = 7777                
EmergencyCenterIP="10.0.5.0"
#Image port number
DataCenterPort=7777
DataCenterIP = "10.0.6.0"

##Defining IP address range.
EmergencyCarIPRange="10.1.0.0/16"
EmergencyCarsCount = 0
CarAvailable = False
EmergencyAvailable = False

EmergencyCaller=""
EmergencyCallerNumber=0
          
EmergencyText = ""

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

#Run openflow CMD
def RunOpenFlowCMD(CMD):
    subprocess.run(CMD, shell=True, executable="/bin/bash")

###Middlebox calls this.  Centralized control means one point of failure, we don't want that.
###IP refers to middlebox IP.  
###MSGType refers to if the change is for an emergency vs nonemergency
###CameraNumber refers to the offending camera that needs modification for its flow.
def CallSDNController(IP,MSGType,CameraNumber):
    global SDNControllerIP
    global SDNPort
    global EmergencyPort
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
    #Try catch block in case commands fail for some reason.
    ###
    try:
        ###If emergency add flows such that the offending camera has higher priority than the other cameras associated with its AP.
        if (MSGType == EmergencyCMD):
                #Delete default path flow.
                DelflowSwitch = "ovs-ofctl del-flows " + Switch + " ip,ip_dst="+EmergencyCenterIP
                #Switch to the emergency lane path.  This dedicates bandwidth meant for only that camera essentially.
                AddflowSwitch = "ovs-ofctl add-flow " + Switch + " priority=300,ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(EmergencyPort)
                #Add flow to camera.
                AddflowAP = "ovs-ofctl add-flow " + CameraAP + " priority=200,ip,ip_src="+CameraIP+",actions=output:normal"
                #run openflow cmds.
                RunOpenFlowCMD(AddflowAP)
                RunOpenFlowCMD(DelflowSwitch)
                RunOpenFlowCMD(AddflowSwitch)

                #Run command 
        elif (MSGType == NonEmergencyCMD):
                #delte emergency lane path flow.
                DelflowSwitch = "ovs-ofctl del-flows " + Switch + " ip,ip_dst="+EmergencyCenterIP
                #delte higher priority camera flow.
                DelflowAP = "ovs-ofctl del-flows " + CameraAP + " ip,ip_src="+CameraIP
                #return to original path flow.
                AddflowSwitch = "ovs-ofctl add-flow " + Switch + " priority=300,ip,ip_dst="+EmergencyCenterIP+",actions=output:"+str(StandardPort)
                #Run openflow cmds.
                RunOpenFlowCMD(DelflowAP)
                RunOpenFlowCMD(DelflowSwitch)
                RunOpenFlowCMD(AddflowSwitch)
        
    except Exception as e:
        print(e)