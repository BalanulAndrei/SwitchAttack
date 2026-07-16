#!/usr/bin/env python3
from flask import Flask, render_template,request,jsonify
from topology import make_network, customAddLink
from mininet import cli 

app = Flask(__name__, static_folder="public")

global net,sw

@app.route("/")
def start():
	return render_template('site.html')

@app.route("/show_info")
def ping_info():
	if net is None:
		return "Network is not running"
	
	# output = cli('dump')

	# return f"<pre>{output}</pre>"

@app.route("/ping_test")
def ping_test():
	if net is None:
		return "Network is not running"

	h1 = net.get('h1')

	output = h1.cmd('ping -c 3 10.0.0.2')

	return f"<pre>{output}</pre>"

@app.route("/add_link", methods=['POST'])
def add_link():
	data = request.get_json()

	node_from = data.get('from')
	node_to = data.get('to')

	if not node_from or not node_to:
		return jsonify({"status": "error", "message": "Missing ID"}), 1

	print(f"Instructing Mininet to link Node {node_from} and Node {node_to}...")


	return jsonify({
	    "status": "success", 
	    "message": f"Successfully linked {node_from} to {node_to}"
	})

if __name__ == "__main__":
	net,sw = make_network()

	try:
		app.run(debug=True, port=5000, use_reloader=False)
	finally:
		print("Stopping network...")
		if sw:
			sw.cmd('kill %python3')
		if net:
			net.stop()