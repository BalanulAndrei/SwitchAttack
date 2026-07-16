let hCnt = 2;
let swCnt = 1;
var DIR = "/public/images/"
var userPng = DIR + "laptop.png"
var switchPng = DIR + "switch.png"
var nodes = new vis.DataSet([
	{ id: 1, label: "User 1", image: userPng, shape: "image"},
	{ id: 2, label: "User 2", image: userPng, shape: "image"  },
	{ id: 3, label: "Switch 1", image: switchPng, shape: "image" }
]);
var edges = new vis.DataSet([
	{ from: 1, to: 3 },
	{ from: 3, to: 2 },
]);
var container = document.getElementById("mynetwork");
var data = {
	nodes: nodes,
	edges: edges
};
function addUser(){
	hCnt ++;
	nodes.add({
		id: swCnt + hCnt,
		label: "User " + hCnt,
		image: userPng,
		shape: "image"
	});
}
function addSwitch(){
	swCnt ++;
	nodes.add({
		id: swCnt + hCnt,
		label: "Switch " + swCnt,
		image: switchPng,
		shape: "image"
	})
}
var options = {
	edges: { color: "black" },
	manipulation: {
		enabled: false, 
		addEdge: function (edgeData, callback) {
		
		if (edgeData.from === edgeData.to) {
			alert("You can't connect a link to itself");
			callback(null); // Anulează desenarea
			return;
		}
		callback(edgeData);
		}
	}
};
	var network = new vis.Network(container, data, options);
function activeazaDesenareLegatura() {
	/*Make button toggable*/
	network.addEdgeMode();
}