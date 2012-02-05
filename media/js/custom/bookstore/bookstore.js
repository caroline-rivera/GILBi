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
			var grid = $(Bookstore.Selectors.Tables.favorites);
			var divMsg = $('#msg_tab1');
			Bookstore.Functions.getSelectedColumnsFn(grid, $("#tab1"));	
		});
		
		/* Funcoes para a tab2: Encomendas de Livros */
		Bookstore.Functions.listBooksOrdersTab();
		
		$(btn.search_tab2).click( function() {
			Bookstore.Functions.searchBooksFn("2");
		});	
		
		$(btn.add_tab2).click( function() {
			var grid = $(Bookstore.Selectors.Tables.orders);
			var divMsg = $('#msg_tab2');
			Bookstore.Functions.getSelectedRowFn(grid, $("#tab2"));	
		});
		
		/* Funcoes para a tab3: Encomendas do usuario */
		Bookstore.Functions.listUserOrdersTab();
		
		$("a[href=#tab3]").click(function(){
		  Bookstore.Functions.searchOrdersFn();
		});
					
		$(btn.cancel_tab3).click( function() {
			var grid = $(Bookstore.Selectors.Tables.userOrders);
			var divMsg = $('#msg_tab3');
			Bookstore.Functions.getSelectedRowFn(grid, $("#tab3"));	
		});

	},
	
//------------------------------------------------------------------------- listBooksFavoritesTab
	listBooksFavoritesTab: function()
	{	
		var table = Bookstore.Selectors.Tables,	
			grid = $(table.favorites),
			columnsTitles = ['Id', 'Nome do Livro','Autor(es)', 'Autor(es) Espiritual(ais)', 'Editora'],
			columnsSpecification = [
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
	searchBooksFn: function(tab)
	{
		var table = Bookstore.Selectors.Tables,	
			data = {};
		
		if(tab == "1")
		{
			var grid = $(table.favorites),
				$tab = $("#tab1"),
				$messageContainer = $tab.find("div.message_container");
				
			data['name'] = $('#name_tab1').val().trim();
			data['author'] = $('#author_tab1').val().trim();
			data['publisher'] = $('#publisher_tab1').val().trim();	
		}
		
		if(tab == "2")
		{
			var grid = $(table.orders),
				$tab = $("#tab2"),
				$messageContainer = $tab.find("div.message_container");
			
			data['name'] = $('#name_tab2').val().trim();
			data['author'] = $('#author_tab2').val().trim();
			data['publisher'] = $('#publisher_tab2').val().trim();					
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
	searchOrdersFn: function(tab)
	{
		var grid = $(Bookstore.Selectors.Tables.userOrders),
			$tab = $("#tab3"),
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

//------------------------------------------------------------------------- getSelectedColumnsFn		
	getSelectedColumnsFn: function(grid, $tab)
	{
		var $messageContainer = $tab.find("div.message_container");
			
		var selArrowNumerations = grid.getGridParam('selarrrow'),
			bookIds = [];
		
		for (var i = 0; i < selArrowNumerations.length; i++)
		{
			var numeration = selArrowNumerations[i]
			bookIds[i] = grid.getRowData(numeration)['id'];
		}
					
		if (bookIds.length == 0)
		{
			var msg = Helpers.Messages.Book.NO_SEL_ARROW;
			Helpers.Functions.showWarningMsg($messageContainer, msg);
		}
		else
		{		
			Bookstore.Functions.saveFn(bookIds, $tab);
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
			
			if($tab.selector == "#tab2")
			{
				msg = Helpers.Messages.Book.NO_SEL_ARROW;
			}
			
			if($tab.selector == "#tab3")
			{
				msg = Helpers.Messages.Order.NO_SEL_ARROW;
			}

			Helpers.Functions.showWarningMsg($messageContainer, msg);
		}
		else
		{		
			var bookId = grid.getRowData(selRowNumber)['id'];
			
			if($tab.selector == "#tab2")
			{
				Bookstore.Functions.saveFn(bookId, $tab);
			}
			
			if($tab.selector == "#tab3")
			{
				Bookstore.Functions.cancelFn(bookId, $tab);
			}
		}
	},
//------------------------------------------------------------------------- saveFn		
	saveFn: function(ids, $tab)
	{
		var data = {},	
			url = "",
			grid = $(Bookstore.Selectors.Tables.favorites),
			$messageContainer = $tab.find("div.message_container");
		
		data['book_ids'] = [ids];
		
		if($tab.selector == "#tab1")
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
					Helpers.Functions.showSuccessMsg($messageContainer, 
													response['success_message']);
				}	
				
				if(response['warning_message'] != "")
				{
					Helpers.Functions.showWarningMsg($messageContainer, 
													 response['warning_message']);
				}			
			},
			error: function() {	
				var msg = Helpers.Messages.Book.ERROR_SAVING_BOOK;
				Helpers.Functions.showErrorMsg($messageContainer, msg);
			}
		});	
	},
	
//------------------------------------------------------------------------- cancelFn		
	cancelFn: function(ids, $tab)
	{
		debugger;
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