This Repo is for our course project in EE6220 where we were supposed to use SDN to improve network performance.  This repo has two subfolders PythonSrc and OpenFlowScripts.  PythonSrc has all the python applications meant to be ran on each node.  OpenFlowScripts is were the flows are stored.  On the top folder, there is two topology scripts where one is meant to be used with no SDN (routers act normal) and SDN (routers follow OpenFlow flows).  

To run the No SDN topology run the following

```
sudo -E python NoSDNTopology.py
```
After this step, when it is finshed loading run (make sure to run chmod +x on this file)
```
sh OpenFlowScripts/./NormalRouterOpenflowCMDs.sh
```
The network is ready to be used now.  

For the SDN topology simiarlly do the following
```
sudo -E python SDNTopology.py
```
Once again after it finishes loading (make sure to run chmod +x on this file)
```
sh OpenFlowScripts/./OpenflowCMDs.sh
```
The network is ready now.  This one has a lot of restrictions to where traffic is permitted vs not permitted.  Flows also have set priorties, to allow certain traffic to flow with higher priority than other traffic.
Unfortunately Mininet doesn't like large networks (also it does very badly with cycles, even with proper rules) so results will vary.  

The only thing I gathered from this project is how OpenFlow works, some SDN concepts that I couldn't apply. Very little time was spent on actually solving a problem, most of it was spent trying to figure out why the tools do not work. 
Which really means that this project did not contribute to my knowledge really and felt like a massive waste of time.  Figuring out tooling does not give actual value to learning SDN if anything it just hampers it and shows the course is not thoughtout in the SDN portion. 
