FROM ubuntu:16.04
# sudo docker build -t vnf:latest vnf
MAINTAINER Subhrendu Chattopadhyay <subhrendu@iitg.ac.in>
#ENV http_proxy 'http://172.16.117.50:4128'
#ENV https_proxy 'http://172.16.117.50:4128'
#ENV ftp_proxy 'http://172.16.117.50:4128'

EXPOSE 6600 9100
ENV HOME /root
WORKDIR /root


ENV HOME /root
WORKDIR /root
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common && add-apt-repository ppa:nm-l2tp/network-manager-l2tp && apt-get install -y --no-install-recommends network-manager-l2tp \
	network-manager-l2tp-gnome \
	net-tools \
	telnet\
	inetutils*

#CMD ["sh","-c","cd /Shared; ryu/bin/ryu-manager --observe-links --ofp-tcp-listen-port 6600 --wsapi-port 9100 ryu.app.ofctl_rest ryu.app.simple_switch_rest_13"]
