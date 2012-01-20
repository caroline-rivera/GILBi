var Bookstore = {};

//------------------------------------------------------------------------------ SELECTORS

Bookstore.Selectors = {
	
	Buttons: {
		search_tab1: '#button_search_tab1',
		search_tab2: '#button_search_tab2',
		add_tab1: '#button_add_tab1',
		add_tab2: '#button_add_tab2',
		cancel_tab3: '#button_cancel_tab3',
	},
	
	Tables: {
		favorites: '#table_favorites',
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
		
		/* Funcoes para a tab1: Livros favoritos */
		Bookstore.Functions.listBooksFavoritesTab();
		
		$(btn.search_tab1).click( function() {
			Bookstore.Functions.searchBooksFn("1");
		});	
		
		$(btn.add_tab1).click( function() {
			grid = $(Bookstore.Selectors.Tables.favorites);
			divMsg = $('#msg_tab1');
			Bookstore.Functions.getSelectedColumnsFn(grid, divMsg, "msg_tab1");	
		});
		
		/* Funcoes para a tab2: Encomendas de Livros */
		Bookstore.Functions.listBooksOrdersTab();
		
		$(btn.search_tab2).click( function() {
			Bookstore.Functions.searchBooksFn("2");
		});	
		
		$(btn.add_tab2).click( function() {
			grid = $(Bookstore.Selectors.Tables.orders);
			divMsg = $('#msg_tab2');
			Bookstore.Functions.getSelectedRowFn(grid, divMsg, "msg_tab2");	
		});
		
		/* Funcoes para a tab3: Encomendas do usuario */
		Bookstore.Functions.listUserOrdersTab();
		
		$("a[href=#tab3]").click(function(){
		  Bookstore.Functions.searchOrdersFn();
		});
					
		$(btn.cancel_tab3).click( function() {
			grid = $(Bookstore.Selectors.Tables.userOrders);
			divMsg = $('#msg_tab3');
			Bookstore.Functions.getSelectedRowFn(grid, divMsg, "msg_tab3");	
		});

	},
	
//------------------------------------------------------------------------- listBooksFavoritesTab
	listBooksFavoritesTab: function()
	{	
		var table = Bookstore.Selectors.Tables;	
		var grid = $(table.favorites);
		var columnsTitles = ['Id', 'Nome','Autor(es)', 'Autor(es) Espiritual(ais)', 'Editora'];
		var columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'name', index:'name', width:260},
	        {name:'author', index:'author', width:150},
	        {name:'spiritual_author', index:'author', width:150},
	        {name:'publisher', index:'publisher', width:160} 		
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#bfavorites',
		    multiselect: true,
		    sortname: 'name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de livros cadastrados na Livraria'				
		});
	},

//------------------------------------------------------------------------- listBooksOrdersTab
	listBooksOrdersTab: function()
	{	
		var table = Bookstore.Selectors.Tables;	
		var grid = $(table.orders);
		var columnsTitles = ['Id', 'Nome','Autor(es)', 'Autor(es) Espiritual(ais)', 
							 'Editora', 'Qtd na Livraria'];
		var columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'name', index:'name', width:220},
	        {name:'author', index:'author', width:140},
	        {name:'spiritual_author', index:'author', width:140},
	        {name:'publisher', index:'publisher', width:160}, 	
	        {name:'avaiable_quantity', index:'avaiable_quantity', width:80}	
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
		var table = Bookstore.Selectors.Tables;	
		var grid = $(table.userOrders);
		var columnsTitles = ['Id', 'Nome','Autor', 'Autor Espiritual', 
							 'Data', 'Qtd', 'Situação'];
		var columnsSpecification = [
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
	searchBooksFn: function(tab)
	{
		var table = Bookstore.Selectors.Tables;	
		var data = {};
		
		if(tab == "1")
		{
			var grid = $(table.favorites);
			data['name'] = $('#name_tab1').val().trim();
			data['author'] = $('#author_tab1').val().trim();
			data['publisher'] = $('#publisher_tab1').val().trim();		
			divMsg = $("#msg_tab1");
			divId =	"msg_tab1";
		}
		
		if(tab == "2")
		{
			var grid = $(table.orders);
			data['name'] = $('#name_tab2').val().trim();
			data['author'] = $('#author_tab2').val().trim();
			data['publisher'] = $('#publisher_tab2').val().trim();	
			divMsg = $("#msg_tab2");
			divId =	"msg_tab2";		
		}
		
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
	                	avaiable_quantity: item.fields['avaiable_quantity']
	                }
	                books[i] = book;
                });

				Bookstore.Functions.listFn(books, grid);							
			},
			error: function() {	
				msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
			}
		});		
	},

