from mininet.node import *
from os import environ
from mininet.log import setLogLevel, info
import os
PWD= os.getcwd()
#RYUDIR = environ[ 'HOME' ] + '/ryu'
#L2CTLR= PWD + '/../../Controllers/cc_client/layer_2_switch.py'
#L2CTLR= PWD + '/../../Controllers/L2Controller/topo_learner.py'
#TFLCDIR= PWD + '/../../Controllers/tflc'
setLogLevel( 'info' )
###########################################################################################################
class OriginalRYU( Controller ):
    def __init__( self, name,cdir="",
                  command='ryu-manager',
                  cargs=( '--observe-links '
                          '--ofp-tcp-listen-port %s '
                          '--wsapi-port %s '
                          'ryu.app.ofctl_rest '
                          'ryu.app.simple_switch_13'),
                  wsport=9100,
                  **kwargs ):
        print("Original RYU L0 in the host system")
        self.wsport = wsport
        Controller.__init__( self, name,
                             command=command,
                             cargs=cargs, **kwargs )
    ####################################
    def start( self ):
        """Start <controller> <args> on controller.
           Log to /tmp/cN.log"""
        pathCheck( self.command )
        cout = '/tmp/' + self.name + '.log'
        if self.cdir is not None:
            self.cmd( 'cd ' + self.cdir )
        self.cmd( self.command + ' ' + self.cargs % (self.port,self.wsport )+
                  ' 1>' + cout + ' 2>' + cout + ' &' )
        self.execed = False
###########################################################################################################
class DockerRyu( Docker, RemoteController ):
    def __init__( self, name,dimage="ryu-docker",ofpport=6600,wsport=9100,**kwargs ):
        f = os.popen('ifconfig docker0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
        self.exposedIP=f.read().strip()
        self.ofpport=6600
        self.wsport=9100
        Docker.__init__( self, name, dimage, port_bindings={self.ofpport:ofpport,self.wsport:wsport},volumes=["/home/mininet/ScalableSDN/Shared:/mnt/ryu:rw"],**kwargs)
    ####################################
    def start( self ):
        pids=Docker.cmd(self,"ps -ef|grep 'ryu-manager'|awk '{print $2}'|xargs kill -9")
        #Docker.start(self)
        Docker.cmd(self,"nohup ryu/bin/ryu-manager --observe-links --ofp-tcp-listen-port %d --wsapi-port %d ryu.app.ofctl_rest ~/ryu/ryu/app/simple_switch_rest_13.py &"%(self.ofpport,self.wsport))
        RemoteController.__init__(self,self.name,port=self.ofpport,ip=self.exposedIP)
        RemoteController.start(self)
    ####################################
    def stop( self ):
        pids=Docker.cmd(self,"ps -ef|grep 'ryu-manager'|awk '{print $2}'|xargs kill -9")
        Docker.stop(self)
        RemoteController.stop(self)
###########################################################################################################
class OVSDocker( Docker, OVSSwitch ):
    """Open vSwitch Ethernet bridge with Spanning Tree Protocol
       rooted at the first bridge that is created"""
    def __init__(self,name,**kwargs):
      Docker.__init__( self, name, dimage="iwaseyusuke/mininet",**kwargs)
      OVSSwitch.__init__( self, name,failMode='secure',**kwargs )
      #OVSSwitch.__init__( self, name,stp=True,failMode='secure',datapath='kernel',**kwargs )
    ####################################
    def start(self,controllers ):
      OVSSwitch.sendCmd(self,'service', 'openvswitch-switch', 'start')
      OVSSwitch.start(self,[])
      self.controllers=controllers
      connections=["tcp:%s:%d"%(c.exposedIP,c.port_bindings[c.port]) for c in controllers ]
      OVSSwitch.vsctl(self,"set-controller %s %s"%(self.name," ".join(connections)))
    ####################################
    def cleanFlows(self):
      flows=OVSSwitch.cmd(self,"ovs-ofctl dump-flows s1").split("\n")
      flow_tab=[re.split(' |,', f.strip())  for f in  flows if len(f)>0]
      tab_set= set([cell.replace("table=","") for row in flow_tab for cell in row if ("table=" in cell) ])
      connections=["tcp:%s:%d"%(c.exposedIP,c.port_bindings[c.port]) for c in self.controllers ]
      OVSSwitch.vsctl(self,"del-controller %s"%(self.name))
      for tab in tab_set:
        OVSSwitch.cmd(self,"ovs-ofctl del-flows %s 'table=%s'"%(self.name,tab))
      OVSSwitch.vsctl(self,"set-controller %s %s"%(self.name," ".join(connections)))
###########################################################################################################
#controllers={ 'CustomL1': CustomL1,'CustomL2': CustomL2,"OriginalRYU":OriginalRYU}
controllers={ 'DockerRyu': DockerRyu,"OriginalRYU":OriginalRYU}
switches={ "OVSDocker":OVSDocker}
