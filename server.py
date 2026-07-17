#!/usr/bin/env python3
from flask import Flask, render_template,request,jsonify
# from topology import make_network, customAddLink
from mininet import cli 
import topology

app = Flask(__name__, static_folder="public")

# global net,sw

@app.route("/")
def start():
	return render_template('site.html')

@app.route("/show_info")
def show_info():
	if topology.net is None:
		return "Network is not running yet."

	output = "Dump:\n"
	output += "======================\n\n"

	output += "Hosts:\n"
	for host in topology.net.hosts:
		output += f"  - {host.name}: IP={host.IP()}, MAC={host.MAC()}\n"
	
	output += "\nSwitches:\n"
	for switch in topology.net.switches:
		output += f"  - {switch.name}\n"
	
	output += "\nLinks:\n"
	for link in topology.net.links:
		node1 = link.intf1.node.name
		node2 = link.intf2.node.name
		output += f"  - {node1} <---> {node2}\n"

	return f"<pre>{output}</pre>"

@app.route("/ping_test")
def ping_test():
	if topology.net is None:
		return "Network is not running"

	h1 = topology.net.get(topology.hosts[0])

	output = h1.cmd('ping -c 3 10.0.0.2')

	return f"<pre>{output}</pre>"

@app.route("/add_link", methods=['POST'])
def add_link():
	data = request.get_json()

	node_from = int(data.get('from'))
	node_to = int(data.get('to'))

	node_1 = min(node_from,node_to)
	node_2 = max(node_from,node_to)

	if node_from + node_to > 180:
		nodeSwitch1 = "switch" + str(node_1 - 89)
		nodeSwitch2 = "switch" + str(node_2 - 89)
		print(nodeSwitch1 + " & " + nodeSwitch2)
		topology.customAddLink(nodeSwitch1,nodeSwitch2)
	else:
		nodeHost = "host" + str(node_1)
		nodeSwitch = "switch" + str(node_2 - 89)
		print(nodeHost + " & " + nodeSwitch)
		topology.customAddLink(nodeHost,nodeSwitch2)

	if not node_from or not node_to:
		return jsonify({"status": "error", "message": "Missing ID"}), 1



	return jsonify({
	    "status": "success", 
	    "message": f"Successfully linked {node_from} to {node_to}"
	})

if __name__ == "__main__":

	topology.make_network()

	try:
		app.run(debug=True, port=5000, use_reloader=False)
	finally:
		print("Stopping network...")
		for sw in switches:
			sw.cmd('kill %python3')

		topology.net.stop()