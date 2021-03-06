var Helpers = {};

//------------------------------------------------------------------------------ MESSAGES

Helpers.Messages = {
	
	All: {
		ERROR_LOADING_TABLE: 'Ocorreu um erro inesperado no carregamento da tabela.',	
		ERROR_UNEXPECTED: 'Ocorreu um erro inesperado. Por favor, contate o administardor do sistema.'	
	},
	
	RegisterEmployee: {
		NO_SEL_ARROW: 'Nenhum usuário foi selecionado na tabela!',
		SUCCESS_REGISTER_MANAGER: 'O(s) novo(s) gerente(s) foi(ram) cadastrado(s) com sucesso!',
		SUCCESS_REGISTER_SELLER: 'O(s) novo(s) vendedor(es) foi(ram) cadastrado(s) com sucesso!',
		ERROR_LOADING_TABLE: 'Erro ao carregar a tabela.',
		ERROR_SAVING_EMPLOYEE: 'Erro ao salvar funcionário(s).'
	},
	
	Book: {
		NO_SEL_ARROW: 'Nenhum livro foi selecionado na tabela!',	
		ERROR_SAVING_BOOK: 'Erro ao salvar livros. Tente novamente.',	
	},
	
	Order: {
		NO_SEL_ARROW: 'Nenhuma encomenda foi selecionada na tabela!',
		ERROR_CANCELING_ORDER: 'Erro ao cancelar encomenda. Tente novamente.'
	},
	
	Bookstore: {
		ERROR_LOADING_LOANS: 'Erro ao carregar lista de livros emprestados.'
	},
	
	Library: {
		ERROR_LOADING_LOANS: 'Erro ao carregar lista de livros emprestados.'
	},
	
	ManageLibrary: {
		ERROR_LOADING_BOOK_INFORMATION: 'Erro ao carregar informações de livro.',
		ERROR_BORROWING_BOOK: 'Erro inesperado ao emprestar livro.',
		ERROR_RECEIVING_BOOK: 'Erro inesperado ao receber livro.',
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

Helpers.Functions = {

//------------------------------------------------------------------------------ showPopUpErrorMsg	
	// TODO: Remover essa função
	showPopUpErrorMsg: function(divMsg, id, msg)
	{
		divMsg.show();
		divMsg.css('background-color', '#FFDAB9');
		divMsg.css('border', '1px solid #FF0000');
		divMsg.css('border-radius', '10px');
		divMsg.css('-moz-border-radius', '10px');
		divMsg.css('-webkit-border-radius', '10px');
		divMsg.css('min-height', '30px');
		divMsg.css('padding-top', '10px');
		divMsg.css('margin-bottom', '30px');
		divMsg.css('width', '400px');
		divMsg.css('text-align', 'center');
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
	},

//------------------------------------------------------------------------------ showPopUpSuccessMsg	
	// TODO: Remover essa função
	showPopUpSuccessMsg: function(divMsg, id, msg)
	{
		divMsg.show();
		divMsg.css('background-color', '#9AFF9A');
		divMsg.css('border', '1px solid #00CD00');
		divMsg.css('border-radius', '10px');
		divMsg.css('-moz-border-radius', '10px');
		divMsg.css('-webkit-border-radius', '10px');
		divMsg.css('min-height', '30px');
		divMsg.css('padding-top', '10px');
		divMsg.css('padding-left', '30px');
		divMsg.css('margin-bottom', '30px');
		divMsg.css('width', '400px');
		divMsg.css('text-align', 'left');
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
	},

//------------------------------------------------------------------------------ showPopUpWarningMsg	
	// TODO: Remover essa função
	showPopUpWarningMsg: function(divMsg, id, msg)
	{
		divMsg.show();
		divMsg.css('background-color', '#FAFAD2');
		divMsg.css('border', '1px solid #CD950C');
		divMsg.css('border-radius', '10px');
		divMsg.css('-moz-border-radius', '10px');
		divMsg.css('-webkit-border-radius', '10px');
		divMsg.css('min-height', '30px');
		divMsg.css('padding-top', '10px');
		divMsg.css('padding-left', '30px');
		divMsg.css('margin-bottom', '30px');
		divMsg.css('width', '400px');
		divMsg.css('text-align', 'left');
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
	},
	
//--------------------------------------------------------------------------- createListedMessege	
	createListedMessege: function(listOfMessages)
	{
		var listedMessages = "";
		
		listedMessages += "<span>Corrija as seguintes informações:</span>";
		listedMessages += "<ul>";
		
		for (var i = 0; i < listOfMessages.length; i++)
		{
			listedMessages += "<li>";
			listedMessages += listOfMessages[i];
			listedMessages += "</li>";
		}
		
		listedMessages += "</ul>";
		
		return listedMessages;
	},

//--------------------------------------------------------------------------- showValidationMsg	
	showValidationMsg: function($messageContainer, text)
	{
		var listedMessage = Helpers.Functions.createListedMessege(text);
		Helpers.Functions.showMessage($messageContainer, "validation", listedMessage);
	},
//------------------------------------------------------------------------------ showSuccessMsg	
	showSuccessMsg: function($messageContainer, text)
	{
		Helpers.Functions.showMessage($messageContainer, "success", text);
	},
//------------------------------------------------------------------------------ showErrorMsg	
	showErrorMsg: function($messageContainer, text)
	{
		Helpers.Functions.showMessage($messageContainer, "error", text);
	},
//------------------------------------------------------------------------------ showWarningMsg	
	showWarningMsg: function($messageContainer, text)
	{
		Helpers.Functions.showMessage($messageContainer, "warning", text);
	},
	
//------------------------------------------------------------------------------ showMessage	
	showMessage: function($messageContainer, type, text)
	{
		var types = "error success warning validation";
		
		$messageContainer
			.removeClass(types)
			.addClass(type)
			.html(text)
			.show()
			.stop(true, false)
			.animate({ opacity: 1.0 }, 6000, function() {
		       $(this).fadeOut(500);
		    });
	},
	
//------------------------------------------------------------------------------ listFn	
	listFn: function(data, grid)
	{		
		grid.clearGridData();
		
		for(var i = 0; i < data.length; i++)
        {
            grid.jqGrid('addRowData', i, data[i]);
        }
		
	},
	
//------------------------------------------------------------------------------ isValidQuantity	
	isValidQuantity: function(stringNumber)
	{		
		var reDigits = /^\d+$/;		
		
		return reDigits.test(stringNumber);		
	},
}	
