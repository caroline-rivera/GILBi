var RegisterBookstoreBook = {};

//-------------------------------------------------------------------------------- SELECTORS

RegisterBookstoreBook.Selectors = {
	
	Buttons: {
		register: '#button_register_book'
	}
}

//-------------------------------------------------------------------------------- FUNCTIONS

RegisterBookstoreBook.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = RegisterBookstoreBook.Selectors.Buttons;
		
		$(btn.register).click( RegisterBookstoreBook.Functions.registerNewBookstoreBook );	
	},

//----------------------------------------------------------------- registerNewBookstoreBook	
	registerNewBookstoreBook: function()
	{
		var $div = $('#register_bookstore_book'),
			$messageContainer = $div.find("div.message_container"),
		    data = {};
		
		data['book'] = $("#id_book").val();
		data['price'] = $("#id_price").val();
		data['total_quantity'] = $("#id_total_quantity").val().trim();
		data['available_quantity'] = $("#id_available_quantity").val().trim();
		
		$.ajax({
			url: "/gerenciarlivraria/cadastrarlivro/cadastrar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				if( (response['validation_message']).length != 0 )
				{
					Helpers.Functions.showValidationMsg($messageContainer, 
														response['validation_message']);
				}
				else
				{
					if( (response['error_message']).length != 0 )
					{
						Helpers.Functions.showErrorMsg($messageContainer, 
															response['error_message']);
					}
					if( (response['success_message']).length != 0 )
					{
						Helpers.Functions.showSuccessMsg($messageContainer, 
															response['success_message']);
					}
				}
									
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	}
}	