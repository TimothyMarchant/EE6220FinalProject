#!/bin/bash
#s1,s2,s3,s4,s5
#define IP addresses
Camera1IPRange=10.0.0.0/24
Camera2IPRange=10.0.1.0/24
MiddleboxIPRange=10.0.4.0/24
EmergencyCenterIP=200.0.0.0
EmergencyVehiclesIPRange=12.0.0.0/16
#port towards middlebox
MiddleboxPort=1


ovs-ofctl add-flow s1 priority=500,ip,nw_src=$Camera1IPRange,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,icmp,nw_src=$Camera1IPRange,actions=output:$MiddleboxPort

ovs-ofctl add-flow s1 priority=500,in_port=1,ip,nw_dst=$Camera1IPRange,actions=normal
ovs-ofctl add-flow s1 priority=500,in_port=1,icmp,nw_dst=$Camera1IPRange,actions=normal

ovs-ofctl add-flow s1 priority=500,ip,nw_src=10.0.0.1,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,in_port=1,ip,nw_dst=10.0.0.1,actions=normal
ovs-ofctl add-flow s1 priority=500,ip,nw_src=10.0.0.2,actions=output:$MiddleboxPort
ovs-ofctl add-flow s1 priority=500,in_port=1,ip,nw_dst=10.0.0.2,actions=normal
ovs-ofctl add-flow s2 priority=500,in_port=1,actions=normal
ovs-ofctl add-flow s1 priority=500,in_port=4,actions=output:1
ovs-ofctl add-flow s1 priority=500,in_port=5,actions=output:1
ovs-ofctl add-flow s1 priority=600,ip,ip_src=10.0.4.2,actions=drop


#s2 defintions
ovs-ofctl add-flow s2 priority=500,ip,nw_src=$Camera2IPRange,actions=output:$MiddleboxPort
ovs-ofctl add-flow s2 priority=500,icmp,nw_src=$Camera2IPRange,actions=output:$MiddleboxPort

ovs-ofctl add-flow s2 priority=500,in_port=1,ip,nw_dst=$Camera2IPRange,actions=normal
ovs-ofctl add-flow s2 priority=500,in_port=1,icmp,nw_dst=$Camera2IPRange,actions=normal

ovs-ofctl add-flow s2 priority=500,ip,nw_src=10.0.1.1,actions=output:$MiddleboxPort
ovs-ofctl add-flow s2 priority=500,in_port=1,ip,nw_dst=10.0.1.1,actions=normal
ovs-ofctl add-flow s2 priority=500,ip,nw_src=10.0.1.2,actions=output:$MiddleboxPort
ovs-ofctl add-flow s2 priority=500,in_port=1,ip,nw_dst=10.0.1.2,actions=normal
ovs-ofctl add-flow s2 priority=500,in_port=1,actions=normal
ovs-ofctl add-flow s2 priority=500,in_port=4,actions=output:1
ovs-ofctl add-flow s2 priority=500,in_port=5,actions=output:1
ovs-ofctl add-flow s2 priority=600,ip,ip_src=10.0.4.1,actions=drop



ovs-ofctl add-flow s3 priority=500,in_port=4,ip,nw_src=10.0.4.0/24,actions=drop
ovs-ofctl add-flow s3 priority=500,in_port=4,ip,nw_src=10.0.4.1,actions=drop
ovs-ofctl add-flow s3 priority=500,in_port=4,ip,nw_src=10.0.4.2,actions=drop

ovs-ofctl add-flow s3 priority=300,in_port=1,actions=normal
ovs-ofctl add-flow s3 priority=300,in_port=2,actions=normal
ovs-ofctl add-flow s3 priority=300,in_port=3,actions=normal

ovs-ofctl add-flow s4 actions=normal

ovs-ofctl add-flow s5 priority=200,actions=normal
ovs-ofctl add-flow s5 priority=199,ip,nw_src=10.0.4.1,nw_dst=10.0.6.1,actions=drop
ovs-ofctl add-flow s5 priority=199,ip,in_port=3,nw_src=10.0.4.1,actions=drop
#ovs-ofctl add-flow s5 actions=normal


ovs-ofctl add-flow Camera1AP actions=normal
ovs-ofctl add-flow Camera2AP actions=normal
ovs-ofctl add-flow Camera3AP actions=normal
ovs-ofctl add-flow Camera4AP actions=normal
