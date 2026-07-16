#!/usr/bin/env python3
from flask import Flask, render_template
from mininet.net import Mininet
from mininet.cli import CLI

app = Flask(__name__, static_folder="public")

net = None
sw = None

@app.route("/")
def start():
    return render_template('site.html')


@app.route("/ping_test")
def ping_test():
    """Example function to call from your web interface"""
    if net is None:
        return "Network is not running yet."
    
    h1 = net.get('h1')
    
    output = h1.cmd('ping -c 3 10.0.0.2')
    
    return f"<pre>{output}</pre>"

@app.route("/stop_switch_script")
def stop_switch():
    if sw is None:
        return "Switch not found."
    
    sw.cmd('kill %python3')
    return "Switch script stopped via web interface."


def setup_network():
    global net, sw 
    
    net = Mininet()

    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    
    sw = net.addHost('sw', ip=None)

    net.addLink(h1, sw) # sw-eth0
    net.addLink(h2, sw) # sw-eth1
    net.addLink(h3, sw) # sw-eth2

    net.start()

    # stop routing
    sw.cmd('sysctl -w net.ipv4.ip_forward=0')
    # deactivate IPv6
    for node in net.hosts:
        node.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
        node.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

    sw.cmd('python3 switch.py > /tmp/sw.log 2>&1 &')

if __name__ == "__main__":
    print("Starting Mininet network in the background...")
    setup_network()
    
    try:
        print("Network is running! Starting Flask server...")
        app.run(debug=True, port=5000, use_reloader=False)
    finally:
        print("Stopping network...")
        if sw:
            sw.cmd('kill %python3')
        if net:
            net.stop()