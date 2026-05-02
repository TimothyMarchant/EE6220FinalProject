#!/bin/bash

###The purpose of this file is to run all the openflow scripts.  It takes a minute to run them all.

SourceFolder=OpenFlowScripts
#Allow each bash script to be ran.
chmod +x $SourceFolder/S1OpenFlow.sh
chmod +x $SourceFolder/S2OpenFlow.sh
chmod +x $SourceFolder/S3OpenFlow.sh
chmod +x $SourceFolder/S4OpenFlow.sh
chmod +x $SourceFolder/S5OpenFlow.sh
chmod +x $SourceFolder/S6OpenFlow.sh
chmod +x $SourceFolder/APOpenFlow.sh

#Run each script.
##Middlebox scripts
$SourceFolder/./S1OpenFlow.sh
$SourceFolder/./S2OpenFlow.sh
##Middle switch for general connection.  This one connects all the nodes together.
$SourceFolder/./S3OpenFlow.sh
#Data center and emergency flows.  These are simple
$SourceFolder/./S4OpenFlow.sh
$SourceFolder/./S5OpenFlow.sh
#AP flows
$SourceFolder/./APOpenFlow.sh

