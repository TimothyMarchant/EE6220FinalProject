#!/bin/bash

#define IP addresses
Camera1IPRange=10.0.0.0/24
Camera2IPRange=10.0.1.0/24
MiddleboxIPRange=10.0.4.0/24
Middlebox1=10.0.4.1
Middlebox2=10.0.4.2
DatacenterIP=10.0.6.0
EmergencyCenterIP=10.0.5.0
EmergencyVehiclesIPRange=12.0.0.0/16
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

#Add flows for s5 not many
#Image data has higher priority than text data.
ovs-ofctl add-flow s5 priority=200,dl_type=0x800,nw_proto=6,tp_dst=7777,actions=normal
ovs-ofctl add-flow s5 priority=150,dl_type=0x800,nw_proto=6,tp_dst=80,actions=normal
ovs-ofctl add-flow s5 priority=100,actions=normal



#ovs-ofctl add-flow s5 priority=199,ip,nw_src=10.0.4.1,nw_dst=10.0.6.1,actions=drop
#ovs-ofctl add-flow s5 priority=199,ip,in_port=3,nw_src=10.0.4.1,actions=drop
