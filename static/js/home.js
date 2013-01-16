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
     $.get('/questions/1/', function(data) {
            $('#myproblems').empty();
            for(var i=0; i < data.length; i++){
                var link = (i+1) + ". " + '<a href=\"/problem/' + data[i].pk + '/\">' + data[i].fields.name;
                link = '<br>' + link  + '</a>';
                $('#myproblems').append(link);
            }
        });
    $("#easy").click(function () {
        $.get('/questions/1/', function(data) {
            $('#myproblems').empty();
            for(var i=0; i < data.length; i++){
                var link = (i+1) + ". " + '<a href=\"/problem/' + data[i].pk + '/\">' + data[i].fields.name;
                link = '<br>' + link  + '</a>';
                $('#myproblems').append(link);
            }
        });
    });
    // Clicked on MEDIUM
    $("#medium").click(function (){
        $.get('/questions/2/', function(data) {
            $('#myproblems').empty();
            for(var i=0; i < data.length; i++){
                var link = (i+1) + ". " + '<a href=\"/problem/' + data[i].pk + '/\">' + data[i].fields.name;
                link = '<br>' + link  + '</a>';
                $('#myproblems').append(link);
            }
        });
    });
    // Clicked on HARD
    $("#hard").click(function (){
        $.get('/questions/3/', function(data) {
            $('#myproblems').empty();
            for(var i=0; i < data.length; i++){
                var link = (i+1) + ". " + '<a href=\"/problem/' + data[i].pk + '/\">' + data[i].fields.name;
                link = '<br>' + link  + '</a>';
                $('#myproblems').append(link);
            }
        });
    });
});

