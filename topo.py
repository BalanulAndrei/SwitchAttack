#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.cli import CLI

def make_network():
	# global net,sw
	net = Mininet()

	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
	
	sw = net.addHost('sw', ip=None)

	net.addLink(h1,sw) # sw-eth0
	net.addLink(h2,sw) # sw-eth1
	net.addLink(h3,sw) # sw-eth2

	net.start()

	# stop routing
	sw.cmd('sysctl -w net.ipv4.ip_forward=0')
	# deactivate IPv6
	for node in net.hosts:
		node.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
		node.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

	sw.cmd('python3 switch.py > /tmp/sw.log 2>&1 &')
	
	# CLI(net)
	
	sw.cmd('kill %python3')
	net.stop()

	return net, sw
