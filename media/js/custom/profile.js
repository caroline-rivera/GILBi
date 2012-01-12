var Profile = {};

//------------------------------------------------------------------------------ SELECTORS

Profile.Selectors = {
	
	Buttons: {
		ok: '#ok_button'
	},
	
	Divs: {
		editStatus: '#edit_status',
		status: '#status'
	},
	
	Forms: {
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

Profile.Functions = {

//------------------------------------------------------------------------------ ShowInitialFields

	init: function(serverParams)
	{
		var btn = Profile.Selectors.Buttons;
		
		if ( serverParams.errorMessage == 'False' )	
		{
			$(Profile.Selectors.Divs.editStatus).hide();
		}
		else
		{
			$(Profile.Selectors.Divs.status).hide();
		}

     	$(btn.ok).button();
     	
        $(Profile.Selectors.Divs.status).click(function() {
        	$(Profile.Selectors.Divs.status).fadeOut("fast");
           	$(Profile.Selectors.Divs.editStatus).fadeIn("fast");	        
        }); 				
	},
	
	removeFavoriteBooks: function(id)
	{
		var data = {};		
		var element = '#favorite_' + id;
	    	
		$.ajax({
			url: "/perfil/removerlivrofavorito/" + id + "/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {	
				$(element).remove();					
			},
			error: function() {		
			}
		});	
	}
    
}


/*
		$(function() {
			$('#edit_status').hide();
     
	        $('#status').click(function() {
	        	$('#status').fadeOut("fast");
	           	$('#edit_status').fadeIn("fast");	        
	        });
	        
	        $('#ok_button').click(function() {
	        	debugger;
	        	var description = $('#description').val();
	        	var description_length = description.length;
	        	if( description_length > 100)
	        	{
	        		$('#error_msg').css(
						        		{"background":"url({{ MEDIA_URL }}/img/icons/error.png) no-repeat 10px 10px #fdf0eb",
						        		"border":"solid 1px #cd0a0a"}
						        		);
					$('#error_msg').html("").append("Tamanho máximo de 100 caracteres.").slideDown("fast").delay(3500).slideUp("fast");
				}
				else
				{
					$('#form_edit_status').submit($.post("/perfil/alterarstatus/"));
				}
	        });	        
		});	
*/