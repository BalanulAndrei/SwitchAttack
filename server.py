#!/usr/bin/env python3
from flask import Flask, render_template,request,jsonify
# from topology import make_network, customAddLink
from mininet import cli 
import topology
import attack_controller

app = Flask(__name__, static_folder="public")

# global net,sw

@app.route("/")
def start():
	return render_template('site.html')
@app.route("/add_switch", methods=['POST'])
def add_switch_topo():
	try:
		switch = topology.customAddSwitch() 

		return jsonify({
				"status": "success", 
				"message": "A new switch was successfully added",
				"switch": switch.name
			})
	except Exception as e:
		return jsonify({
			"status": "error", 
			"message": str(e) 
		}), 500
@app.route("/add_host", methods=['POST'])
def add_host_topo():
	try:
		host = topology.customAddHost() 

		return jsonify({
			"status": "success",
			"message": f"{host.name} was successfully added.",
			"host": host.name,
			"ip": host.params.get("ip", "Not assigned"),
			"mac": host.params.get("mac", "Not assigned")
		})
	except Exception as e:
		return jsonify({
			"status": "error", 
			"message": str(e)
		}), 500
@app.route("/show_info")
def show_info():
	if topology.net is None:
		return "Network is not running yet."

	output = "Dump:\n"
	output += "======================\n\n"

	output += "Hosts:\n"
	for host in topology.hosts:
		host_ip = host.params.get('ip', 'Not Assigned')
		host_mac = host.params.get('mac', 'Not Assigned')
		output += f"  - {host.name}: IP={host_ip}, MAC={host_mac}\n"
	
	output += "\nSwitches:\n"
	for switch in topology.switches:
		output += f"  - {switch.name}\n"
	
	output += "\nLinks:\n"
	for link in topology.net.links:
		node1 = link.intf1.name
		node2 = link.intf2.name
		output += f"  - {node1} <---> {node2}\n"

	return f"<pre>{output}</pre>"
@app.route("/ping_test", methods=['POST'])
def ping_test():
	if topology.net is None:
		return "Network is not running"

	data = request.get_json()
	host1 = data.get('source')
	host2 = data.get('destination')

	host1 = "host" + str(host1)
	host2 = "host" + str(host2)
	
	host1 = topology.net.get(host1)
	destination = topology.net.get(host2)

	destination_ip = destination.params.get('ip')
	final_ip = destination_ip[:-3:]
	output = host1.cmd(f'ping -c 3 {final_ip}')

	return output

@app.route("/add_link", methods=['POST'])
def add_link():
	data = request.get_json()

	node_from = int(data.get('from'))
	node_to = int(data.get('to'))

	node_aux1 = min(node_from,node_to)
	node_aux2 = max(node_from,node_to)

	if node_from + node_to > 180:
		node_aux1 -= 89
		node_aux2 -= 89
		node_1 = "switch" + str(node_aux1)
		node_2 = "switch" + str(node_aux2)
		print(node_1 + " & " + node_2)
		topology.customAddLinkSS(node_1,node_2)
	else:
		node_aux2 -= 89
		node_1 = "host" + str(node_aux1)
		node_2 = "switch" + str(node_aux2)
		print(node_1 + " & " + node_2)
		topology.customAddLinkHS(node_1,node_2)

	if not node_from or not node_to:
		return jsonify({"status": "error", "message": "Missing ID"}), 1



	return jsonify({
	    "status": "success", 
	    "message": f"Successfully linked {node_1} to {node_2}"
	})

@app.route("/attack/mac_flood", methods=["POST"])
def mac_flood_route():
	try:
		data = request.get_json() or {}

		attacker = data.get("attacker", "host1")
		count = int(data.get("count", 100))
		interval = float(data.get("interval", 0.01))

		log_path = attack_controller.start_mac_flood(
			attacker_name=attacker,
			count=count,
			interval=interval
		)

		return jsonify({
			"status": "success",
			"message": f"MAC flood started from {attacker}.",
			"log": log_path
		})

	except Exception as error:
		return jsonify({
			"status": "error",
			"message": str(error)
		}), 500
@app.route("/attack/pod", methods=["POST"])
def pod_route():
	try:
		data = request.get_json() or {}

		attacker = data.get("attacker", "host1"())
		victim = data.get("victim", "host2")
		interval = float(data.get("interval", 0.01))

		log_path = attack_controller.start_pod(
			attacker_name=attacker,
			victim_name=victim,
			interval=interval
		)

		return jsonify({
			"status": "success",
			"message": f"PoD-like started: {attacker} -> {victim}.",
			"log": log_path
		})

	except Exception as error:
		return jsonify({
			"status": "error",
			"message": str(error)
		}), 500
@app.route("/attack/<attack_name>/log")
def attack_log_route(attack_name):
	log = attack_controller.read_attack_log(attack_name)
	return f"<pre>{log}</pre>"

if __name__ == "__main__":

	topology.make_network()

	try:
		app.run(debug=True, port=5000, use_reloader=False)
	finally:
		print("Stopping network...")
		for sw in topology.switches:
			sw.cmd('kill %python3')

		topology.net.stop()