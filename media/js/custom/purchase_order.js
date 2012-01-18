var PurchaseOrder = {};

//------------------------------------------------------------------------------ SELECTORS

PurchaseOrder.Selectors = {
	
	Buttons: {
		add: "#button_add_book",
		accept: "#button_accept_book",
		remove: "#button_remove_item"
	},
	
	Tables: {
		orders: "#table_orders",
		purchaseItems: "#table_purchase_items"
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

PurchaseOrder.Functions = {

//------------------------------------------------------------------------- init	
	init: function() {
		
		var btn = PurchaseOrder.Selectors.Buttons;
								
		/* Funcoes para a tab1: Novo Pedido de Compra */
		
		PurchaseOrder.Functions.createOrdersTable();
		PurchaseOrder.Functions.createPurchaseItemsTable();
		
		$(btn.add).click(PurchaseOrder.Functions.addBookToPurchaseOrder);
		$(btn.accept).click(PurchaseOrder.Functions.addBookOrderToPurchaseOrder);
		$(btn.remove).click(PurchaseOrder.Functions.removeItemFromPurchaseOrder);
	},

//------------------------------------------------------------------------- createOrdersTable
	createOrdersTable: function() {
			
		
	},
	
//------------------------------------------------------------------------- createPurchaseItemsTable
	createPurchaseItemsTable: function() {
			
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
		    caption:'Itens do Pedido de Compra',
		    userdata: {
				purchaseItems: []
			}			
		});
	},
	
//-------------------------------------------------------------------------- addBookToPurchaseOrder
	addBookToPurchaseOrder: function(event) {
		
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
		
		PurchaseOrder.Functions._addItemToPurchaseOrder(book, quantity);
	},
	
//--------------------------------------------------------------------- addBookOrderToPurchaseOrder
	addBookOrderToPurchaseOrder: function(event) {
		
		// 'quantity' veio da grid
		var quantity = 3;
		
		// 'book' veio da grid
		var book = {
			"id": 3,
			"name": "Livro legal",
			"author": "Alex",
			"spiritualAuthor": "Carol",
			"publisher": "A Editora"
		};
		
		// 'orderId' veio da grid
		var bookOrderId = 20;
		
		PurchaseOrder.Functions._addItemToPurchaseOrder(book, quantity, bookOrderId);
	},
	
//-------------------------------------------------------------------------- addItemToPurchaseOrder
	_addItemToPurchaseOrder: function(book, quantity, bookOrderId) {
			
		var $grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		
			purchaseItemRow = {
				bookId: book.id,
				bookName: book.name,
				author: book.author,
				spiritualAuthor: book.spiritualAuthor,
				publisher: book.publisher,
				quantity: quantity
			},
			
			purchaseItem = {
				bookId: book.id,
				bookOrdersIds: [],
				quantity: quantity
			},
			
			userData = $grid.jqGrid("getGridParam", "userdata"),
			purchaseItems = userData.purchaseItems,
			
			rowData = $grid.jqGrid("getRowData", purchaseItemRow.bookId);
			
		
		if (jQuery.isEmptyObject(rowData)) {
			
			// Adiciona o item ao modelo
			if (typeof bookOrderId !== "undefined") {
				purchaseItem.bookOrdersIds.push(bookOrderId);
			}
			
			purchaseItems.push(purchaseItem);
		
			// Adiciona o item à visualização
			$grid.jqGrid("addRowData", purchaseItemRow.bookId, purchaseItemRow, "first");
			             
		} else {
			
			var existingItem = 
					PurchaseOrder.Functions._findPurchaseItemByBookId(purchaseItems,
			                                                          purchaseItem.bookId).item,
                newQuantity = (+rowData.quantity) + (+quantity);
		
			// Atualiza o item do modelo
			if (existingItem) {
				existingItem.quantity = newQuantity;
				
				if (typeof bookOrderId !== "undefined") {
					existingItem.bookOrdersIds.push(bookOrderId);
				}
			}
		
			// Atualiza o item da visualização
			$grid.jqGrid("setRowData", purchaseItemRow.bookId, { "quantity": newQuantity });
		}
	},
	
//--------------------------------------------------------------------- removeItemFromPurchaseOrder
	removeItemFromPurchaseOrder: function(event) {
		
		var $grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		
			userData = $grid.jqGrid("getGridParam", "userdata"),
			purchaseItems = userData.purchaseItems,
			
			// Faz uma cópia, pra não "confundir" o loop
			selectedIds = $grid.jqGrid("getGridParam", "selarrrow").slice();
		
		
		for (var i = 0; i < selectedIds.length; i++) {
			
			var selectedId = selectedIds[i],
			    index = PurchaseOrder.Functions._findPurchaseItemByBookId(purchaseItems,
			                                                              selectedId).index;
			
			// Remove o item do modelo                                                             
			purchaseItems.splice(index, 1);
			
			// Remove o item da visualização			
			$grid.jqGrid("delRowData", selectedId);
		}
		
	},	
		
//------------------------------------------------------------------------ findPurchaseItemByBookId
	
	_findPurchaseItemByBookId: function(purchaseItems, bookId) {
	
		for (var i = 0; i < purchaseItems.length; i++) {
			if (purchaseItems[i].bookId == bookId) {
				return { index: i, item: purchaseItems[i] };
			}
		}
	},	
		
//------------------------------------------------------------------------- listFn	
	listFn: function(data, grid)
	{		
		grid.clearGridData();
		
		for(var i = 0; i < data.length; i++)
        {
            grid.jqGrid('addRowData', i, data[i]);
        }
		
	}
}