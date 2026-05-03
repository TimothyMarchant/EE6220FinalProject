To run these python files, run new terminal windows with xterm for each node.  
Node names Camera station: Camerasx where x is 1,2,3, or 4. Middlebox: Midx where x is either 1 or 2.  Datacenter: data.  Emergency center: Emerctr (mininet doesn't like long names).  Emergency Car: EmerCar1 (there was meant to be more cars, but I left it like this).  The APs do not need to be touched.
It is assumed you ran the openflow scripts.
To run each file in this folder some instructions are given.
To run CameraClient.py
```
py CameraClient.py TARGETIPADDRESS
```
To run MiddleboxServer.py
```
py MiddleboxServer.py WINDOWTITLE CAMERABUTTON1 CAMERABUTTON2 IP
```
To run DataCenterServer.py
```
py DataCenterServer.py
```
To run EmergencyCenterServer.py
```
py EmergencyCenterServer.py
```
To run EmergencyCar.py
```
py EmergencyCar.py WINDOWTITLE
```
The other scripts are called by these files.  You do not run them by themselves.
