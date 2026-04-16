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

#S3 middle switch
#higher priority for emergency center
ovs-ofctl add-flow s3 priority=200,ip,ip_dst=$EmergencyCenterIP,actions=output:6
ovs-ofctl add-flow s3 priority=100,ip,ip_dst=$DataCenterIP,actions=output:5
ovs-ofctl add-flow s3 priority=120,ip,ip_dst=$Middlebox1,actions=output:2
ovs-ofctl add-flow s3 priority=120,ip,ip_dst=$Middlebox2,actions=output:4
#ICMP
ovs-ofctl add-flow s3 priority=200,icmp,ip_dst=$EmergencyCenterIP,actions=output:6
ovs-ofctl add-flow s3 priority=100,icmp,ip_dst=$DataCenterIP,actions=output:5
ovs-ofctl add-flow s3 priority=120,icmp,ip_dst=$Middlebox1,actions=output:2
ovs-ofctl add-flow s3 priority=120,icmp,ip_dst=$Middlebox2,actions=output:4
#ARP
ovs-ofctl add-flow s3 priority=800,arp,ip_dst=$EmergencyCenterIP,actions=output:6
ovs-ofctl add-flow s3 priority=800,arp,ip_dst=$DataCenterIP,actions=output:5
ovs-ofctl add-flow s3 priority=800,arp,ip_dst=$Middlebox2,actions=output:4
ovs-ofctl add-flow s3 priority=800,arp,ip_dst=$Middlebox1,actions=output:2
#ovs-ofctl add-flow s3 priority=100,actions=normal
#ovs-ofctl add-flow s3 priority=1000,ip,ip_src=127.0.0.1,actions=normal
#ovs-ofctl add-flow s3 priority=80,actions=drop
