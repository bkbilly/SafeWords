$( document ).ready(function() {
	getSafewordsLeft();
});

function getSafewordsLeft(){
	$.getJSON("getSafewordsLeft").done(function(data){
		$("#safewordsLeft").val(data);
	});
}

function getSafeWord(){
	$.getJSON("getSafeword").done(function(data){
		$("#firstsafeword").val(data);
		getSafewordsLeft();
	});

}

function uploadSafeWords(){
	var lines = $("#newsafewords").val().split('\n');
	var newdatatoappend = [];
	for (var i=0; i < lines.length; i++) {
		if (/\S/.test(lines[i])) {
			newdatatoappend.push($.trim(lines[i]));
		}
	}
	httprequestdata = {"safewordList": newdatatoappend}
	$.ajax({
		url: "appendSafewords",
		data: httprequestdata,
		type: 'get',
		success: function(data) {
			$("#newsafewords").val("");
			getSafewordsLeft();
		}
	});

}

function clearSafeWords(){
	$.ajax({
		url: "clearSafewords",
		success: function(data) {
			getSafewordsLeft();
		}
	});

}