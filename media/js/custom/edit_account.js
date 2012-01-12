var EditAccount = {};

//------------------------------------------------------------------------------ SELECTORS

EditAccount.Selectors = {
	
	Buttons: {
		edit: '#edit_button',
		exclude: '#exclude_button'
	},
	
	Divs: {
		edit: '#edit_account',
		exclude: '#exclude_account'
	},
	
	TextBoxes: {
		edit: '#edit_text',
		exclude: '#exclude_text'
	},
	
	Forms: {
		edit: '#edit_form',
		exclude: '#exclude_form'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

EditAccount.Functions = {

//------------------------------------------------------------------------------ ShowInitialFields

	showInitialFields: function(serverParams)
	{
		if ( serverParams.isValidForm == 'True' )	
		{
			$(EditAccount.Selectors.Divs.edit).hide();
		}
		
		$(EditAccount.Selectors.Divs.exclude).hide();
		
		EditAccount.Functions.showOrHideEditFields();
		EditAccount.Functions.showOrHideExcludeFields();
		
	},
//------------------------------------------------------------------------------ ShowOrHideEditFields
    
    showOrHideEditFields: function()
    {
        $(EditAccount.Selectors.TextBoxes.edit).click(function() {
        	if ( $(EditAccount.Selectors.Divs.edit).is(':visible') )
        	{
            	$(EditAccount.Selectors.Divs.edit).fadeOut("slow");
        	}
            else
            {
				$(EditAccount.Selectors.Divs.edit).fadeIn("slow");
            }
        
        });
    },	

//------------------------------------------------------------------------------ ShowOrHideExcludeFields    

    showOrHideExcludeFields: function()
    {
        $(EditAccount.Selectors.TextBoxes.exclude).click(function() {
        	if ( $(EditAccount.Selectors.Divs.exclude).is(':visible') )
        	{
            	$(EditAccount.Selectors.Divs.exclude).fadeOut("slow");
        	}
            else
            {
				$(EditAccount.Selectors.Divs.exclude).fadeIn("slow");
            }
        
        });    
    }
    
}
