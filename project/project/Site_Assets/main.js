var API_PREFIX = "/api/";

function http_get(url) {
	var request = new XMLHttpRequest();
	request.open("GET", url, false);
	request.send(null);
	return request.responseText;
}
function on_manoeuvre_click() {
	var manoeuvre_name = event.srcElement.value;
	var url = `${API_PREFIX}set_manoeuvre/${manoeuvre_name}`;
	http_get(url);
}
function retrieve_maneuvers() {

	var url = `${API_PREFIX}get_manoeuvres`;
	var json = http_get(url);
	
	var maneuvers_array = JSON.parse(json);
	
	var manoeuvre_div = document.getElementById("manoeuvre_list");
	 
	for (var manoeuvre in maneuvers_array) {
		var h2 = document.createElement("h2");
		h2.innerText = 	maneuvers_array[manoeuvre];
		h2.value = maneuvers_array[manoeuvre];
		h2.onclick = on_manoeuvre_click;
		h2.classList.add('manoeuvre');
		manoeuvre_div.appendChild(h2);
	}

}
window.addEventListener('load', retrieve_maneuvers);