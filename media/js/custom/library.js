var Library = {};

//------------------------------------------------------------------------------ SELECTORS

Library.Selectors = {
	
	Buttons: {
		search: '#button_search'
	},
	
	Tables: {
		books: '#table_books',
		loans: '#table_user_loans'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

Library.Functions = {

//------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = Library.Selectors.Buttons;
		
		/* Funcoes para a tab1: Cadastro */

		
		/* Funcoes para a tab2: Procurar Livros */
		
		Library.Functions.listBooks();
		
		$(btn.search).click( function() {
			Library.Functions.searchBooksFn();
		});	
		
		/* Funcoes para a tab3: Emprestimos do usuario */
		Library.Functions.listUserLoans();
		
		$("a[href=#tab3]").click(function(){
		  Library.Functions.searchLoansFn();
		});

	},

//------------------------------------------------------------------------- listBooks
	listBooks: function()
	{	
		var table = Library.Selectors.Tables;	
		var grid = $(table.books);
		var columnsTitles = ['Código', 'Nome','Autor(es)', 'Autor(es) Espiritual(ais)', 
								'Editora', 'Situação'];
		var columnsSpecification = [
			{name:'id', index:'id', width:42},
	        {name:'name', index:'name', width:200},
	        {name:'author', index:'author', width:130},
	        {name:'spiritual_author', index:'author', width:145},
	        {name:'publisher', index:'publisher', width:145}, 	
	        {name:'situation', index:'situation', width:80},	
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#bbooks',
		    multiselect: false,
		    sortname: 'name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de livros cadastrados da Biblioteca'				
		});
	},

//------------------------------------------------------------------------- searchBooksFn	
	searchBooksFn: function(tab)
{
		var table = Library.Selectors.Tables;
		var grid = $(table.books);
		var divMsg = $("#msg_tab2");
		var divId =	"msg_tab2";		
		var data = {};
		
		data['name'] = $('#name').val().trim();
		data['author'] = $('#author').val().trim();
		data['publisher'] = $('#publisher').val().trim();		
			
		$.ajax({
			url: "/biblioteca/pesquisarlivros/",
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
	                	situation: item.fields['situation']
	                }
	                books[i] = book;
                });

				Library.Functions.listFn(books, grid);							
			},
			error: function() {	
				msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
			}
		});		
	},


//------------------------------------------------------------------------- listUserLoans
	listUserLoans: function()
	{	
		var table = Library.Selectors.Tables;	
		var grid = $(table.loans);
		var columnsTitles = ['Código<br />Livro', 'Nome do Livro','Autor(es)', 'Autor(es) Espiritual(ais)', 
							'Data de<br />Empréstimo', 'Data para<br />Devolução', 
							'Data de<br />Devolução'];
		var columnsSpecification = [
			{name:'id', index:'id', width:40},
	        {name:'name', index:'name', width:220},
	        {name:'author', index:'author', width:135},
	        {name:'spiritual_author', index:'author', width:135},	
	        {name:'loan_date', index:'loan_date', width:65},
	        {name:'expected_return_date', index:'expected_return_date', width:60},
	        {name:'return_date', index:'return_date', width:60}		
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
		var table = Library.Selectors.Tables;	
		var grid = $(table.loans);
		var divMsg = $('#msg_tab3');
		var divId = "msg_tab3";
		var msg = Helpers.Messages.Library.ERROR_LOADING_LOANS;
				
		$.ajax({
			url: "/biblioteca/meusemprestimos/listar/",
			dataType: "json",
			data: {},
			async: true,
			success: function(response) {
				var loans = [];
				$.each(response, function(i, item){
	                var loan = {
	                	id: item.pk,
	                	name: item.fields['name'],
	                	author: item.fields['author'],
	                	spiritual_author: item.fields['spiritual_author'],
	                	loan_date: item.fields['loan_date'],
	                	expected_return_date: item.fields['expected_return_date'],
	                	return_date: item.fields['return_date']
	                }
	                loans[i] = loan;
                });

				Library.Functions.listFn(loans, grid);							
			},
			error: function() {	
				msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
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
		
	}
}	