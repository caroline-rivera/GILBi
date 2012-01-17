var PurchaseOrder = {};

//------------------------------------------------------------------------------ SELECTORS

PurchaseOrder.Selectors = {
	
	Buttons: {
		add: '#button_add_book'
	},
	
	Tables: {
		orders: '#table_orders',
		purchaseItems: '#table_purchase_items'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

PurchaseOrder.Functions = {

//------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = PurchaseOrder.Selectors.Buttons;
								
		/* Funcoes para a tab1: Novo Pedido de Compra */
		
		PurchaseOrder.Functions.createOrdersTable();
		PurchaseOrder.Functions.createPurchaseItemsTable();
		
		var $grid = $(PurchaseOrder.Selectors.Tables.purchaseItems);
				
		$(btn.add).click( function() {
			//PurchaseOrder.Functions.searchOrdersFn();
			
			// 'quantity' eu peguei da tela
			var $quantity = $("#id_quantity"),
			    quantity = $quantity.val();
			
			// 'book' voltou do servidor
			var book = {
				"id": 1,
				"name": "Livro legal",
				"author": "Alex",
				"spiritualAuthor": "Carol",
				"publisher": "A Editora"
			};
			
			var purchaseItemRow = {
				"bookId": book.id,
				"bookName": book.name,
				"author": book.author,
				"spiritualAuthor": book.spiritualAuthor,
				"publisher": book.publisher,
				"quantity": quantity
			};
			
			var purchaseItem = {
				
				"bookId": book.id,
				"bookOrders": [],
				"quantity": quantity
			};

			var rowData = $grid.jqGrid("getRowData", purchaseItemRow.bookId);
			
			if (jQuery.isEmptyObject(rowData)) {
			
				$grid.jqGrid("addRowData", purchaseItemRow.bookId, purchaseItemRow, "first");
				             
			} else {
			
				$grid.jqGrid("setRowData",
				             purchaseItemRow.bookId,
				             { "quantity": (+rowData.quantity) + (+quantity) });
				
			}
				
		});		
	},

//------------------------------------------------------------------------- createOrdersTable
	createOrdersTable: function()
	{	
		
	},
	
//------------------------------------------------------------------------- createPurchaseItemsTable
	createPurchaseItemsTable: function()
	{	
		var grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		    columnsTitles = ['Livro', 'Autor(es)', 'Autor(es) Espiritual(ais)','Editora', 
		    			     'Quantidade'],
			columnsSpecification = [
		        {name:'bookName', index:'bookName', width:230},
		        {name:'author', index:'author', width:140},
		        {name:'spiritualAuthor', index:'spiritualAuthor', width:140},
		        {name:'publisher', index:'publisher', width:100}, 
		        {name:'quantity', index:'quantity', width:80}		
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    height: 'auto',
		    multiselect: true,
		    sortname: 'name',
		    viewrecords: true,
		    caption:'Itens do Pedido de Compra'				
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
	}
}	