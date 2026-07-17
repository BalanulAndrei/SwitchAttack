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

def customAddLinkHS(host, switch):

	hosts_names = []
	switches_names = []

	for x in hosts:
		hosts_names.append(x.name)
	for x in switches:
		switches_names.append(x.name)

	if host in hosts_names and switch in hosts_names:
		print("Cannot link 2 hosts!")
		return
	if not (host in hosts_names and switch  in switches_names):
		print("Error linking H to S")
		return


	global net
	net.addLink(host, switch) # Am facut link intre dispozitive
	# Incerc sa fac interfetele
	# Fiecare switch va fi un dictionar cu perechile HostXX - ethXX
	# Caut indicele lui host in hosts si acela va fi 'XX'

	index_switch = switches_names.index(switch)

	interfete_switches[index_switch]["eth" + str(len(interfete_switches[index_switch]))] = host

def customAddLinkSS(switch1, switch2):

	switches_names = []

	for x in switches:
		switches_names.append(x.name)

	if switch1 not in switches_names or switch2 not in switches_names:
		print("Switch error")
		return

	global net
	net.addLink(switch1, switch2) 

	try:
		index1 = switches_names.index(switch1)
	except:
		print("Eroare 1")
	try:
		index2 = switches_names.index(switch2)
	except:
		print("Eroare 2")

	interfete_switches[index1]["eth" + str(len(interfete_switches[index1]))] = switch2
	interfete_switches[index2]["eth" + str(len(interfete_switches[index2]))] = switch1


def createDefaultTopology():
	global net, hosts, switches, interfete_switches
	# Default topology without links
	customAddHost()
	customAddHost()
	customAddSwitch()

	customAddLinkHS(hosts[0].name, switches[0].name)
	customAddLinkHS(hosts[1].name, switches[0].name)

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