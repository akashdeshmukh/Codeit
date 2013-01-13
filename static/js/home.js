function changePointer(x) {
    x.style.cursor="pointer";
    x.style.backgroundColor="#000000";
    x.style.color="#ffffff";
}


function changePointer2(x) {
    x.style.backgroundColor="#D3D3D3";
    x.style.color="#000000";
}

$(document).ready(function() {
    // data is a collection of questions of a particular type
    // Iterate over it to extract fields and display them on page
    // Clicked on EASY
    $("#easy").click(function () {
        $.get('http://0.0.0.0:8000/questions/1', function(data) {
            console.log(data[0].fields);
        });
    });
    // Clicked on MEDIUM
    $("#medium").click(function (){
        $.get('http://0.0.0.0:8000/questions/2', function(data) {
            console.log(data[0].fields);
        });
    });
    // Clicked on HARD
    $("#hard").click(function (){
        $.get('http://0.0.0.0:8000/questions/3', function(data) {
            console.log(data[0].fields);
        });
    });
});
