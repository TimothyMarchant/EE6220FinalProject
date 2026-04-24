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



###Nothing special for this one.  Simply act like a normal router.
ovs-ofctl add-flow Camera1AP actions=normal
ovs-ofctl add-flow Camera2AP actions=normal
ovs-ofctl add-flow Camera3AP actions=normal
ovs-ofctl add-flow Camera4AP actions=normal

ovs-ofctl add-flow Emer1AP actions=normal
ovs-ofctl add-flow Emer2AP actions=normal
ovs-ofctl add-flow Emer3AP actions=normal
ovs-ofctl add-flow Emer4AP actions=normal

