#!/bin/bash

#define IP addresses
Camera1IPRange=10.0.0.0/24
Camera2IPRange=10.0.1.0/24
MiddleboxIPRange=10.0.4.0/24
Middlebox1=10.0.4.1
Middlebox2=10.0.4.2
DataCenterIP=10.0.6.0
EmergencyCenterIP=10.0.5.0
EmergencyVehiclesIPRange=12.0.0.0/16
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

#s1 definitions.
ovs-ofctl add-flow s1 priority=500,ip,nw_src=$Camera1IPRange,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,icmp,nw_src=$Camera1IPRange,actions=output:$MiddleboxPort

ovs-ofctl add-flow s1 priority=500,in_port=$MiddleboxPort,ip,nw_dst=$Camera1IPRange,actions=normal
ovs-ofctl add-flow s1 priority=500,in_port=$MiddleboxPort,icmp,nw_dst=$Camera1IPRange,actions=normal

ovs-ofctl add-flow s1 priority=500,ip,nw_src=$Camera1,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,in_port=$MiddleboxPort,ip,nw_dst=$Camera1,actions=normal
ovs-ofctl add-flow s1 priority=500,ip,nw_src=$Camera2,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,in_port=$MiddleboxPort,ip,nw_dst=$Camera2,actions=normal
ovs-ofctl add-flow s1 priority=500,in_port=$HighBandWidthPort,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,in_port=$LowBandWidthPort,actions=output:$MiddleboxPort
#Traffic that should never be accepted (shouldn't happen).
ovs-ofctl add-flow s1 priority=600,ip,ip_dst=$Middlebox2,actions=drop
ovs-ofctl add-flow s1 priority=600,ip,ip_dst=$Middlebox2,actions=drop
ovs-ofctl add-flow s1 priority=600,ip,ip_src=$Middlebox1,in_port=$HighBandWidthPort,actions=drop
ovs-ofctl add-flow s1 priority=600,ip,ip_src=$Middlebox1,in_port=$LowBandWidthPort,actions=drop



#Setting up Network Slicing.
ovs-ofctl add-flow s1 priority=600,dl_type=0x800,nw_proto=6,tp_dst=$ImageServerPort,actions=output:$HighBandWidthPort
ovs-ofctl add-flow s1 priority=600,dl_type=0x800,nw_proto=6,tp_dst=$TextDataPort,actions=output:$LowBandWidthPort

#Higher priority for emergency center
ovs-ofctl add-flow $HighBandWidth1 priority=200,ip,ip_dst=$EmergencyCenterIP,actions=normal
ovs-ofctl add-flow $HighBandWidth1 priority=100,actions=normal
ovs-ofctl add-flow $LowBandWidth1 priority=200,ip,ip_dst=$EmergencyCenterIP,actions=normal
ovs-ofctl add-flow $LowBandWidth1 priority=100,actions=normal
#For testing purposes define rules for ICMP
ovs-ofctl add-flow s1 priority=50,icmp,ip_dst=$EmergencyCenterIP,actions=output:$LowBandWidthPort
ovs-ofctl add-flow s1 priority=50,ip,ip_dst=$EmergencyCenterIP,actions=output:$LowBandWidthPort
ovs-ofctl add-flow s1 priority=50,icmp,ip_dst=$DataCenterIP,actions=output:$LowBandWidthPort
ovs-ofctl add-flow s1 priority=50,ip,ip_dst=$DataCenterIP,actions=output:$LowBandWidthPort
#Emergency AP
ovs-ofctl add-flow s1 priority=600,in_port=$EmergencyAP1Port,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=600,in_port=$EmergencyAP2Port,actions=output:$MiddleboxPort