//------------------------------------------------------------------------- searchOrdersFn	
	searchOrdersFn: function(tab)
	{
		var table = Bookstore.Selectors.Tables;	
		var grid = $(table.userOrders);
		var divMsg = $('#msg_tab3');
		var divId = "msg_tab3";
				
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
		
	},	

//------------------------------------------------------------------------- getSelectedColumnsFn		
	getSelectedColumnsFn: function(grid, divMsg, divId)
	{
		var selArrowNumerations = grid.getGridParam('selarrrow');
		var bookIds = [];
		
		for (var i = 0; i < selArrowNumerations.length; i++)
		{
			numeration = selArrowNumerations[i]
			bookIds[i] = grid.getRowData(numeration)['id'];
		}
					
		if (bookIds.length == 0)
		{
			msg = Helpers.Messages.Book.NO_SEL_ARROW;
			Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);
		}
		else
		{		
			Bookstore.Functions.saveFn(bookIds, divMsg, divId);
		}
	},

//------------------------------------------------------------------------- getSelectedRowFn		
	getSelectedRowFn: function(grid, divMsg, divId)
	{
		var selRowNumber = grid.getGridParam('selrow');
					
		if (selRowNumber == null)
		{
			msg = Helpers.Messages.Book.NO_SEL_ARROW;
			Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);
		}
		else
		{		
			bookId = grid.getRowData(selRowNumber)['id'];
			
			if(divId == "msg_tab2")
			{
				Bookstore.Functions.saveFn(bookId, divMsg, divId);
			}
			
			if(divId == "msg_tab3")
			{
				Bookstore.Functions.cancelFn(bookId, divMsg, divId);
			}
		}
	},
//------------------------------------------------------------------------- saveFn		
	saveFn: function(ids, divMsg, divId)
	{
		var data = {};	
		var url = "";
		var grid = $(Bookstore.Selectors.Tables.favorites);
		
		data['book_ids'] = [ids];
		
		if(divId == "msg_tab1")
		{
			url = "/livraria/adicionarfavoritos/";
		}
		else
		{
			data['quantity'] = $("#quantity").val().trim();
			url = "/livraria/encomendarlivros/";	
			grid = $(Bookstore.Selectors.Tables.orders);
		}
		
		$.ajax({
			traditional: true,
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {			
				if(response['success_message'] != "")
				{
					$("#quantity").val("");
					grid.resetSelection();
					Helpers.Functions.showPopUpSuccessMsg(divMsg, 
														  divId, 
														  response['success_message']);
				}	
				
				if(response['error_message'] != "")
				{
					Helpers.Functions.showPopUpErrorMsg(divMsg, 
														divId, 
														response['error_message']);
				}			
			},
			error: function() {	
				msg = Helpers.Messages.Book.ERROR_SAVING_BOOK;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
			}
		});	
	},
	
//------------------------------------------------------------------------- cancelFn		
	cancelFn: function(ids, divMsg, divId)
	{
		var data = {};	
		var url = "";
		var grid = $(Bookstore.Selectors.Tables.userOrders);
		
		data['order_ids'] = [ids];
		
		$.ajax({
			traditional: true,
			url: "/livraria/encomendas/cancelar",
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
					Helpers.Functions.showPopUpSuccessMsg(divMsg, 
														  divId, 
														  response['success_message']);
					//Bookstore.Functions.searchOrdersFn();	
				}	
				
				if(response['error_message'] != "")
				{
					Helpers.Functions.showPopUpErrorMsg(divMsg, 
														divId, 
														response['error_message']);
				}			
			},
			error: function() {	
				msg = Helpers.Messages.Order.ERROR_CANCELING_ORDER;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
			}
		});	
	}
}	