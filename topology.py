#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.cli import CLI

hosts = []
switches = []
interfete_switches = []

net = Mininet()

# TODO: Create the default topology on start
# DONE

def customAddHost():
	global hosts
	nume_host = "host" + str(len(hosts)+1)
	ip_host = "10.0.0." + str(len(hosts)+1) + "/24"
	mac_digits = str(hex(len(hosts)+1))[2:]
	if len(mac_digits) == 1:
		mac_digits = "0" + mac_digits
	mac_host = "00:00:00:00:00:" + mac_digits
	h = net.addHost(nume_host, ip=ip_host, mac=mac_host)
	hosts.append(h)
	print(f"\"{nume_host}\" was created!")

def customAddSwitch():
	global switches
	nume_switch = "switch" + str(len(switches)+1)
	ip_switch = None
	mac_switch = None
	sw = net.addHost(nume_switch, ip=ip_switch, mac=mac_switch)

	switches.append(sw)	# TODO: logica pentru lista de switch
						# DONE
	interfete_switches.append(dict()) # adaug un dictionar gol pentru a face perechea hostXX <==>ethXX
	print(f"\"{nume_switch}\" was created!")

def customAddLink(host, switch):
	if host in hosts and switch in hosts:
		print("Cannot link 2 hosts!")
		return
	global net
	net.addLink(host, switch) # Am facut link intre dispozitive
	# Incerc sa fac interfetele
	# Fiecare switch va fi un dictionar cu perechile HostXX - ethXX
	# Caut indicele lui host in hosts si acela va fi 'XX'
	index_host = hosts.index(host)
	# Pozitia i - Host(i+1) / Eth(i+1) | Exemplu: lists[0] <==> host1/eth1 

	index_switch = switches.index(switch)

	nume_host = "host" + str(index_host+1)
	nume_interfata = "eth" + str(index_host+1)
	interfete_switches[index_switch][nume_host] = nume_interfata


def createDefaultTopology():
	global net, hosts, switches, interfete_switches\
	# Default topology without links
	customAddHost()
	customAddHost()
	customAddSwitch()

	customAddLink(hosts[0], switches[0])
	customAddLink(hosts[1], switches[0])

	# Links intre host1-switch1 si host2-switch1


def make_network():

	global net, hosts, switches, interfete_switches

	createDefaultTopology()

	net.start()

	# stop routing

	for sw in switches:
		sw.cmd('sysctl -w net.ipv4.ip_forward=0')

	# deactivate IPv6
	for node in net.hosts:
		node.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
		node.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

	for sw in switches:
		sw.cmd('python3 switch.py > /tmp/switches.log 2>&1 &')



if __name__ == '__main__':
	make_network()