var RegisterPayment = {};

//-------------------------------------------------------------------------------- SELECTORS

RegisterPayment.Selectors = {
	
	Buttons: {
		register: '#button_register'
	}
}

//-------------------------------------------------------------------------------- FUNCTIONS

RegisterPayment.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = RegisterPayment.Selectors.Buttons;
		
		$(btn.register).click( RegisterPayment.Functions.registerNewPayment );	
	},

//----------------------------------------------------------------------- registerNewPayment	
	registerNewPayment: function()
	{
		var $div = $('#register_payment'),
			$messageContainer = $div.find("div.message_container"),
		    data = {};
		
		data['invoice'] = $("#id_invoice").val();
		data['duplicate'] = $("#id_duplicate").val();
		data['payment_date'] = $("#id_payment_date").val();
		
		$.ajax({
			url: "/gerenciarlivraria/pagamento/cadastrar/",
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