#!/bin/bash
SourceFolder=OpenFlowScripts
chmod +x $SourceFolder/S1OpenFlow.sh
chmod +x $SourceFolder/S2OpenFlow.sh
chmod +x $SourceFolder/S3OpenFlow.sh
chmod +x $SourceFolder/S4OpenFlow.sh
chmod +x $SourceFolder/S5OpenFlow.sh
chmod +x $SourceFolder/S6OpenFlow.sh
chmod +x $SourceFolder/APOpenFlow.sh


$SourceFolder/./S1OpenFlow.sh
$SourceFolder/./S2OpenFlow.sh
$SourceFolder/./S3OpenFlow.sh
$SourceFolder/./S4OpenFlow.sh
$SourceFolder/./S5OpenFlow.sh
$SourceFolder/./S6OpenFlow.sh
$SourceFolder/./APOpenFlow.sh

