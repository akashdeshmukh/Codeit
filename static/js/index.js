function validateForm()
{
	var firstName = document.getElementById("id_first_name").value.replace(/\s/g, "");
	var lastName = document.getElementById("id_last_name").value.replace(/\s/g, "");
	var rcptno = document.getElementById("id_receipt_no").value.replace(/\s/g, "");

	if (rcptno == "" && firstName == "" && lastName == "")
	{
		$("#example").modal();
		$("#first").modal();
		return false;
	}

	if(isNaN(document.getElementById("id_receipt_no").value))
	{
		$("#second").modal();
		return false; 
	}
	if(isNaN(document.getElementById("id_first_name").value) && isNaN(document.getElementById("id_last_name").value) )
	{
		return true;
	}
	else
	{
		$("#third").modal();
		return false;
	}
}