let hCnt = 2;
let swCnt = 90;
var DIR = "/public/images/";
var userPng = DIR + "laptop.png";
var switchPng = DIR + "switch.png";
var nodes = new vis.DataSet([
	{ id: 1, label: "User 1", image: userPng, shape: "image"},
	{ id: 2, label: "User 2", image: userPng, shape: "image"  },
	{ id: 90, label: "Switch 1", image: switchPng, shape: "image" }
]);
var edges = new vis.DataSet([
	{ from: 1, to: 90 },
	{ from: 90, to: 2 },
]);
var container = document.getElementById("mynetwork");
var data = {
	nodes: nodes,
	edges: edges
};
function addUser(){
	hCnt ++;
	nodes.add({
		id: hCnt,
		label: "User " + hCnt,
		image: userPng,
		shape: "image"
	});
}
function addSwitch() {
	fetch('/add_switch', {
		method: 'POST',
		headers: {
		    'Content-Type': 'application/json'
		},
		body: JSON.stringify({ next_id: swCnt + 1 })
	})
	.then(response => response.json())
	.then(serverData => {
		if (serverData.status === "success") {
			swCnt++;
		
			nodes.add({
				id: swCnt,
				label: "Switch " + (swCnt - 89),
				image: switchPng,
				shape: "image"
			});
		
			console.log(serverData.message);
		} else {
			console.error("Backend error:", serverData.message);
		}
	})
	.catch(error => {
		console.error("Network error:", error);
	});
}
var options = {
	edges: { color: "black" },
	manipulation: {
		enabled: false, 
		addEdge: function (edgeData, callback) {
		
		if (edgeData.from === edgeData.to) {
			alert("You can't connect a link to itself");
			callback(null);
			return;
		}
		if (edgeData.from + edgeData.to < 90) {
			alert("You can't connect 2 hosts to themselves")
			callback(null);
			return;
		}
		callback(edgeData);
		fetch('/add_link', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					from: edgeData.from,
					to: edgeData.to
				})
			})
			.then(response => response.json())
			.then(serverData => {
				if (serverData.status === "success") {
					//For testing reasons
					//TODO: Change back
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					console.log(serverData.message);
					callback(edgeData);
				} 
				else {
					console.error(serverData.message);
					alert("Backend failed to link nodes.");
					callback(null);
				}
			})
			.catch(error => {
				console.error("Network error:", error);
				alert("Could not reach the server.");
				callback(null);
			});
		}
	}
};
	var network = new vis.Network(container, data, options);
function activeazaDesenareLegatura() {
	/* TODO: Make button toggable*/
	network.addEdgeMode();
}