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
			url: "/perfil/livrosfavoritos/remover/" + id + "/",
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
