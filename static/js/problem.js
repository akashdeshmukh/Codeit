/* add content for problem.js here */
var control = $("#id_code"),
function validateForm()
{
 var control = $("#id_code");
 if (control.val())
 {
   var picked = $("#id_picked");
   var n=control.val().toLowerCase().split(".");
   var x=n.length;
   if ( n[x-1] == picked.val())
       return true;
   else
   {
     alert("Uploaded file format does not match with selected");
     return false;
 }
 }
 else
 {
     alert("Please select a file to upload");
     return false;
 }
    }
    var control = $("#id_code"),
    clearBn = $("#clear");

    clearBn.on("click", function(){
    // Some browsers will actually honor .val('')
    // So I'm adding it back onto the solution
    control.replaceWith( control.val('').clone( true ) );
    });

