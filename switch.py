#!/usr/bin/env python3

from collections import deque
from scapy.all import sniff, sendp, Ether, get_if_list


mac_table = {}
mac_queue = deque()

MAX_MAC_ENTRIES = 32


def get_switch_interfaces():
	interfaces = []

	for interface in get_if_list():
		if interface != "lo":
			interfaces.append(interface)

	return interfaces


def is_multicast_or_broadcast(mac_address):
	first_octet = int(mac_address.split(":")[0], 16)
	return first_octet & 1 == 1


def learn_mac(source_mac, incoming_interface):
	if is_multicast_or_broadcast(source_mac):
		return

	old_interface = mac_table.get(source_mac)

	if old_interface == incoming_interface:
		return

	if old_interface is None:
		print(f"LEARN: {source_mac} -> {incoming_interface}", flush=True)
		mac_queue.append(source_mac)
	else:
		print(
			f"MAC MOVE: {source_mac}: "
			f"{old_interface} -> {incoming_interface}",
			flush=True
		)

	mac_table[source_mac] = incoming_interface

	if len(mac_table) > MAX_MAC_ENTRIES:
		remove_oldest_mac()


def remove_oldest_mac():
	while mac_queue:
		oldest_mac = mac_queue.popleft()

		if oldest_mac in mac_table:
			print(f"CAM FULL: removed {oldest_mac}", flush=True)
			del mac_table[oldest_mac]
			return


def flood_packet(packet, incoming_interface, interfaces):
	for interface in interfaces:
		if interface != incoming_interface:
			sendp(packet, iface=interface, verbose=False)


def forward_packet(packet, outgoing_interface, incoming_interface):
	if outgoing_interface == incoming_interface:
		return

	sendp(packet, iface=outgoing_interface, verbose=False)


def process_packet(packet):
	if not packet.haslayer(Ether):
		return

	interfaces = get_switch_interfaces()

	source_mac = packet[Ether].src
	destination_mac = packet[Ether].dst
	incoming_interface = packet.sniffed_on

	learn_mac(source_mac, incoming_interface)

	if is_multicast_or_broadcast(destination_mac):
		flood_packet(packet, incoming_interface, interfaces)
		return

	if destination_mac in mac_table:
		outgoing_interface = mac_table[destination_mac]
		forward_packet(packet, outgoing_interface, incoming_interface)
	else:
		flood_packet(packet, incoming_interface, interfaces)


def main():
	interfaces = get_switch_interfaces()

	if len(interfaces) == 0:
		print("Switch has no interfaces. Exiting.", flush=True)
		return

	print(f"Switch running on interfaces: {interfaces}", flush=True)

	sniff(
		iface=interfaces,
		prn=process_packet,
		store=False,
		filter="inbound"
	)


if __name__ == "__main__":
	main()