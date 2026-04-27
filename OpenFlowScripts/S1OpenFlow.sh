#!/bin/bash

#define IP addresses
Camera1IPRange=10.0.0.0/24
Camera2IPRange=10.0.1.0/24
MiddleboxIPRange=10.0.4.0/24
Middlebox1=10.0.4.1
Middlebox2=10.0.4.2
DataCenterIP=10.0.6.0
EmergencyCenterIP=10.0.5.0
EmergencyVehiclesIPRange=10.1.0.0/16
EmergencyVehicle1IP=10.1.0.1

#Camera IPs
Camera1=10.0.0.1
Camera2=10.0.0.2
Camera3=10.0.1.1
Camera4=10.0.1.2

#port towards middlebox
MiddleboxPort=1
#Network Slicing
HighBandWidthPort=4
LowBandWidthPort=5
HighBandWidth1=s1HIGH
LowBandWidth1=s1LOW
HighBandWidth2=s2HIGH
LowBandWidth2=s2LOW
#EmergencyAP
EmergencyAP1Port=6
EmergencyAP2Port=7

#Port numbers we care about.
ImageServerPort=7777
TextDataPort=80

#s1 definitions
#Rules for cameras
ovs-ofctl add-flow s1 priority=100,ip,nw_src=$Camera1,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=101,in_port=$MiddleboxPort,ip,nw_dst=$Camera1,actions=normal
ovs-ofctl add-flow s1 priority=103,ip,nw_src=$Camera2,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=102,in_port=$MiddleboxPort,ip,nw_dst=$Camera2,actions=normal
#ARP rules
#camera 1
ovs-ofctl add-flow s1 priority=1200,arp,nw_src=$Camera1,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=1201,in_port=$MiddleboxPort,arp,nw_dst=$Camera1,actions=normal
#camera 2
ovs-ofctl add-flow s1 priority=1202,arp,nw_src=$Camera2,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=1203,in_port=$MiddleboxPort,arp,nw_dst=$Camera2,actions=normal

#Port to middlebox from network slicing.
ovs-ofctl add-flow s1 priority=300,in_port=$HighBandWidthPort,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=400,in_port=$LowBandWidthPort,actions=output:$MiddleboxPort
#Traffic that should never be accepted (shouldn't happen).
ovs-ofctl add-flow s1 priority=601,ip,ip_dst=$Middlebox2,actions=drop
ovs-ofctl add-flow s1 priority=602,ip,ip_dst=$Middlebox2,actions=drop
ovs-ofctl add-flow s1 priority=603,ip,ip_src=$Middlebox1,in_port=$HighBandWidthPort,actions=drop
ovs-ofctl add-flow s1 priority=604,ip,ip_src=$Middlebox1,in_port=$LowBandWidthPort,actions=drop



#Setting up Network Slicing.
ovs-ofctl add-flow s1 priority=699,in_port=$MiddleboxPort,dl_type=0x800,nw_proto=6,tp_dst=$ImageServerPort,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=698,in_port=$MiddleboxPort,dl_type=0x800,nw_proto=6,tp_dst=$TextDataPort,actions=output:$LowBandWidthPort
ovs-ofctl add-flow s1 priority=700,in_port=$MiddleboxPort,dl_type=0x800,nw_proto=6,tp_dst=$ImageServerPort,ip,ip_dst=$EmergencyCenterIP,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=701,in_port=$MiddleboxPort,dl_type=0x800,nw_proto=6,tp_dst=$TextDataPort,ip,ip_dst=$EmergencyCenterIP,actions=output:$LowBandWidthPort

#Higher priority for emergency center
ovs-ofctl add-flow $HighBandWidth1 priority=200,ip,ip_dst=$EmergencyCenterIP,actions=normal
ovs-ofctl add-flow $HighBandWidth1 priority=100,actions=normal
ovs-ofctl add-flow $HighBandWidth1 priority=300,arp,actions=drop #prevent cycles
ovs-ofctl add-flow $LowBandWidth1 priority=200,ip,ip_dst=$EmergencyCenterIP,actions=normal
ovs-ofctl add-flow $LowBandWidth1 priority=100,actions=normal


#For testing purposes define rules for ICMP
ovs-ofctl add-flow s1 priority=50,icmp,ip_dst=$EmergencyCenterIP,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=49,ip,ip_dst=$EmergencyCenterIP,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=50,icmp,ip_dst=$DataCenterIP,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=49,ip,ip_dst=$DataCenterIP,actions=output:$HighBandWidthPort
#Emergency AP
ovs-ofctl add-flow s1 priority=120,in_port=$EmergencyAP1Port,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=110,in_port=$EmergencyAP2Port,actions=output:$MiddleboxPort
#Emergency vehicle
ovs-ofctl add-flow s1 priority=800,ip,nw_dst=$EmergencyVehicle1IP,actions=output:normal
ovs-ofctl add-flow s1 priority=800,arp,nw_dst=$EmergencyVehicle1IP,actions=output:normal
ovs-ofctl add-flow s1 priority=800,icmp,nw_dst=$EmergencyVehicle1IP,actions=output:normal

