
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
     $("#first").modal();
     return false;
 }
 }
 else
 {
     $("#second").modal();
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

