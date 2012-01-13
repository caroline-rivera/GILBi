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
		
		// TO DO: PROCURAR SE EU POSSO PEGAR O ID
		
		$("#id_book").change(function(){
			book_name = $("#id_book option:selected").text();
			//SellBooks.Functions.searchBookInfo(book_name);
		});
			
		$(btn.sell_tab1).click( function() {
			//divMsg = $('#msg_tab1');
			//SellBooks.Functions.sellBooks(divMsg, "msg_tab1");	
		});
				
		/* Funcoes para a tab2: Venda de encomendas do usuario */
		
		SellBooks.Functions.listUserOrders();
		
		$(btn.search_tab2).click( function() {
			SellBooks.Functions.searchOrdersFn();
		});			
					
		$(btn.sell_tab2).click( function() {
			SellBooks.Functions.sellOrder();
			//grid = $(SellBooks.Selectors.Tables.orders);
			//divMsg = $('#msg_tab2');
			//SellBooks.Functions.getSelectedRowFn(grid, divMsg, "msg_tab2");	
		});

	},
	
//------------------------------------------------------------------------- listUserOrders
	listUserOrders: function()
	{	
		var table = SellBooks.Selectors.Tables;	
		var grid = $(table.orders);
		var columnsTitles = ['Id', 'Data/Hora','Nome','Autor(es)', 'Autor(es) Espiritual(ais)', 
								'Qtd', 'Situação'];
		var columnsSpecification = [
			{name:'id', index:'id', hidden:true},
			{name:'order_date', index:'order_date', width:100},
	        {name:'name', index:'name', width:230},
	        {name:'author', index:'author', width:135},
	        {name:'spiritual_author', index:'author', width:135},
	        {name:'quantity', index:'quantity', width:35},
	        {name:'situation', index:'situation', width:75}, 		
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
		var table = SellBooks.Selectors.Tables;	
		var grid = $(table.orders);
		var divMsg = $("#msg_tab2");
		var divId =	"msg_tab2";	
		var data = {};
				
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
	                }
	                orders[i] = order;
                });

				SellBooks.Functions.listFn(orders, grid);							
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
			bookId = grid.getRowData(selRowNumber)['id'];
			return bookId;
		}
	},
//------------------------------------------------------------------------- sellOrder		
	sellOrder: function()
	{
		var table = SellBooks.Selectors.Tables;	
		var grid = $(table.orders);
		var data = {};
		var url = "/vendas/encomendas/venderencomenda/";

		id_selected_order = SellBooks.Functions.getSelectedRowFn(grid);

		data['order_id'] = [id_selected_order];		
		data['order_price'] = $("#order_price").val();

		$.ajax({
			traditional: true,
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {	
				if(response['validation_message'] != "")
				{
					Helpers.Functions.showValidationMsg("div_validation", response['validation_message']);
				}
				if (response['error_message'] != "")
				{
					Helpers.Functions.showErrorMsg("div_error", response['error_message']);
				}		
				if (response['success_message'] != "")
				{
					alert(response['success_message']);
					$("#order_price").val("");
					grid.resetSelection(); //deletar a linha
					Helpers.Functions.showSuccessMsg("div_success", response['success_message']);
				}				
			},
			error: function() {	
				msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg(divId, msg);		
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
					grid.getRowData(selRowNumber)['situation'].val('Cancelada');
					grid.resetSelection();
					//Bookstore.Functions.searchOrdersFn();
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
				msg = Helpers.Messages.Order.ERROR_CANCELING_ORDER;
				Helpers.Functions.showPopUpErrorMsg(divMsg, divId, msg);		
			}
		});	
	}
}	