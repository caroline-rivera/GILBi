var ManageLibrary = {};

//------------------------------------------------------------------------------ SELECTORS

ManageLibrary.Selectors = {
	
	Buttons: {
		save: '#button_register_book',
		search: '#button_search',
		borrow: '#button_borrow',
		receive: '#button_receive'
	},
	
	Tables: {
		loans: '#table_loans'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

ManageLibrary.Functions = {

//------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = ManageLibrary.Selectors.Buttons;

		/* Funcoes para a tab1: Cadastrar Livros */
	
		$(btn.save).click( function() {
			ManageLibrary.Functions.registerNewLibraryBook();
		});
		
		$("a[href=#tab1]").click(function(){
			ManageLibrary.Functions.cleanPageData();
		});
				
		/* Funcoes para a tab2: Emprestar Livros */
		
		$("#id_book1").change(function(){
			var book_id = $("#id_book1 option:selected").val();
			ManageLibrary.Functions.searchBookInfo(book_id, "_tab2");
		});
		
		$(btn.borrow).click( function() {
			ManageLibrary.Functions.borrowBook();
		});
		
		$("a[href=#tab2]").click(function(){
			ManageLibrary.Functions.cleanPageData();
		});
		
		/* Funcoes para a tab3: Receber Livros */
		
		$("#id_book2").change(function(){
			var book_id = $("#id_book2 option:selected").text();
			ManageLibrary.Functions.searchBookInfo(book_id, "_tab3");
		});
		
		$(btn.receive).click( function() {
			ManageLibrary.Functions.receiveBook();
		});
		
		$("a[href=#tab3]").click(function(){
			ManageLibrary.Functions.cleanPageData();
		});
		
		/* Funcoes para a tab4: Emprestimos */
		ManageLibrary.Functions.listLoans();
		
		$("a[href=#tab4]").click(function(){
		  ManageLibrary.Functions.searchLoansFn();
		});

	},

//----------------------------------------------------------------- registerNewLibraryBook	
	registerNewLibraryBook: function()
	{
		var $tab = $('#tab1'),
			$messageContainer = $tab.find("div.message_container"),
		    data = {};
		
		data['book'] = $("#id_book").val();
		
		$.ajax({
			url: "/gerenciarbiblioteca/cadastrarlivro/cadastrar/",
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
					if( (response['success_message']).length != 0 )
					{
						var $tab2 = $('#tab2'),
							combo2 = $tab2.find("#id_book1"),	
							$tab3 = $('#tab3'),
							combo3 = $tab3.find("#id_book2"),
							bookId = response['book_id'];
							
				        combo2.append('<option value="'+bookId+'">'+bookId+'</option>');
				        combo3.append('<option value="'+bookId+'">'+bookId+'</option>');
				        
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
	
//------------------------------------------------------------------------- searchBookInfo	
	searchBookInfo: function(book_id, tab)
	{
		var data = {},
			$tab = $('#tab2'),
			$messageContainer = $tab.find("div.message_container");
							
		data['book_id'] = book_id;		
		
		$.ajax({
			url: "/gerenciarbiblioteca/informacoes/livro/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				var books = [];
				$.each(response, function(i, item){
	                var book = {
	                	id: item.pk,
	                	name: item.fields['name'],
	                	author: item.fields['author'],
	                	spiritual_author: item.fields['spiritual_author'],
	                	publisher: item.fields['publisher'],
	                	situation: item.fields['situation'],
	                };
	                books[i] = book;
                });

				ManageLibrary.Functions.listBookInformationFn(books, tab);							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	},

//------------------------------------------------------------------------- borrowBook	
	borrowBook: function()
	{
		var data = {},
			$tab = $('#tab2'),
			$messageContainer = $tab.find("div.message_container");
							
		data['book1'] = $('#id_book1').val();	
		data['user_login1'] = $('#id_user_login1').val();	

		$.ajax({
			url: "/gerenciarbiblioteca/emprestarlivro/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {				
				ManageLibrary.Functions.showResultMessage($messageContainer, response);		
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	},

//------------------------------------------------------------------------- receiveBook	
	receiveBook: function()
	{
		var data = {},
			$tab = $('#tab3'),
			$messageContainer = $tab.find("div.message_container");
				
		data['book2'] = $('#id_book2').val();	
		data['user_login2'] = $('#id_user_login2').val();	
		
		$.ajax({
			url: "/gerenciarbiblioteca/receberlivro/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {				
				ManageLibrary.Functions.showResultMessage($messageContainer, response);					
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	},

//------------------------------------------------------------------------- showResultMessage	
	showResultMessage: function($messageContainer, response)
	{
		if(response['validation_message'] != "") {
			
			Helpers.Functions.showValidationMsg($messageContainer, 
												response['validation_message']);
		}	
		
		else {	
			
			if(response['error_message'] != "")
			{
				ManageLibrary.Functions.cleanPageData();
				Helpers.Functions.showSuccessMsg($messageContainer, 
												 response['error_message']);
			}	
			if(response['success_message'] != "")
			{
				ManageLibrary.Functions.cleanPageData();
				Helpers.Functions.showSuccessMsg($messageContainer, 
											     response['success_message']);
			}	
				
		}			
	},

//------------------------------------------------------------------------- listBookInformationFn
	listBookInformationFn: function(books, tab)
	{
		if (books.length == 0)
		{
			$("#content_name" + tab).html("");
			$("#content_author" + tab).html("");
			$("#content_sauthor" + tab).html("");
			$("#content_publisher" + tab).html("");
			$("#content_situation" + tab).html("");
		}
		else
		{
			$("#content_name" + tab).html(books[0].name);
			$("#content_author" + tab).html(books[0].author);
			$("#content_sauthor" + tab).html(books[0].spiritual_author);
			$("#content_publisher" + tab).html(books[0].publisher);
			$("#content_situation" + tab).html(books[0].situation);		
		}

	},

//------------------------------------------------------------------------- listLoans
	listLoans: function()
	{	
		var table = ManageLibrary.Selectors.Tables,	
			grid = $(table.loans),
			columnsTitles = ['Código<br />Livro', 'Nome do Livro', 'Data de<br />Empréstimo', 
							'Data para<br />Devolução', 'Data de<br />Devolução',
							'Nome  do Usuário'],
			columnsSpecification = [
			{name:'id', index:'id', width:40},
	        {name:'book_name', index:'book_name', width:230},	
	        {name:'loan_date', index:'loan_date', width:70},
	        {name:'expected_return_date', index:'expected_return_date', width:70},
	        {name:'return_date', index:'return_date', width:70},
	        {name:'user_name', index:'user_name', width:230}
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#bloans',
		    multiselect: true,
		    sortname: 'name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Histórico de empréstimos'				
		});
	},

//------------------------------------------------------------------------- searchLoansFn	
	searchLoansFn: function(tab)
	{
		var table = ManageLibrary.Selectors.Tables,	
			grid = $(table.loans),
			$tab = $('#tab4'),
			$messageContainer = $tab.find("div.message_container");
				
		$.ajax({
			url: "/gerenciarbiblioteca/livrosemprestados/listar/",
			dataType: "json",
			data: {},
			async: true,
			success: function(response) {
				var loans = [];
				$.each(response, function(i, item){
	                var loan = {
	                	id: item.pk,
	                	book_name: item.fields['book_name'],
	                	loan_date: item.fields['loan_date'],
	                	expected_return_date: item.fields['expected_return_date'],
	                	return_date: item.fields['return_date'],	                	
	                	user_name: item.fields['user_name']
	                }
	                loans[i] = loan;
                });

				ManageLibrary.Functions.listFn(loans, grid);							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);			
			}
		});		
	},
	
//------------------------------------------------------------------------- listFn	
	listFn: function(data, grid)
	{		
		grid.clearGridData();
		
		for(var i=0;i<data.length;i++)
        {
            grid.jqGrid('addRowData', i, data[i]);
        }
		
	},
	
//------------------------------------------------------------------------- cleanPageData	
	cleanPageData: function()
	{
		/* Dados da tab1 */
		$('#id_book').val("");	
		
		/* Dados da tab2 */
		$('#id_book1').val("");	
		$('#id_user_login1').val("");	
		
		$("#content_name_tab2").html("");
		$("#content_author_tab2").html("");
		$("#content_sauthor_tab2").html("");
		$("#content_publisher_tab2").html("");
		$("#content_situation_tab2").html("");

		/* Dados da tab3 */
		$('#id_book2').val("");	
		$('#id_user_login2').val("");
		
		$("#content_name_tab3").html("");
		$("#content_author_tab3").html("");
		$("#content_sauthor_tab3").html("");
		$("#content_publisher_tab3").html("");
		$("#content_situation_tab3").html("");	

	},

}	