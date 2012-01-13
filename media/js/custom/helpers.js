var Helpers = {};

//------------------------------------------------------------------------------ MESSAGES

Helpers.Messages = {
	
	All: {
		ERROR_LOADING_TABLE: 'Erro ao carregar a tabela.',	
		ERROR_UNEXPECTED: 'Ocorreu um erro inesperado.'	
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

//------------------------------------------------------------------------------ showValidationMsg	
	showValidationMsg: function(id, msg)
	{
		divMsg = $("#" + id);
		divMsg.show();
		//divMsg.addClass("validation");
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
		//divMsg.removeClass("validation");
	},
	
//------------------------------------------------------------------------------ showSuccessMsg	
	showSuccessMsg: function(id, msg)
	{
		divMsg = $("#" + id);
		divMsg.show();
		//divMsg.addClass("success");
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
		//divMsg.removeClass("success");
	},
//------------------------------------------------------------------------------ showErrorMsg	
	showErrorMsg: function(id, msg)
	{
		divMsg = $("#" + id);
		divMsg.show();
		//divMsg.addClass("error");
		divMsg.html(msg);
		setTimeout("$(\"#".concat(id, "\").hide();"), 6000);
		//divMsg.removeClass("error");
	}
}