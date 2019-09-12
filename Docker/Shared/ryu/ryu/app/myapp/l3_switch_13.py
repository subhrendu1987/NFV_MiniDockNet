# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.app import simple_switch_13
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import *


class SimpleSwitch13(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.ip_to_port = {}

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        ip= pkt.get_protocols(ipv4.ipv4)[0] if(len(pkt.get_protocols(ipv4.ipv4))) else None
        if(not ip):
            super(SimpleSwitch13, self)._packet_in_handler(ev)
            return
        dpid = datapath.id
        self.ip_to_port.setdefault(dpid, {})
        self.ip_to_port[dpid][ip.src] = in_port 

        if ip.dst in self.ip_to_port[dpid]:
            ip_out_port = self.ip_to_port[dpid][ip.dst]
        else:
            ip_out_port = ofproto.OFPP_FLOOD
        # learn a mac address to avoid FLOOD next time.
        self.ip_to_port[dpid][ip.src] = in_port

        if ip.dst in self.ip_to_port[dpid]:
            out_port = self.ip_to_port[dpid][ip.dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        ip_actions = [parser.OFPActionOutput(ip_out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            ip_match = parser.OFPMatch(in_port=in_port, ipv4_dst=ip.dst, ipv4_src=ip.src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, ip_match, ip_actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, ip_match, ip_actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        ip_out=parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=ip_actions, data=data)
        flow_property={"MSG":"IP_Property","dpid":dpid,"ip":ip,'actions':ip_actions}
        self.logger.info(flow_property)
        datapath.send_msg(ip_out)
