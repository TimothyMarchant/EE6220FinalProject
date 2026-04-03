#!/usr/bin/python
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
net=Mininet_wifi()

ryu_ip = '127.0.0.1'
ryu_port = 6653

def CameraTopology():
        global net
    #Camera topology
        print("RAN")
        info("Creating Nodes\n")
        
        Cameras1 = net.addStation('Cameras1', mac='00:00:00:00:00:01', position='1,0,0')
        Cameras2 = net.addStation('Cameras2', mac='00:00:00:00:00:02', position='1000,0,0')
        Cameras3 = net.addStation('Cameras3', mac='00:00:00:00:00:03', position='2000,0,0')
        Cameras4 = net.addStation('Cameras4', mac='00:00:00:00:00:04', position='3000,0,0')
        CameraAccessPoint1=net.addAccessPoint('Camera1AP', ssid='ssid-Camera1AP', channel='1', position='1,5,0')
        CameraAccessPoint2=net.addAccessPoint('Camera2AP', ssid='ssid-Camera2AP', channel='1', position='1000,5,0')
        CameraAccessPoint3=net.addAccessPoint('Camera3AP', ssid='ssid-Camera3AP', channel='1', position='2000,5,0')
        CameraAccessPoint4=net.addAccessPoint('Camera4AP', ssid='ssid-Camera4AP', channel='1', position='3000,5,0')

        c1=net.addController('c1',controller=RemoteController,ip=ryu_ip,port=ryu_port)
        s1=net.addSwitch('s1')

        #Middlebox1=net.addStation('Middlebox1',mac='00:00:00:00:1B:01',position='500,500,0')
        #Middlebox2=net.addStation('Middlebox2',mac='00:00:00:00:1B:02',position='2500,500,0')

        EmergencyAP1=net.addAccessPoint('Emergency1AP', ssid='ssid-Emergency1AP', channel='2', position='500,5,0')
        EmergencyAP2=net.addAccessPoint('Emergency2AP', ssid='ssid-Emergency2AP', channel='2', position='1500,5,0')
        EmergencyAP3=net.addAccessPoint('Emergency3AP', ssid='ssid-Emergency3AP', channel='2', position='2500,5,0')
        EmergencyAP4=net.addAccessPoint('Emergency4AP', ssid='ssid-Emergency4AP', channel='2', position='3200,5,0')

        EmergencyCenter=net.addHost('Emerctr') #name is character limited
        Middlebox1=net.addHost('Mid1')
        Middlebox2=net.addHost('Mid2')

        #net.setPropagationModel(model='logDistance', exp=3)

        net.configureNodes()
        
        net.addLink(Cameras1,CameraAccessPoint1)
        net.addLink(Cameras2,CameraAccessPoint2)
        net.addLink(Cameras3,CameraAccessPoint3)
        net.addLink(Cameras4,CameraAccessPoint4)

        

        
        

        net.addLink(Middlebox1,s1)
        net.addLink(Middlebox2,s1)
        net.addLink(CameraAccessPoint1,s1)
        net.addLink(CameraAccessPoint2,s1)
        net.addLink(CameraAccessPoint3,s1)
        net.addLink(CameraAccessPoint4,s1)
        net.addLink(EmergencyCenter,s1)

      #  net.addLink(EmergencyCenter,Middlebox1)
      #  net.addLink(EmergencyCenter,Middlebox2)


        net.plotGraph(max_x=3250,max_y=2050)

        net.build()
        c1.start()
      #  c2.start()
        CameraAccessPoint1.start([c1])
        CameraAccessPoint2.start([c1])
        CameraAccessPoint3.start([c1])
        CameraAccessPoint4.start([c1])
        EmergencyAP1.start([c1])
        EmergencyAP2.start([c1])
        EmergencyAP3.start([c1])
        EmergencyAP4.start([c1])
      #  Middlebox1.start([c1])
      #  Middlebox2.start([c1])
      #  EmergencyCenter.start([c1])

def Middleboxes():
        print("run")
def EmergencyCenter():
        print("run")
def SetupSDN():
        print("")

setLogLevel('info')

CameraTopology()
info("*** Running CLI\n")
net.start()
CLI(net)

info("*** Stopping network\n")
net.stop()