#!/bin/bash
#Regular APs
ovs-ofctl add-flow Camera1AP actions=normal
ovs-ofctl add-flow Camera2AP actions=normal
ovs-ofctl add-flow Camera3AP actions=normal
ovs-ofctl add-flow Camera4AP actions=normal
#Emergency APs
ovs-ofctl add-flow Emer1AP actions=normal
ovs-ofctl add-flow Emer2AP actions=normal
ovs-ofctl add-flow Emer3AP actions=normal
ovs-ofctl add-flow Emer4AP actions=normal

#normal flows for all the switches
ovs-ofctl add-flow s1 actions=normal
ovs-ofctl add-flow s2 actions=normal
ovs-ofctl add-flow s3 actions=normal
ovs-ofctl add-flow s4 actions=normal
ovs-ofctl add-flow s5 actions=normal
