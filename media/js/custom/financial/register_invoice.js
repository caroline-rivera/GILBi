var RegisterInvoice = {};

//-------------------------------------------------------------------------------- SELECTORS

RegisterInvoice.Selectors = {
	
	Buttons: {
		add: '#button_add_duplicate',
		remove: '#button_remove_duplicate',
		save: '#button_save_invoice'
	}
}

//-------------------------------------------------------------------------------- FUNCTIONS

RegisterInvoice.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = RegisterInvoice.Selectors.Buttons;
		
		$(btn.add).click( RegisterInvoice.Functions.addDuplicateFields );	
		$(btn.remove).click( RegisterInvoice.Functions.removeDuplicateFields );
		$(btn.save).click( RegisterInvoice.Functions.registerNewInvoice );

	},

//----------------------------------------------------------------------- addDuplicateFields	
	addDuplicateFields: function()
	{     
        var $duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length,
            number = existentDuplicates + 1,
            fields = "",
            field_date= '#expiration_date_' + number,
            value_date= '#value_' + number;
        
        if (existentDuplicates > 0) {
         
            var $lastDuplicate = $duplicates.find("li").filter(":last"),
            	expirationDate = $lastDuplicate.find("input").filter("[id^=expiration]").val();
                value = $lastDuplicate.find("input").filter("[id^=value]").val();
            
            if (!(expirationDate) || !(value) || (value.trim() == "")) {
                alert("Preencha os campos da duplicata anterior primeiro!");
                return;
            }
        }        
        
        fields += '<div class="tab_save_button"></div>';
        fields += '<ul><label>(*) Número da Duplicata:</label>'
        fields += '<input type="text" id="number_"'+number+'" value="'+number+'" disabled="disabled" />';
        fields += '</ul><ul><label>(*) Data de Expiração:</label>';
        fields += '<input id="expiration_date_'+number+'" type="text" maxlength="10"/>';
        fields += '</ul><ul><label>(*) Valor:</label>';
        fields += '<input id="value_'+number+'" type="text" maxlength="10"/>';
        fields += '</ul>';
        
        $("<li/>")
        	.append(fields)
        	.appendTo($duplicates);
        	
        $(field_date).datepicker();
        $(value_date).maskMoney({symbol:'R$ ', showSymbol:true, thousands:'', decimal:'.', symbolStay: true});
	},
	
//----------------------------------------------------------------------- removeDuplicateFields	
	removeDuplicateFields: function()
	{  
        var $duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length;
        
        if (existentDuplicates > 1) {    	        
			$duplicates.find("li").filter(":last").remove();
        }
	},
	
//----------------------------------------------------------------------- registerNewInvoice	
	registerNewInvoice: function()
	{
		var $div = $('#register_invoice'),
			$messageContainer = $div.find("div.message_container"),
			$duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length;
		
		var response = RegisterInvoice.Functions.validateForm();   
		
		if (response.length != 0) {
			Helpers.Functions.showValidationMsg($messageContainer, response);
		}
		else {		
			var data = RegisterInvoice.Functions.getRegisterInvoiceData();
		
			RegisterInvoice.Functions.sendRegisterInvoiceData($messageContainer, data);
		}
	
	},
	
//----------------------------------------------------------------------- validateForm	
	validateForm: function()
	{
		var $duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length,
			messages = [],
			messageIndex = 0;

			if ( $("#id_purchase_order").val() == "") {
				messages[messageIndex] = "O campo Pedido de Compra é obrigatório.";
				messageIndex++;
			}

			if ( $("#id_number").val().trim() == "") {
				messages[messageIndex] = "O campo Número da Nota Fiscal é obrigatório.";
				messageIndex++;
			}
			
			if ( $("#id_series").val().trim() == "") {
				messages[messageIndex] = "O campo Número de Série é obrigatório.";
				messageIndex++;
			}
			
		for (var i = 1; i <= existentDuplicates; i++) {
			
			var field_date = '#expiration_date_' + i,
				field_value = '#value_' + i;

			if ( $(field_date).val().trim() == "") {
				messages[messageIndex] = "O campo Data de Expiração da Duplicata número " + i + " é obrigatório.";
				messageIndex++;
			}
			
			if ( $(field_value).val().trim() == "") {
				messages[messageIndex] = "O campo Valor da Duplicata número " + i + " é obrigatório.";
				messageIndex++;
			}
		}

		return messages;	
	},

//---------------------------------------------------------------- getRegisterInvoiceData	
	getRegisterInvoiceData: function()
	{	
		var data = {},
			$duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length;
        			
		data['purchase_order'] = $("#id_purchase_order").val();		
		data['number'] = $("#id_number").val();
		data['series'] = $("#id_series").val();
		data['duplicates_number'] = existentDuplicates;
		
		for (var i = 1; i <= existentDuplicates; i++) {
						
			var field_date = '#expiration_date_' + i,
				field_value = '#value_' + i;	
	
			duplicateArray = [];	
			duplicateArray[0] = i;
			duplicateArray[1] = $(field_date).val().trim();
			duplicateArray[2] = $(field_value).val().trim();
			
			data['duplicate_' + i] = duplicateArray.join(";");
		}	
		
		return data;
	},
		
//---------------------------------------------------------------- sendRegisterInvoiceData	
	sendRegisterInvoiceData: function($messageContainer, data)
	{		
		$.ajax({
			url: "/gerenciarlivraria/notafiscal/cadastrar/",
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
						RegisterInvoice.Functions.cleanPageData();
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
	},


//------------------------------------------------------------------------- cleanPageData	
	cleanPageData: function()
	{
        var $duplicates = $("#duplicates"),
        	existentDuplicates = $duplicates.find("li").length;
        
        while (existentDuplicates != 1)	{
        	RegisterInvoice.Functions.removeDuplicateFields();
        	existentDuplicates = existentDuplicates - 1;
        }
        	
		$('#id_purchase_order').val("");	
		$('#id_number').val("");	
		$('#id_series').val("");
		
		$('#expiration_date_1').val("");	
		$('#value_1').val("");	
	}

}	

        /*$("<li/>")
        	.append('<div class="tab_save_button"></div>')
        	.append('<ul><label>(*) Número da Duplicata:</label>')
        	.append('<input type="text" id="number_"'+number+'" value="'+number+'" disabled="disabled" />')
        	.append('</ul><ul><label>(*) Data de Expiração:</label>')
        	.append('<input id="expiration_date_'+number+'" type="text" />')
        	.append('</ul><ul><label>(*) Valor:</label>')
        	.append('<input id="value_'+number+'" type="text" />')
        	.append('</ul>')
            .appendTo($duplicates);*/