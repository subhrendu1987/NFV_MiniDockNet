## Folder Structure
RawTopology		--> Topology Store for experiments
Controllers		--> L1 and L2 Wrappers to be used for mininet automated controller setup
mininet_script	--> Mininet driver scripts for experimentation
scikit-optimize	--> Python library used for BO
ryu + ryu.diff	--> L2 controller implementation
BaysianOptimization	--> BO finds the optimum switch controller assignment
results			--> 
util			--> Plots generation from results
Documents		--> Reports and posters
## Setup instructions
Required python packages
`sudo -E pip install bottle, bottledaemon`
## Instructions
### Create Controller docker
`sudo docker build NFV/Docker/ryu-docker -t ryu-docker`
### Execute command in a node
``



`cd ~/ScalableSDN/util;sudo python mnexecWrapper.py -h`
`cd ~/ScalableSDN/util;sudo python mnexecWrapper.py -l`
`cd ~/ScalableSDN/util;sudo python mnexecWrapper.py -n <node_name> -cmd <cmd>`
### Invoke data center clos tree topology in mininet
`cd ~/ScalableSDN/mininet_script/TestTopo;sudo python topo-clos-like.py`
### Check mininet stat using REST
`http://172.16.117.50:8081/switches`
### Enforce switch-controller assignment based on ~/ScalableSDN/Controllers/cc_client/switch_controller_config.json
`cd ~/ScalableSDN/BaysianOptimization; sudo python mininetChangeAssignment.py`


### View log of c0
`sudo docker run --name mn.c0 -it ryu-docker /bin/bash`
`sudo docker logs --follow $(sudo docker inspect --format="{{.Id}}" mn.c0)`
