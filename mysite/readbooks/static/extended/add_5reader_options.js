$(document).ready(function(){
	$("#datepicker").datepicker();
	$("#datepicker").datepicker("option", "dateFormat", $("#date_format").val());
	$("#datepicker_book").datepicker();
	$("#datepicker_book").datepicker("option", "dateFormat", $("#date_format").val());

	$("#new_author_form").hide();
	$("#new_genre_form").hide();
	$("#new_publisher_form").hide();
	$("#new_group_form").hide();
	$("#currents_stats_div").hide();

	$("#book_form_btn").click(function(){
		$("#new_book_form").toggle("fade");
		$("#new_author_form").hide();
		$("#new_genre_form").hide();
		$("#new_publisher_form").hide();
		$("#new_group_form").hide();
	});

	$("#author_form_btn").click(function(){
		$("#new_author_form").toggle("fade");
		$("#new_book_form").hide();
		$("#new_group_form").hide();
		$("#new_genre_form").hide();
		$("#new_publisher_form").hide();
	});

	$("#publisher_form_btn").click(function(){
		$("#new_publisher_form").toggle("fade");
		$("#new_book_form").hide();
		$("#new_group_form").hide();
		$("#new_genre_form").hide();
		$("#new_author_form").hide();
	});

	$("#genre_form_btn").click(function(){
		$("#new_genre_form").toggle("fade");
		$("#new_book_form").hide();
		$("#new_group_form").hide();
		$("#new_publisher_form").hide();
		$("#new_author_form").hide();
	});

	$("#group_form_btn").click(function(){
		$("#new_group_form").toggle("fade");
		$("#new_book_form").hide();
		$("#new_genre_form").hide();
		$("#new_publisher_form").hide();
		$("#new_author_form").hide();
	});

	$("#current_stats_btn").click(function(){
		$("#all_form_btns_div").toggle("hide");
		$("#currents_stats_div").fadeToggle("show");
	});

	// $("#author_submit_btn").click(function(){
	// 	if (!allowSubmit)	{
	// 	// 	e.preventDefault();
	// 		preview_author_data();
	// 		allowSubmit = true;
	// 	// }
	// 	}

	// });


	function previewAuthorData(){
		var firstName = $('input[name="first_name"]').val(), labelFirstName=$('label[for="id_first_name"]').text(), lastName = $('input[name="last_name"]').val(), labelLastName=$('label[for="id_last_name"]').text();
		var nameData = '<h2>' + labelFirstName + '<strong>' + firstName + '</strong></h3><h3>' + labelLastName + '<strong>' + lastName + '</strong></h2>';

		var bio = $('input[name="bio"]').val(),	labelBio = $('label[for="id_bio"]').text();
		var bioData = '<h4>' + labelBio + '<strong>' + bio + '</strong></h4>';

		var gender = $('input[type="radio"]:checked').val(),labelGender =$('label[for="gender_choices"]').text(), genderVal='Undefined';
		if (gender=='Female'){ gender_val='Female';} else if (gender=='Male'){ gender_val='Male';}

		var genderData = '<h4>'+labelGender+'<strong>'+genderVal+'</strong></h4>';

		var date0fBirth = $('input[name="date_of_birth"]').val(),labelDateOfBirth = $('label[for="datepicker"]').text();
		var dateOfBirthData = '<h4>'+labelDateOfBirth+'<strong>'+dateOfBirth+'</strong></h4>';

		var authorData = nameData+bioData+genderData+dateOfBirthData;

		// $('#preview_author_data').html('');
		$('#preview_author_data').append(authorData);

		$('#preview_author_data').dialog({
			modal:true,
			buttons:{
				OK: function(){
					$(this).dialog("close");
				} 
			}
		});
	}	


 });