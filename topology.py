#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.cli import CLI

cnt_hosts = 2

hosts = []
switches = []

net = Mininet()


# TODO: Create the default topology on start

def customAddHost():
	global hosts
	nume_host = "host" + str(len(hosts)+1)
	ip_host = "10.0.0." + str(len(hosts)+1) + "/24"
	mac_host = "00:00:00:00:00:" + str(hex(len(hosts)+1))
	h = net.addHost(nume_host, ip=ip_host, mac=mac_host)
	hosts.append(h)
	print(f"\"{nume_host}\" was created!")

def customAddSwitch():
	global switches
	nume_switch = "switch" + str(len(switches)+1)
	ip_switch = None
	mac_host = None
	sw = net.addHost(nume_host, ip=ip_host, mac=mac_host)

	switches.append([])	# TODO: logica pentru lista de switches

	print(f"\"{nume_switch}\" was created!")

def customAddLink(host, switch):
	if host in hosts and switch in hosts:
		print("Cannot link 2 hosts!")
		return
	

def make_network():
	pass


	# net = Mininet()

	# h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	# h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	# # h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
	
	# sw1 = net.addHost('sw1', ip=None)

	# net.addLink(h1,sw1) # sw1-eth0
	# net.addLink(h2,sw1) # sw1-eth1
	# # net.addLink(h3,sw1) # sw1-eth2

	# net.start()

	# # stop routing
	# sw1.cmd('sysctl -w net.ipv4.ip_forward=0')
	# # deactivate IPv6
	# for node in net.hosts:
	# 	node.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
	# 	node.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

	# sw1.cmd('python3 switch.py > /tmp/sw1.log 2>&1 &')
	
	# CLI(net)
	
	# sw1.cmd('kill %python3')
	# net.stop()

if __name__ == '__main__':
	make_network()