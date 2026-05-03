This Repo is for our course project in EE6220 where we were supposed to use SDN to improve network performance.  This repo has two subfolders PythonSrc and OpenFlowScripts.  PythonSrc has all the python applications meant to be ran on each node.  OpenFlowScripts is were the flows are stored there is some automation.  On the top folder, there is one topology script.  All plots are stored in Plots.ipynb.  The figures are saved in Images.
To run the topology run
```
sudo -E python Topology.py
```
Now to treat the network like a normal one run the following command (chmod +x the .sh file).
```
sh OpenFlowScripts/./NormalRouterOpenflowCMDs.sh
```
The network is ready to be used now.  
Now if you want to use the slightly different SDN version run the following command (chmod +x the .sh file).
```
sh OpenFlowScripts/./OpenflowCMDs.sh
```
The network is ready now.  This one has some restrictions to where traffic is permitted vs not permitted.  Flows also have set priorties, to allow certain traffic to flow with higher priority than other traffic.
Unfortunately Mininet doesn't like large networks (also it does very badly with cycles, even with proper rules) so results will vary.  There is some automation that is controlled by the middleboxes.  It adds a flow where data to the emergency center is given higher priority.

The only thing I gathered from this project is how OpenFlow works, some SDN concepts that I couldn't apply. Very little time was spent on actually solving a problem, most of it was spent trying to figure out why the tools do not work. 
Which really means that this project did not contribute to my knowledge really and felt like a massive waste of time. 
Figuring out tooling does not give actual value to learning SDN if anything it just hampers it and shows the course is not thoughtout and designed to waste my time.
