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
        Cameras1 = net.addStation('Cameras1', ip='10.0.0.1',mac='00:00:00:00:00:01', position='1,0,0')
        Cameras2 = net.addStation('Cameras2', ip='10.0.0.2', mac='00:00:00:00:00:02', position='1000,0,0')
        Cameras3 = net.addStation('Cameras3',ip='10.0.1.1', mac='00:00:00:00:00:03', position='0,1000,0')
        Cameras4 = net.addStation('Cameras4',ip='10.0.1.2', mac='00:00:00:00:00:04', position='1000,1000,0')
        ###Use channel 1.  They do not overlap.
        CameraAccessPoint1=net.addAccessPoint('Camera1AP', ssid='ssid-Camera1AP', channel='1', position='1,5,0')
        CameraAccessPoint2=net.addAccessPoint('Camera2AP', ssid='ssid-Camera2AP', channel='1', position='1010,5,0')
        CameraAccessPoint3=net.addAccessPoint('Camera3AP', ssid='ssid-Camera3AP', channel='1', position='10,1000,0')
        CameraAccessPoint4=net.addAccessPoint('Camera4AP', ssid='ssid-Camera4AP', channel='1', position='1010,1005,0')
        #call remote so SDN controller works.  This example uses a dumb L2 switch for establishing a baseline.
        #c1=net.addController('c1',controller=RemoteController,ip=ryu_ip,port=ryu_port)
        c1=net.addController('c1')
        ##Switches
        s1=net.addSwitch('s1')
        s2=net.addSwitch('s2')
        s3=net.addSwitch('s3')
        s4=net.addSwitch('s4')
        s5=net.addSwitch('s5')
        s6=net.addSwitch('s6')
        Mid1HighBandwidthSwitch=net.addSwitch('s1HIGH')
        Mid1LowBandwidthSwitch=net.addSwitch('s1LOW')
        Mid2HighBandwidthSwitch=net.addSwitch('s2HIGH')
        Mid2LowBandwidthSwitch=net.addSwitch('s2LOW')
        ###Use channel 2 overlaps with channel 1.
        EmergencyAP1=net.addAccessPoint('Emer1AP', ssid='ssid-Emergency1AP', channel='2', position='500,5,0')
        EmergencyAP2=net.addAccessPoint('Emer2AP', ssid='ssid-Emergency2AP', channel='2', position='1000,500,0')
        EmergencyAP3=net.addAccessPoint('Emer3AP', ssid='ssid-Emergency3AP', channel='2', position='0,500,0')
        EmergencyAP4=net.addAccessPoint('Emer4AP', ssid='ssid-Emergency4AP', channel='2', position='500,1000,0')
        #Add wire hosts
        EmergencyCenter=net.addHost('Emerctr',ip='10.0.5.0') #name is character limited
        Middlebox1=net.addHost('Mid1',ip='10.0.4.1')
        Middlebox2=net.addHost('Mid2',ip='10.0.4.2')
        Datacenter=net.addHost('data',ip='10.0.6.0')
        #net.setPropagationModel(model='logDistance', exp=3)

        net.configureNodes()


        
        #Connections from hosts to switches
        net.addLink(Middlebox1,s1,port1=1,port2=1,bw=50)
        net.addLink(Middlebox2,s2,port1=1,port2=1,bw=50)
        #Camera access point connections to switches s1 and s2
        net.addLink(CameraAccessPoint1,s1,port1=2,port2=2,bw=20) #Connect to S1.  Connects to box 1
        net.addLink(CameraAccessPoint2,s1,port1=2,port2=3,bw=20) #Connect to S1.  Connects to box 1
        net.addLink(CameraAccessPoint3,s2,port1=2,port2=2,bw=20) #Connect to S2.  Connects to box 2
        net.addLink(CameraAccessPoint4,s2,port1=2,port2=3,bw=20) #Connect to S2.  Connects to box 2

        #switch connections
        #Network slicing.  Send image data over larger bandwidth, send smaller data over the other link.
        #Middlebox 1
        net.addLink(s1,Mid1HighBandwidthSwitch,port1=4,port2=1,bw=50)
        net.addLink(s1,Mid1LowBandwidthSwitch,port1=5,port2=1,bw=2)
        #Middlebox 2
        net.addLink(s2,Mid2HighBandwidthSwitch,port1=4,port2=1,bw=50)
        net.addLink(s2,Mid2LowBandwidthSwitch,port1=5,port2=1,bw=2)
        #Connect to switch 3 which connects the entire network.
        #connect S1
        net.addLink(Mid1HighBandwidthSwitch,s3,port1=2,port2=1,bw=50)
        net.addLink(Mid1LowBandwidthSwitch,s3,port1=2,port2=2,bw=2)
        #Connect S2
        net.addLink(Mid2HighBandwidthSwitch,s3,port1=2,port2=3,bw=50)
        net.addLink(Mid2LowBandwidthSwitch,s3,port1=2,port2=4,bw=2)
        #make remaining switch connections
        #Connect S4
        net.addLink(s3,s4,port1=5,port2=1,bw=75)
        #Connect S5
        net.addLink(s3,s5,port1=6,port2=1,bw=75)

        #Storage and emergencenter connections
        net.addLink(Datacenter,s4,port2=2,bw=100) #Data storage platform.
        #emergency center connection
        net.addLink(EmergencyCenter,s5,port2=2,bw=100) #High bandwidth
        #Connect Emergency APs to their nearby middlebox
        net.addLink(EmergencyAP1,s1,port2=6,bw=2)
        net.addLink(EmergencyAP2,s1,port2=7,bw=2)
        net.addLink(EmergencyAP3,s2,port2=6,bw=2)
        net.addLink(EmergencyAP4,s2,port2=7,bw=2)



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
