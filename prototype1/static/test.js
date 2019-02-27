var dumpJSONtoConsole = function(response_data_json) {
	console.log("start dump");
	var codeElement = document.getElementById("codeId");
	
	var prop;
	for(prop in response_data_json) {
		codeElement.innerText += prop + response_data_json[prop] + "\n";
		console.log(prop);	
	}

	//codeElement.innerText = response_data_json;	
	console.log(response_data_json);
}

var sendMessagePost = function() {
	var boxElem = document.getElementById("box");
	$.ajax({
		type:"POST",
		url: "/message",
		data:{"message": boxElem.value},
		success: dumpJSONtoConsole
	});
	console.log(boxElem.value)
}

var sendJWT = function() {
	var boxElem = document.getElementById("box2");
	var boxElem = document.getElementById("box");
	$.ajax({
		type:"POST",
		url: "/send",
		data:{"message": boxElem.value},
		success: dumpJSONtoConsole
	});
	console.log(boxElem.value)
}
