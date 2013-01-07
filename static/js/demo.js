$(document).ready(function() {
	$("#nameLabel").fadeIn(1800);
	$("#nameDiv").show(1000);

});

function showStatement() {
	$("#nameDiv").toggle("slow");
	$("#statementLabel").fadeIn(1800);
	$("#statementDiv").show(1000);
	pageScroll();
}

function showSampleIp() {
	$("#statementDiv").toggle("slow");
	$("#sampleIpLabel").fadeIn(1800);
	$("#sampleIpDiv").show(1000);
	pageScroll();
}

function showSampleOp() {
	$("#sampleIpDiv").toggle("slow");
	$("#sampleOpLabel").fadeIn(1800);
	$("#sampleOpDiv").show(1000);
}

function pageScroll() {
    window.scrollBy(0,100);
    scrolldelay = setTimeout('pageScroll()',50);
}
