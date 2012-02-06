var Bookstore = {};

//------------------------------------------------------------------------------ SELECTORS

Bookstore.Selectors = {
	
	Buttons: {
		search: '#button_search',
		add: '#button_add',
		cancel: '#button_cancel',
	},
	
	Tables: {
		orders: '#table_orders',
		userOrders: '#table_user_orders'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

Bookstore.Functions = {

//------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = Bookstore.Selectors.Buttons;
			
		/* Funcoes para a tab1: Encomendas de Livros */
		Bookstore.Functions.listBooksOrdersTab();
		
		$(btn.search).click( function() {
			Bookstore.Functions.searchBooksFn();
		});	
		
		$(btn.add).click( function() {
			var grid = $(Bookstore.Selectors.Tables.orders);
			Bookstore.Functions.getSelectedRowFn(grid, $("#tab1"));	
		});
		
		/* Funcoes para a tab2: Encomendas do usuario */
		Bookstore.Functions.listUserOrdersTab();
		
		$("a[href=#tab2]").click(function(){
		  Bookstore.Functions.searchOrdersFn();
		});
					
		$(btn.cancel).click( function() {
			var grid = $(Bookstore.Selectors.Tables.userOrders);
			Bookstore.Functions.getSelectedRowFn(grid, $("#tab2"));	
		});

	},
	


//------------------------------------------------------------------------- listBooksOrdersTab
	listBooksOrdersTab: function()
	{	
		var table = Bookstore.Selectors.Tables,	
			grid = $(table.orders),
			columnsTitles = ['Id', 'Nome do Livro','Autor(es)', 'Autor(es) Espiritual(ais)', 
							 'Editora', 'Qtd na Livraria'],
			columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'name', index:'name', width:220},
	        {name:'author', index:'author', width:140},
	        {name:'spiritual_author', index:'author', width:140},
	        {name:'publisher', index:'publisher', width:160}, 	
	        {name:'available_quantity', index:'available_quantity', width:80}	
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#borders',
		    multiselect: false,
		    sortname: 'name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de livros cadastrados na Livraria'				
		});
	},

//------------------------------------------------------------------------- listUserOrdersTab
	listUserOrdersTab: function()
	{	
		var table = Bookstore.Selectors.Tables,	
			grid = $(table.userOrders),
			columnsTitles = ['Id', 'Nome do Livro','Autor(es)', 'Autor(es) Espiritual(ais)', 
							 'Data da Encomenda', 'Qtd', 'Situação'],
			columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'name', index:'name', width:220},
	        {name:'author', index:'author', width:140},
	        {name:'spiritual_author', index:'author', width:140},
	        {name:'order_date', index:'order_date', width:110}, 	
	        {name:'quantity', index:'quantity', width:40},
	        {name:'situation', index:'situation', width:90}	
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#bmyorders',
		    multiselect: false,
		    sortname: 'name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de encomendas'				
		});
	},	
//------------------------------------------------------------------------- searchBooksFn	
	searchBooksFn: function()
	{
		var table = Bookstore.Selectors.Tables,	
			grid = $(table.orders),
			$tab = $("#tab1"),
			$messageContainer = $tab.find("div.message_container"),
			data = {};
			
			data['name'] = $('#name').val().trim();
			data['author'] = $('#author').val().trim();
			data['publisher'] = $('#publisher').val().trim();					
		
		$.ajax({
			url: "/livraria/pesquisar/",
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
	                	available_quantity: item.fields['available_quantity']
	                }
	                books[i] = book;
                });

				Bookstore.Functions.listFn(books, grid);							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	},

