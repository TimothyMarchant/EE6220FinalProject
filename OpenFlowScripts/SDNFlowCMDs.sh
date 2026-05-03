#!/bin/bash
###Variables
SourceFolder=OpenFlowScripts
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
###ports are defined for more accurate forwarding.
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


#Install normal flows first.
$SourceFolder/./NormalRouterOpenflowCMDs.sh

####Drop packets that should not arrive at certain locations.
ovs-ofctl add-flow s1 priority=300,ip,ip_src=$Middlebox2,actions=drop
ovs-ofctl add-flow s1 priority=300,ip,ip_dst=$Middlebox2,actions=drop
ovs-ofctl add-flow s2 priority=300,ip,ip_src=$Middlebox1,actions=drop
ovs-ofctl add-flow s2 priority=300,ip,ip_dst=$Middlebox1,actions=drop



