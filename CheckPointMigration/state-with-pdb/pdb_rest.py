#!/usr/bin/python
from bottle import Bottle, request
import time, subprocess, json, sys
sys.path.append("../modified_pdb")
import modified_pdb
from bottledaemon import daemon_run
"""
MininetRest adds a REST API to mininet.
"""
protocols='OpenFlow13'
IP="127.0.0.1"
PORT="38081"
##########################################################################################
class PdbRest(Bottle):
    ############################################################
    def run(self,**kwargs):
        #daemon_run(**kwargs)
        super(PdbRest, self).run(**kwargs)
        #print("Run Called")
        #This can not be used as mininet is already running in main thread
        #super(MininetRest, self).run(reloader=True,**kwargs) 
    ############################################################
    def __init__(self, net):
        super(PdbRest, self).__init__()
        self.prog_name = ""
        self.route('/start/<prog_name>', callback=self.start)
        '''
        self.route('/nodes', callback=self.get_nodes)
        self.route('/nodes/<node_name>', callback=self.get_node)
        self.route('/nodes/post/<node_name>/<params>', method='GET', callback=self.post_node)
        self.route('/nodes/cmd/<cmd_name>', method='GET', callback=self.do_cmd)
        self.route('/nodes/<node_name>/mnexec/<cmd>', method='GET', callback=self.mnexec)
        self.route('/nodes/<node_name>/cmdPrint/<cmd>', method='GET', callback=self.cmdPrint)
        self.route('/switches/rules/<switch_name>', method='GET', callback=self.ovsrules)
        self.route('/nodes/<node_name>/<intf_name>', callback=self.get_intf)
        self.route('/nodes/post/<node_name>/<intf_name>/<params>', method='GET', callback=self.post_intf)
        self.route('/hosts', method='GET', callback=self.get_hosts)
        self.route('/hosts/post/<host_name>', method='GET', callback=self.get_host_info)
        self.route('/switches', method='GET', callback=self.get_switches)
        self.route('/links', method='GET', callback=self.get_links)
        self.route('/controllers', method='GET', callback=self.get_ctlrs)
        self.route('/ctlrport', method='GET', callback=self.get_ctlrs_wsport)
        self.route('/neighbor', method='GET', callback=self.get_neighbors)
        self.route('/interfaces', method='GET', callback=self.get_intfs)
        '''
    ############################################################
    def start(self, prog_name, params):
        ''' Start program in pdb mode'''
        return({'Return':"%s started"%(prog_name)})
    ############################################################
##########################################################################################