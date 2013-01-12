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
    // Clicked on EASY
    $("#easy").click(function (){
        //alert("easy");
        $.getJSON('http://127.0.0.1:8000/questions/1/',
            function(data){
                alert('Fetched ' + data.length + ' items!');
            }
            )
    });
    // Clicked on MEDIUM
    $("#medium").click(function (){
        //alert("medium");
        $.getJSON('http://127.0.0.1:8000/questions/2/',
            function(data){
                alert('Fetched ' + data.length + ' items!');
            }
            )
    });
    // Clicked on HARD
    $("#hard").click(function (){
        //alert("hard");
        $.getJSON('http://127.0.0.1:8000/questions/3/',
            function(data){
                alert('Fetched ' + data.length + ' items!');
            }
            )
    });
});
