var SellBooks = {};

//------------------------------------------------------------------------------ SELECTORS

SellBooks.Selectors = {
	
	Buttons: {
		sell_tab1: '#button_sell_tab1',
		sell_tab2: '#button_sell_tab2',
		search_tab2: '#button_search_tab2'
	},
	
	Tables: {
		orders: '#table_orders'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

SellBooks.Functions = {

//------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = SellBooks.Selectors.Buttons;
		
		/* Funcoes para a tab1: Venda de livros da prateleira */	
			
		$("#id_book").change(function(){
			var book_id = $("#id_book option:selected").val();
			SellBooks.Functions.searchBookInfo(book_id);
		});		
		
		$(btn.sell_tab1).click( function() {
			var divMsg = $('#msg_tab1');
			SellBooks.Functions.sellShelfBook();	
		});
		
		$("a[href=#tab1]").click(function(){
			SellBooks.Functions.cleanPageData();
		});
						
		/* Funcoes para a tab2: Venda de encomendas do usuario */
		
		SellBooks.Functions.listUserOrders();
		
		$(btn.search_tab2).click( function() {
			SellBooks.Functions.searchOrdersFn();
		});			
					
		$(btn.sell_tab2).click( function() {
			SellBooks.Functions.sellOrder();
		});
		
		$("a[href=#tab2]").click(function(){
			SellBooks.Functions.cleanPageData();
		});
	},

//------------------------------------------------------------------------- searchBookInfo	
	searchBookInfo: function(book_id)
	{
		var data = {},
			$tab = $("#tab1"),
			$messageContainer = $tab.find("div.message_container");
			
		data['book_id'] = book_id;		
		
		$.ajax({
			url: "/vendas/prateleira/informacoes/livro/",
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
	                	available_quantity: item.fields['available_quantity'],
	                	reserved_quantity: item.fields['reserved_quantity'],
	                };
	                books[i] = book;
                });

				SellBooks.Functions.listBookInformationFn(books);							
			},
			error: function() {	
				var msg = Helpers.Messages.ManageLibrary.ERROR_LOADING_BOOK_INFORMATION;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	},
//------------------------------------------------------------------------- listBookInformationFn
	listBookInformationFn: function(books)
	{
		var contentName = "", 
	        contentAuthor = "", 
	        contentSpiritualAuthor = "", 
	        contentPublisher = "",
			contentAvailableQty = "", 
			contentReservedQty = "";
			
		if (books.length != 0)
		{
			contentName = books[0].name; 
			contentAuthor = books[0].author;
			contentSpiritualAuthor = books[0].spiritual_author; 
			contentPublisher = books[0].publisher;
			contentAvailableQty = books[0].available_quantity; 
			contentReservedQty = books[0].reserved_quantity;
		}

		$("#content_name").html(contentName);
		$("#content_author").html(contentAuthor);
		$("#content_sauthor").html(contentSpiritualAuthor);
		$("#content_publisher").html(contentPublisher);
		$("#content_available_quantity").html(contentAvailableQty);	
		$("#content_reserved_quantity").html(contentReservedQty);	
	},		
	
//------------------------------------------------------------------------- sellShelfBook		
	sellShelfBook: function()
	{
		var data = {},
		    url = "/vendas/prateleira/venderlivro/",
			$tab = $("#tab1"),
			$messageContainer = $tab.find("div.message_container");

		data['book_id'] = $("#id_book option:selected").val();		
		data['book_price'] = $("#id_book_price").val();

		$.ajax({
			traditional: true,
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				    	
				if((response['validation_message']).length != 0)
				{
					Helpers.Functions.showValidationMsg($messageContainer, response['validation_message']);
				}
				if (response['error_message'] != "")
				{
					Helpers.Functions.showErrorMsg($messageContainer, response['error_message']);
				}		
				if (response['success_message'] != "")
				{
					SellBooks.Functions.cleanPageData();
					
					Helpers.Functions.showSuccessMsg($messageContainer, response['success_message']);
				}				
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});	
	},
//------------------------------------------------------------------------- listUserOrders
	listUserOrders: function()
	{	
		var grid = $(SellBooks.Selectors.Tables.orders),
		    columnsTitles = ['Id', 'Data/Hora','Nome','Autor(es)', 
		                     'Autor(es) Espiritual(ais)','Qtd', 'Situação'],
			columnsSpecification = [
				{name:'id', index:'id', hidden:true},
				{name:'order_date', index:'order_date', width:100},
		        {name:'name', index:'name', width:230},
		        {name:'author', index:'author', width:135},
		        {name:'spiritual_author', index:'author', width:135},
		        {name:'quantity', index:'quantity', width:35},
		        {name:'situation', index:'situation', width:75} 		
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#borders',
		    multiselect: false,
		    sortname: 'date',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de encomendas do usuário disponíveis para compra'				
		});
	},
	
