let hCnt = 2;
let swCnt = 1;
var nodes = new vis.DataSet([
	{ id: 1, label: "User 1" },
	{ id: 2, label: "User 2" },
	{ id: 3, label: "Switch 1" }
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
	});
}
function addSwitch(){
	swCnt ++;
	nodes.add({
		id: swCnt + hCnt,
		label: "Switch " + swCnt,
	})
}
var options = {
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