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
        alert("easy");
    });
    // Clicked on MEDIUM
    $("#medium").click(function (){
        alert("medium");
    });
    // Clicked on HARD
    $("#hard").click(function (){
        alert("hard");
    });
});