//------------------------------------------------------------------------- searchOrdersFn	
	searchOrdersFn: function(tab)
	{
		var grid = $(SellBooks.Selectors.Tables.orders),
			$tab = $("#tab2"),
			$messageContainer = $tab.find("div.message_container"),
		    data = {};
				
		data['login'] = $('#login').val();
		data['email'] = $('#email').val();

		$.ajax({
			url: "/vendas/encomendas/procurarencomenda/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				var orders = [];
				$.each(response, function(i, item){
	                var order = {
	                	id: item.pk,
	                	order_date: item.fields['order_date'],
	                	name: item.fields['name'],
	                	author: item.fields['author'],
	                	spiritual_author: item.fields['spiritual_author'],
	                	quantity: item.fields['quantity'],
	                	situation: item.fields['situation']
	                };
	                orders[i] = order;
                });

				SellBooks.Functions.listFn(orders, grid);							
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
		
		for(var i = 0; i < data.length; i++)
        {
            grid.jqGrid('addRowData', i, data[i]);
        }
		
	},	

//------------------------------------------------------------------------- getSelectedRowFn		
	getSelectedRowFn: function(grid)
	{
		var selRowNumber = grid.getGridParam('selrow');
					
		if (selRowNumber == null)
		{
			return '';
		}
		else
		{		
			var bookId = grid.getRowData(selRowNumber)['id'];
			return bookId;
		}
	},
//------------------------------------------------------------------------- sellOrder		
	sellOrder: function()
	{
		var grid = $(SellBooks.Selectors.Tables.orders),
		    data = {},
		    url = "/vendas/encomendas/venderencomenda/",
		    id_selected_order = SellBooks.Functions.getSelectedRowFn(grid),
			$tab = $("#tab2"),
			$messageContainer = $tab.find("div.message_container");

		data['order_id'] = [id_selected_order];		
		data['order_price'] = $("#order_price").val();

		$.ajax({
			traditional: true,
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				    	
				if((response['validation_message']).length != 0)
				{
					Helpers.Functions.showValidationMsg($messageContainer, response['validation_message']);
				}
				if (response['error_message'] != "")
				{
					Helpers.Functions.showErrorMsg($messageContainer, response['error_message']);
				}		
				if (response['success_message'] != "")
				{
					var row_id = grid.getGridParam('selrow');
					$("#order_price").val("");
					
					grid.delRowData(row_id);
					
					Helpers.Functions.showSuccessMsg($messageContainer, response['success_message']);
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
		var grid = $(SellBooks.Selectors.Tables.orders);
		
		/* Dados da tab1 */
		$('#id_book').val("");	
		$('#id_book_price').val("");	
		
		$("#content_name").html("");
		$("#content_author").html("");
		$("#content_sauthor").html("");
		$("#content_publisher").html("");
		$("#content_available_quantity").html("");	
		$("#content_reserved_quantity").html("");

		/* Dados da tab2 */
		$('#login').val("");	
		$('#email').val("");
		$('#order_price').val("");
		
		grid.clearGridData();

	},

}	