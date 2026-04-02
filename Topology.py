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


def CameraTopology():
    #Camera topology
        print("RAN")
        net=Mininet_wifi(link=wmediumd)
        info("Creating Nodes\n")
        
        Cameras1 = net.addStation('Cameras1', mac='00:00:00:00:00:01', position='1,0,0')
        Cameras2 = net.addStation('Cameras2', mac='00:00:00:00:00:02', position='1000,0,0')
        Cameras3 = net.addStation('Cameras3', mac='00:00:00:00:00:03', position='2000,0,0')
        Cameras4 = net.addStation('Cameras4', mac='00:00:00:00:00:04', position='3000,0,0')
        CameraAccessPoint1=net.addAccessPoint('Camera1AP', ssid='ssid-Camera1AP', channel='1', position='1,5,0')
        CameraAccessPoint2=net.addAccessPoint('Camera2AP', ssid='ssid-Camera2AP', channel='1', position='1000,5,0')
        CameraAccessPoint3=net.addAccessPoint('Camera3AP', ssid='ssid-Camera3AP', channel='1', position='2000,5,0')
        CameraAccessPoint4=net.addAccessPoint('Camera4AP', ssid='ssid-Camera4AP', channel='1', position='3000,5,0')

        c1=net.addController('c1')

        #net.setPropagationModel(model='logDistance', exp=3)

        net.configureNodes()
        

        
        net.addLink(CameraAccessPoint1,CameraAccessPoint2)
        net.addLink(CameraAccessPoint2,CameraAccessPoint3)
        net.addLink(CameraAccessPoint3,CameraAccessPoint4)
        net.addLink(CameraAccessPoint4,CameraAccessPoint1)

        net.plotGraph(max_x=3200,max_y=30)

        net.build()
        c1.start()
        CameraAccessPoint1.start([c1])
        CameraAccessPoint2.start([c1])
        CameraAccessPoint3.start([c1])
        CameraAccessPoint4.start([c1])
        info("*** Running CLI\n")
        CLI(net)

        info("*** Stopping network\n")
        net.stop()

setLogLevel('info')
CameraTopology()
