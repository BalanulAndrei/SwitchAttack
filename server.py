#!/usr/bin/env python3
from flask import Flask, render_template
from topology import make_network

app = Flask(__name__, static_folder="public")

global net,sw

@app.route("/")
def start():
    return render_template('site.html')


@app.route("/ping_test")
def ping_test():
    if net is None:
        return "Network is not running"
    
    h1 = net.get('h1')
    
    output = h1.cmd('ping -c 3 10.0.0.2')
    
    return f"<pre>{output}</pre>"

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