//------------------------------------------------------------------------- searchOrdersFn	
	searchOrdersFn: function()
	{
		var grid = $(Bookstore.Selectors.Tables.userOrders),
			$tab = $("#tab2"),
			$messageContainer = $tab.find("div.message_container");
				
		$.ajax({
			url: "/livraria/encomendas/listar/",
			dataType: "json",
			data: {},
			async: true,
			success: function(response) {
				var orders = [];
				$.each(response, function(i, item){
	                var order = {
	                	id: item.pk,
	                	name: item.fields['name'],
	                	author: item.fields['author'],
	                	spiritual_author: item.fields['spiritual_author'],
	                	order_date: item.fields['order_date'],
	                	quantity: item.fields['quantity'],
	                	situation: item.fields['situation']
	                }
	                orders[i] = order;
                });

				Bookstore.Functions.listFn(orders, grid);							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
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


//------------------------------------------------------------------------- getSelectedRowFn		
	getSelectedRowFn: function(grid, $tab)
	{
		var selRowNumber = grid.getGridParam('selrow'),
			$messageContainer = $tab.find("div.message_container");
					
		if (selRowNumber == null)
		{
			var msg = "";
			
			if($tab.selector == "#tab1")
			{
				msg = Helpers.Messages.Book.NO_SEL_ARROW;
			}
			
			if($tab.selector == "#tab2")
			{
				msg = Helpers.Messages.Order.NO_SEL_ARROW;
			}

			Helpers.Functions.showWarningMsg($messageContainer, msg);
		}
		else
		{		
			var bookId = grid.getRowData(selRowNumber)['id'];
			
			if($tab.selector == "#tab1")
			{
				Bookstore.Functions.orderBook(bookId, $tab);
			}
			
			if($tab.selector == "#tab2")
			{
				Bookstore.Functions.cancelOrder(bookId, $tab);
			}
		}
	},
//------------------------------------------------------------------------- orderBook		
	orderBook: function(ids, $tab)
	{
		var data = {},	
			url = "/livraria/encomendarlivros/",
			grid = $(Bookstore.Selectors.Tables.orders),
			$messageContainer = $tab.find("div.message_container");
		
		data['book_ids'] = [ids];		
		data['quantity'] = $("#quantity").val().trim();
		
		$.ajax({
			traditional: true,
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {	

				if(response['validation_message'].length != 0)
				{
					Helpers.Functions.showValidationMsg($messageContainer, 
													 response['validation_message']);
				}
					
				if(response['error_message'] != "")
				{
					Helpers.Functions.showErrorMsg($messageContainer, 
													 response['error_message']);
				}	
								
				if(response['warning_message'] != "")
				{
					Helpers.Functions.showWarningMsg($messageContainer, 
													 response['warning_message']);
				}	
				
				if(response['success_message'] != "")
				{
					$("#quantity").val("");
					grid.resetSelection();
					Helpers.Functions.showSuccessMsg($messageContainer, 
													response['success_message']);
				}	
		
			},
			error: function() {	
				var msg = Helpers.Messages.Book.ERROR_SAVING_BOOK;
				Helpers.Functions.showErrorMsg($messageContainer, msg);
			}
		});	
	},
	
//------------------------------------------------------------------------- cancelOrder		
	cancelOrder: function(ids, $tab)
	{
		var data = {},	
			url = "",
			grid = $(Bookstore.Selectors.Tables.userOrders),
			$messageContainer = $tab.find("div.message_container");
		
		data['order_ids'] = [ids];
		
		$.ajax({
			traditional: true,
			url: "/livraria/encomendas/cancelar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {	
				if(response['success_message'] != "")
				{
					var selRowNumber = grid.getGridParam('selrow');
					var rowData = grid.getRowData(selRowNumber);					
					grid.jqGrid('setRowData', selRowNumber, {situation:'Cancelada'});
					
					grid.resetSelection();
					Helpers.Functions.showSuccessMsg($messageContainer, 
													 response['success_message']);
				}	
				
				if(response['error_message'] != "")
				{
					Helpers.Functions.showErrorMsg($messageContainer, 
													 response['error_message']);
				}			
			},
			error: function() {	
				var msg = Helpers.Messages.Order.ERROR_CANCELING_ORDER;
				Helpers.Functions.showErrorMsg($messageContainer, msg);	
			}
		});	
	}
}	