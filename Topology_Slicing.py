#!/usr/bin/python
#need to change a few things.
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, mesh
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from json import dumps
from requests import put
from mininet.util import quietRun
from os import listdir, environ
import re
import sys
net=Mininet_wifi(link = TCLink)

ryu_ip = '127.0.0.1'
ryu_port = 6653

def CameraTopology():
        global net
         #High bandwidth#Camera topology
        info("Creating Nodes\n")
        #define cameras
        Cameras1 = net.addStation('Cameras1', mac='00:00:00:00:00:01', position='1,0,0')
        Cameras2 = net.addStation('Cameras2', mac='00:00:00:00:00:02', position='1000,0,0')
        Cameras3 = net.addStation('Cameras3', mac='00:00:00:00:00:03', position='0,1000,0')
        Cameras4 = net.addStation('Cameras4', mac='00:00:00:00:00:04', position='1000,1000,0')
        ###Use channel 1.  They do not overlap.
        CameraAccessPoint1=net.addAccessPoint('Camera1AP', ssid='ssid-Camera1AP', channel='1', position='1,5,0')
        CameraAccessPoint2=net.addAccessPoint('Camera2AP', ssid='ssid-Camera2AP', channel='1', position='1010,5,0')
        CameraAccessPoint3=net.addAccessPoint('Camera3AP', ssid='ssid-Camera3AP', channel='1', position='10,5,0')
        CameraAccessPoint4=net.addAccessPoint('Camera4AP', ssid='ssid-Camera4AP', channel='1', position='1010,1005,0')
        #call remote so SDN controller works.  This example uses a dumb L2 switch for establishing a baseline.
        c1=net.addController('c1',controller=RemoteController,ip=ryu_ip,port=ryu_port)

        s1=net.addSwitch('s1')
        s2=net.addSwitch('s2')
        s3=net.addSwitch('s3')
        s4=net.addSwitch('s4')
        s5=net.addSwitch('s5')
        s6=net.addSwitch('s6')

        ###Use channel 2 overlaps with channel 1.
        EmergencyAP1=net.addAccessPoint('Emergency1AP', ssid='ssid-Emergency1AP', channel='2', position='500,5,0')
        EmergencyAP2=net.addAccessPoint('Emergency2AP', ssid='ssid-Emergency2AP', channel='2', position='1000,500,0')
        EmergencyAP3=net.addAccessPoint('Emergency3AP', ssid='ssid-Emergency3AP', channel='2', position='0,500,0')
        EmergencyAP4=net.addAccessPoint('Emergency4AP', ssid='ssid-Emergency4AP', channel='2', position='500,1000,0')
        #Add wire hosts
        EmergencyCenter=net.addHost('Emerctr') #name is character limited
        Middlebox1=net.addHost('Mid1')
        Middlebox2=net.addHost('Mid2')
        Datacenter=net.addHost('data')
        #net.setPropagationModel(model='logDistance', exp=3)

        net.configureNodes()
        #temp.  Should be removed later.

        
        #Connections from hosts to switches
        net.addLink(Middlebox1,s1,port1=1,port2=1,bw=50)
        net.addLink(Middlebox2,s2,port1=1,port2=1,bw=50)

        net.addLink(CameraAccessPoint1,s1,bw=20) #Connect to S1.  Connects to box 1
        net.addLink(CameraAccessPoint2,s1,bw=20) #Connect to S1.  Connects to box 1
        net.addLink(CameraAccessPoint3,s2,bw=20) #Connect to S2.  Connects to box 2
        net.addLink(CameraAccessPoint4,s2,bw=20) #Connect to S2.  Connects to box 2

        net.addLink(EmergencyCenter,s5,port2=4,bw=100) #High bandwidth
        net.addLink(s1,s5,port2=1,bw=50)
        net.addLink(s2,s5,port2=2,bw=50)
        net.addLink(s1,s3,port2=1,bw=100) #cannot make switch from Box 1 to S3 without causing problems.
        net.addLink(s2,s3,port2=2,bw=100) #cannot make switch from Box 2 to S3 without causing problems.
        net.addLink(s3,s4,port2=1,bw=100)
        net.addLink(s3,s5,port2=3,bw=100)

        net.addLink(Datacenter,s4,port2=2,bw=100) #Data storage platform.

        net.addLink(Cameras1,CameraAccessPoint1,bw=10)
        net.addLink(Cameras2,CameraAccessPoint2,bw=10)
        net.addLink(Cameras3,CameraAccessPoint3,bw=10)
        net.addLink(Cameras4,CameraAccessPoint4,bw=10)


        net.plotGraph(max_x=1050,max_y=1050)

        net.build()
        c1.start()

        CameraAccessPoint1.start([c1])
        CameraAccessPoint2.start([c1])
        CameraAccessPoint3.start([c1])
        CameraAccessPoint4.start([c1])
        EmergencyAP1.start([c1])
        EmergencyAP2.start([c1])
        EmergencyAP3.start([c1])
        EmergencyAP4.start([c1])




setLogLevel('info')

CameraTopology()
info("*** Running CLI\n")
net.start()
CLI(net)

info("*** Stopping network\n")
net.stop()