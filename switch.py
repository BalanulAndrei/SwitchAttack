#!/usr/bin/env python3
from scapy.all import sniff, sendp, Ether, get_if_list
from topology import hosts, switches, interfete_switches

# switches[] retine obiecte de tip mininet switch

tabela_mac = {}

interfaces=[]

def get_switch_interfaces():
	interfaces = []

	for interface in get_if_list():
		if interface != "lo":
			interfaces.append(interface)

	return interfaces

def proceseaza_pachet(pachet):
	if not pachet.haslayer(Ether):
		return
	mac_sursa = pachet[Ether].src
	mac_dest = pachet[Ether].dst
	interf_intr = pachet.sniffed_on


	if tabela_mac.get(mac_sursa) != interf_intr:
		print(f"{mac_sursa} - {interf_intr}")
	tabela_mac[mac_sursa] = interf_intr

	if mac_dest in tabela_mac:
		interf_iesire = tabela_mac[mac_dest]
		if interf_iesire != interf_intr:
			sendp(pachet, iface=interf_iesire, verbose=False)
	else:
		for iface in interfaces:
			if iface != interf_intr:
				sendp(pachet, iface=iface, verbose=False)

interfaces = get_switch_interfaces()

print("Switch is running")
sniff(iface=interfaces,prn=proceseaza_pachet, store=0, filter="inbound")