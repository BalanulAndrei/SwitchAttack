#!/usr/bin/env python3

from pathlib import Path
from mininet.net import Mininet
from mininet.cli import CLI


# host1 e mereu atacatorul

hosts = []
switches = []
interfete_switches = []

net = Mininet()



def get_node_name(node):
	if hasattr(node, "name"):
		return node.name

	return node


def get_host_names():
	return [host.name for host in hosts]


def get_switch_names():
	return [switch.name for switch in switches]


def generate_host_mac(host_id):
	return f"00:00:00:00:00:{host_id:02x}"


def customAddHost():
	global hosts

	host_id = len(hosts) + 1

	nume_host = "host" + str(host_id)
	ip_host = "10.0.0." + str(host_id) + "/24"
	mac_host = generate_host_mac(host_id)

	host = net.addHost(
		nume_host,
		ip=ip_host,
		mac=mac_host
	)

	hosts.append(host)

	if net:
		host.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		host.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")

	print(f"\"{nume_host}\" was created!")

	return host


def customAddSwitch():
	global switches

	switch_id = len(switches) + 1

	nume_switch = "switch" + str(switch_id)

	switch = net.addHost(
		nume_switch,
		ip=None,
		mac=None
	)

	switches.append(switch)
	interfete_switches.append(dict())

	if net:
		switch.cmd("sysctl -w net.ipv4.ip_forward=0")
		switch.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		switch.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")

	print(f"\"{nume_switch}\" was created!")

	return switch


def startSwitchProcess(switch):
	if net is None:
		return

	switch.cmd("pkill -f switch.py")

	switch.cmd(
		f"python3 -u switch.py > /dev/null 2>&1 &"
	)


def customAddLinkHS(host, switch):
	host_name = get_node_name(host)
	switch_name = get_node_name(switch)

	hosts_names = get_host_names()
	switches_names = get_switch_names()

	if host_name not in hosts_names:
		print("Error linking H to S: host does not exist")
		return

	if switch_name not in switches_names:
		print("Error linking H to S: switch does not exist")
		return

	host_node = net.get(host_name)
	switch_node = net.get(switch_name)

	link = net.addLink(host_node, switch_node)
	link.intf1.config(up=True)
	link.intf2.config(up=True)
	
	if link.intf1.node.name == switch_name:
		switch_interface = link.intf1.name
	else:
		switch_interface = link.intf2.name

	sw_obj = net.get(switch)

	sw_obj.cmd(f'pkill -f "python3 switch.py {switch}"')
	sw_obj.cmd(f'python3 switch.py {switch} > /tmp/{switch}.log 2>&1 &')

	# index_switch = switches_names.index(switch)
	# interfete_switches[index_switch]["eth" + str(len(interfete_switches[index_switch]))] = host

	index_switch = switches_names.index(switch_name)
	interfete_switches[index_switch][switch_interface] = host_name

	print(f"Linked {host_name} <-> {switch_name}")
	print(f"{switch_name} interface: {switch_interface}")

	# se porneste switchul pentru a invata noile cai

	startSwitchProcess(switch_node)

	return link


def customAddLinkSS(switch1, switch2):
	switch1_name = get_node_name(switch1)
	switch2_name = get_node_name(switch2)

	switches_names = get_switch_names()

	if switch1_name not in switches_names or switch2_name not in switches_names:
		print("Switch error")
		return

	if switch1_name == switch2_name:
		print("Cannot link switch to itself")
		return

	switch1_node = net.get(switch1_name)
	switch2_node = net.get(switch2_name)

	link = net.addLink(switch1_node, switch2_node)

	link.intf1.ifconfig("up")
	link.intf2.ifconfig("up")

	if link.intf1.node.name == switch1_name:
		switch1_interface = link.intf1.name
		switch2_interface = link.intf2.name
	else:
		switch1_interface = link.intf2.name
		switch2_interface = link.intf1.name

	index1 = switches_names.index(switch1_name)
	index2 = switches_names.index(switch2_name)

	interfete_switches[index1][switch1_interface] = switch2_name
	interfete_switches[index2][switch2_interface] = switch1_name

	print(f"Linked {switch1_name} <-> {switch2_name}")
	print(f"{switch1_name} interface: {switch1_interface}")
	print(f"{switch2_name} interface: {switch2_interface}")

	startSwitchProcess(switch1_node)
	startSwitchProcess(switch2_node)

	return link


def createDefaultTopology():
	customAddHost()
	customAddHost()
	customAddSwitch()

	customAddLinkHS(hosts[0].name, switches[0].name)
	customAddLinkHS(hosts[1].name, switches[0].name)


def make_network():
	global network_started

	createDefaultTopology()

	net.start()
	network_started = True

	for switch in switches:
		switch.cmd("sysctl -w net.ipv4.ip_forward=0")
		switch.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		switch.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")

	for node in net.hosts:
		node.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
		node.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")

	for switch in switches:
		startSwitchProcess(switch)


def stop_network():
	for switch in switches:
		switch.cmd("pkill -f switch.py")

	net.stop()


if __name__ == "__main__":
	make_network()
	CLI(net)
	stop_network()