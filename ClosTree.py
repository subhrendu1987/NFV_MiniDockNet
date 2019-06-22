"""ClosTree topology by Howar31
http://www.hoggnet.com/NWWPics/CLOS%20Network.jpg

sudo mn --custom ~/mininet/custom/topo-clos-like.py --topo clostree --switch ovs-stp --controller=remote,ip=127.0.0.1,port=6633
sudo mn --custom ~/mininet/custom/topo-clos-like.py --topo clostree --switch ovs --controller=ref
mininet> sh time bash -c 'while ! ovs-ofctl show es_0_0 | grep FORWARD; do sleep 1; done'

Pass '--topo=fattree' from the command line
"""
#from mininet.net import mininet
from mininet.topo import Topo
from mininet.net import Containernet
from mininet_rest import MininetRest
from mininet.log import setLogLevel, info
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch, UserSwitch, Ryu
from mininet.cli import CLI
from mininet.link import TCLink
from CustomCtlr import *
from os import environ,system
import json, itertools, thread,logging,sys
protocols="OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13"
##########################################################################################
class StreamToLogger(object):
    '''Fake file-like stream object that redirects writes to a logger instance'''
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
    ################################################################
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
##########################################################################################
def getVal(d,key):
    return(d[key] if key in d.keys() else None)
##########################################################################################
class ClosTree( Topo ):
    def __init__( self,racks=6,hostsPerRack=20,ctlrNo = 1,ipBase='11.0.0.1/24'):
        # Initialize topology
        Topo.__init__( self)
        # Topology settings
        #(racks,hostsPerRack,ctlrNo)=(6,20,3)
        hostNum = (racks*hostsPerRack)   # Hosts in ClosTree
        rackSwitchNum = racks            # Core switches 
        spineSwitchNum = (racks/2)       # Edge switches
        # Device Lists
        rackSwitches = []
        spineSwitches = []
        hosts=[]
        hostLinks=[]

        #net = Containernet(controller=Controller)
        net = Containernet(ipBase=ipBase)
        info("*** CONTROL PLANE STARTS\n")
        info("*** Add Central Controller for debugging\n")
        port_bindings={6600:6600,9100:9100}
        c0=net.addController(name="c0",controller=DockerRyu,ofpport=getVal(port_bindings,6600),wsport=getVal(port_bindings,9100))
        info("*** DATA PLANE STARTS\n")
        info("*** Add spine switches\n")
        for spine in xrange(1, (spineSwitchNum+1)):
            s = net.addSwitch("spine"+str(spine), cls=OVSDocker,protocols=protocols)
            spineSwitches.append(s)

        info("*** Add leaf/rack switches\n")
        for rack in xrange(1, (rackSwitchNum+1)):
            s = net.addSwitch("rack"+str(rack+spineSwitchNum),cls=OVSDocker, protocols=protocols)
            rackSwitches.append(s)

        info("*** Add inter-switch links\n")
        for h_num,spine in enumerate(spineSwitches):
            rackLinks=[net.addLink(spine, rack) for rack in rackSwitches]
        # Edges and hosts
        rack_id = 0
        multiplier=pow(10,len(str(hostsPerRack)))

        info("*** Create hosts and links between host and switchs\n")
        for rack in rackSwitches:
            for x in xrange(1,(hostsPerRack+1)):
                h_num = (rack_id * hostsPerRack)+ x
                #hopts={"ip":"%s.%s.%d/%d"%(IPbase,rack_id,x,mask)}
                h=net.addDocker("h"+str(h_num), dimage="ubuntu:trusty")
                hosts.append(h)
                hostLinks.append(net.addLink(rack,h,cls=TCLink))
            rack_id += 1
        info("*** All devices are deployed\n")
        self.net=net
        self.rackSwitches =rackSwitches # Core switches in ClosTree
        self.spineSwitches = spineSwitches # Edge switches in ClosTree
        self.hosts=hosts # Hosts in ClosTree
        self.hostLinks=hostLinks # Links in ClosTree
        self.c0=net.controllers[0]
        self.controllers=net.controllers
        return
    ################################################################
    def startNetwork(self,SwitchMappingDict=None,REST=False):
        net=self.net
        net.build()
        #if self.c0 is not None:
        #    self.c0.start()
        for c in net.controllers:
            c.start()
        if(SwitchMappingDict==None):
            info("*** Add all switches to first available controller\n")
            for sw in net.switches:
                sw.start([self.c0])
        else:
            info("*** Use switch to controller mapping from %s\n"%(config_file))
            for sw in SwitchMappingDict.keys():
                net.getNodeByName(sw).start([net.getNodeByName(SwitchMappingDict[sw])])
        info("*** Set arp table\n")
        for host in self.hosts:
            for host1 in self.hosts:
                if host.name != host1.name:
                    host.setARP(host1.IP(), host1.MAC())
        info("*** Create shell variable\n")
        resTemp=[n.cmd('name=\"%s\"'%(n.name)) for n in net.hosts]
        resTemp=[n.cmd('name=\"%s\"'%(n.name)) for n in net.switches]
        resTemp=[n.cmd('name=\"%s\";connect=\"%s:%s:%s\"'%(n.name,n.protocol,n.ip,n.port)) for n in net.controllers]
        if(REST):
            info("*** Super controller WSGI help http://0.0.0.0:8081/index\n")
            self.monitor=thread.start_new_thread(self.startMininetRest,())
        return(net)
    ################################################################
    def startMininetRest(self):
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            filename="/tmp/monitor.log",filemode='a')
        stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(stderr_logger, logging.INFO)
        sys.stderr = sl
        info("*** Start Mininet Rest\n")
        mininet_rest = MininetRest(self.net)
        mininet_rest.run(host="0.0.0.0",port=8081, quite=True)
    ################################################################
    def stop(self):
        info("*** Stop Mininet Rest\n")
        info("*** Stopping network\n")
        self.net.stop()
        system("mn -c")
##########################################################################################
