#!/bin/bash

###The purpose of this file is to add flows that treat all APs and switches as normal routers.
### this is to make a base line for No SDN.  It is also used for the SDN version as well.
###Techincally since we are applying openflow rules this is SDN, but treating them like normal routers does not change anything.


#Regular APs
ovs-ofctl add-flow Camera1AP priority=100,actions=normal
ovs-ofctl add-flow Camera2AP priority=100,actions=normal
ovs-ofctl add-flow Camera3AP priority=100,actions=normal
ovs-ofctl add-flow Camera4AP priority=100,actions=normal
#Emergency APs
ovs-ofctl add-flow Emer1AP priority=100,actions=normal
ovs-ofctl add-flow Emer2AP priority=100,actions=normal
ovs-ofctl add-flow Emer3AP priority=100,actions=normal
ovs-ofctl add-flow Emer4AP priority=100,actions=normal

#normal flows for all the switches
ovs-ofctl add-flow s1 priority=100,actions=normal
ovs-ofctl add-flow s2 priority=100,actions=normal
ovs-ofctl add-flow s3 priority=100,actions=normal
ovs-ofctl add-flow s4 priority=100,actions=normal
ovs-ofctl add-flow s5 priority=100,actions=normal
