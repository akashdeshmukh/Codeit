/* add content for problem.js here */
var control = $("#id_code"),
    clearBn = $("#clear");

clearBn.on("click", function(){
    // Some browsers will actually honor .val('')
    // So I'm adding it back onto the solution
    control.replaceWith( control.val('').clone( true ) );
});

