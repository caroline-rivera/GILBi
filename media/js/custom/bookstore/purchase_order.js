var PurchaseOrder = {};

//------------------------------------------------------------------------------ SELECTORS

PurchaseOrder.Selectors = {
	
	Buttons: {
		add: "#button_add_book",
		accept: "#button_accept_book",
		reject: "#button_reject_book",
		remove: "#button_remove_item",
		save: "#button_save_purchase_order",
		conclude: "#button_conclude_purchase_order",
		exclude: "#button_exclude_purchase_order"
	},
	
	Tables: {
		orders: "#table_orders",
		purchaseItems: "#table_purchase_items",
		purchaseItemsView: "#table_purchase_items_view",
	},
	
	MessageContainers: {
		books: "#book_message_container",
		orders: "#order_message_container",
		purchaseOrder: "#purchase_order_message_container",
		purchaseOrderView: "#purchase_order_view_message_container"
	},
	
	Combos : {
		purchaseOrders: "#id_purchase_order"
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

PurchaseOrder.Functions = {

//------------------------------------------------------------------------- init	
	init: function() {
		
		var btn = PurchaseOrder.Selectors.Buttons;
			cbo = PurchaseOrder.Selectors.Combos;
								
		/* Funcoes para a tab1: Novo Pedido de Compra */
		
		PurchaseOrder.Functions.createOrdersTable();
		PurchaseOrder.Functions.createPurchaseItemsTable();
		
		$(btn.add).click(PurchaseOrder.Functions.addBookToPurchaseOrder);
		$(btn.accept).click(PurchaseOrder.Functions.addBookOrderToPurchaseOrder);
		$(btn.remove).click(PurchaseOrder.Functions.removeItemFromPurchaseOrder);
		$(btn.reject).click(PurchaseOrder.Functions.rejectBookOrder);
		$(btn.save).click(PurchaseOrder.Functions.savePurchaseOrder);
		
		/* Funcoes para a tab 2: Visualizar Pedido de Compra*/
		PurchaseOrder.Functions.createPurchaseItemsViewTable();
		
		$(cbo.purchaseOrders).change(PurchaseOrder.Functions.showPurchaseOrder);
		$(btn.conclude).click(PurchaseOrder.Functions.concludePurchaseOrder);
		$(btn.exclude).click(PurchaseOrder.Functions.excludePurchaseOrder);
	},

//------------------------------------------------------------------------- createOrdersTable
	createOrdersTable: function() {
			
		var grid = $(PurchaseOrder.Selectors.Tables.orders),
		    columnsTitles = ['Nome do Usuário', 'Livro', /*'Autor(es)', 
		    				 'Autor(es) Espiritual(ais)',*/'Editora', 'Data', 'Quantidade'],
			columnsSpecification = [
				{name:'userName', index:'userName', width:160},
		        {name:'bookName', index:'bookName', width:220},
		        {name:'publisher', index:'publisher', width:170}, 
		        {name:'date', index:'date', width:110}, 
		        {name:'quantity', index:'quantity', width:70}		
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    height: 'auto',
		    multiselect: false,
		    sortname: 'bookName',
		    viewrecords: true,
		    caption:'Encomendas de Usuário',
		    userdata: {
				purchaseItems: []
			}			
		});			

		$.ajax({
			url: "/gerenciarlivraria/encomendas/json",
			dataType: "json",
			success: function(response) {
				var orders = [];
				$.each(response, function(i, item){
	                var order = {
	                	id: item.pk,
	                	userName: item.fields['user_name'],
	                	bookName: item.fields['name'],
	                	publisher: item.fields['publisher'],
	                	quantity: item.fields['quantity'],
	                	date: item.fields['order_date']
	                };
	                orders[i] = order;
                });

				PurchaseOrder.Functions.listFn(orders, grid);							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});
				
	},
	
//------------------------------------------------------------------------- createPurchaseItemsTable
	createPurchaseItemsTable: function() {
			
		var grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		    columnsTitles = ['Livro', 'Autor(es)', 'Autor(es) Espiritual(ais)','Editora', 
		    			     'Quantidade'],
			columnsSpecification = [
		        {name:'bookName', index:'bookName', width:200},
		        {name:'author', index:'author', width:150},
		        {name:'spiritualAuthor', index:'spiritualAuthor', width:150},
		        {name:'publisher', index:'publisher', width:150}, 
		        {name:'quantity', index:'quantity', width:65}		
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    height: 'auto',
		    multiselect: true,
		    viewrecords: true,
		    caption:'Itens do Pedido de Compra',
		    userdata: {
				purchaseItems: []
			}			
		});	
		
	},

//--------------------------------------------------------------------- createPurchaseItemsViewTable
	createPurchaseItemsViewTable: function() {
			
		var grid = $(PurchaseOrder.Selectors.Tables.purchaseItemsView),
		    columnsTitles = ['Livro', 'Autor(es)', 'Autor(es) Espiritual(ais)','Editora', 
		    			     'Quantidade'],
			columnsSpecification = [
		        {name:'bookName', index:'bookName', width:200},
		        {name:'author', index:'author', width:155},
		        {name:'spiritualAuthor', index:'spiritualAuthor', width:155},
		        {name:'publisher', index:'publisher', width:155}, 
		        {name:'quantity', index:'quantity', width:65}		
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    height: 'auto',
		    viewrecords: true,
		    caption:'Itens do Pedido de Compra'
		});	
		
	},
		
//-------------------------------------------------------------------------- addBookToPurchaseOrder
	addBookToPurchaseOrder: function(event) {
		
		var $messageContainer = $(PurchaseOrder.Selectors.MessageContainers.books),
			bookId = $("#id_book").val(),
		    quantity = $("#id_quantity").val(),
		    messages = [];
		    
		if (bookId == "") {			
			messages[0] = "O campo Livro é obrigatório.";			
		} 
		
		if (quantity == "") {
			
			messages[messages.length] = "O campo Quantidade é obrigatório.";
			
		} else if ( Helpers.Functions.isValidQuantity(quantity) == false) {
			
			messages[messages.length] = "A quantidade é inválida. Preencha com um valor inteiro maior que 0.";
		} else if (quantity == "0" || quantity == "00" || quantity == "000") {
			messages[messages.length] = "A quantidade é inválida. Preencha com um valor inteiro maior que 0.";
		}
				
		if (messages.length != 0) {
			
			Helpers.Functions.showValidationMsg($messageContainer, messages);
			
		} else {		
			$.ajax({
				url: "/gerenciarlivraria/livros/"+bookId+"/json",
				dataType: "json",
				success: function(book) {
					//var book = $.extend({}, json.fields, { id: json.pk });
					
					PurchaseOrder.Functions._addItemToPurchaseOrder(book, quantity);
				},
				error: function() {	
					var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
					Helpers.Functions.showErrorMsg($messageContainer, msg);		
				}
			});
		}
	},
	
//--------------------------------------------------------------------- addBookOrderToPurchaseOrder
	addBookOrderToPurchaseOrder: function(event) {
		
		var $messageContainer = $(PurchaseOrder.Selectors.MessageContainers.orders),
			$ordersGrid = $(PurchaseOrder.Selectors.Tables.orders),
		    bookOrderId = $ordersGrid.jqGrid("getGridParam", "selrow");

		if (bookOrderId == null) {
			
			Helpers.Functions.showWarningMsg($messageContainer, 
											 "Selecione pelo menos uma encomenda para ser rejeitada.");
			
		} else {			
	
			$.ajax({
				url: "/gerenciarlivraria/encomendas/"+bookOrderId+"/json",
				dataType: "json",
				success: function(response) {
					//var book = $.extend({}, json.fields, { id: json.pk });				
					
					PurchaseOrder.Functions._addItemToPurchaseOrder(response.book,
					                                                response.quantity,
					                                                bookOrderId);                  
					                             
					// Esconde a encomenda, para que não possa ser aceita novamente                   
					$ordersGrid.find("#"+bookOrderId).hide();
				},
				error: function() {	
					var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
					Helpers.Functions.showErrorMsg($messageContainer, msg);		
				}
			});
		}
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
					PurchaseOrder.Functions._findPurchaseItemInformationByBookId(purchaseItems,
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
		
		var $messageContainer = $(PurchaseOrder.Selectors.MessageContainers.purchaseOrder),
			$grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		    $ordersGrid = $(PurchaseOrder.Selectors.Tables.orders),
		
			userData = $grid.jqGrid("getGridParam", "userdata"),
			purchaseItems = userData.purchaseItems,
			
			// Faz uma cópia, pra não "confundir" o loop
			selectedIds = $grid.jqGrid("getGridParam", "selarrrow").slice();
		
		if (purchaseItems.length === 0) {
			
			Helpers.Functions.showWarningMsg($messageContainer, 
											 "Não há itens no Pedido de Compras!");
			
		} else if (selectedIds.length === 0) {
			
			Helpers.Functions.showWarningMsg($messageContainer, 
											 "Selecione pelo menos um item do pedido para ser removido.");	
		
	    } else {
	    	
			for (var i = 0; i < selectedIds.length; i++) {
				
				var selectedId = selectedIds[i],
				    purchaseItemInformation = 
				        PurchaseOrder.Functions._findPurchaseItemInformationByBookId(purchaseItems, selectedId),
				    index = purchaseItemInformation.index,
				    bookOrdersIds = purchaseItemInformation.item.bookOrdersIds;
							
				// Remove o item do modelo                                                             
				purchaseItems.splice(index, 1);
				
				// Remove o item da visualização			
				$grid.jqGrid("delRowData", selectedId);
				
				// Mostra novamente na tabela de encomenda
				for (var j = 0; j < bookOrdersIds.length; j++) {
					var bookOrderId = bookOrdersIds[j];
					$ordersGrid.find("#"+bookOrderId).show();
				}
			}
			
			$ordersGrid.jqGrid("resetSelection");	    	
	    }
		
	},	

//------------------------------------------------------------ _findPurchaseItemInformationByBookId
	
	_findPurchaseItemInformationByBookId: function(purchaseItems, bookId) {
	
		for (var i = 0; i < purchaseItems.length; i++) {
			if (purchaseItems[i].bookId == bookId) {
				return { index: i, item: purchaseItems[i] };
			}
		}
	},	

//--------------------------------------------------------------------------------- rejectBookOrder
	
	rejectBookOrder: function() {

		var $grid = $(PurchaseOrder.Selectors.Tables.orders),
			$messageContainer = $(PurchaseOrder.Selectors.MessageContainers.orders),
			selectedRowId = $grid.jqGrid("getGridParam", "selrow");

		if (selectedRowId == null) {
			
			Helpers.Functions.showWarningMsg($messageContainer, 
											 "Selecione pelo menos uma encomenda para ser rejeitada.");
			
		} else {
	    			
			if (selectedRowId != null) {
	
				$.ajax({
					url: "/gerenciarlivraria/encomendas/"+selectedRowId+"/rejeitar",
					dataType: "json",
					success: function(response) {
						
		 				$grid.jqGrid("delRowData", selectedRowId);	
		 				Helpers.Functions.showSuccessMsg($messageContainer, 
		 												 response['success_message']);
					},
					error: function() {	
						var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
						Helpers.Functions.showErrorMsg($messageContainer, msg);		
					}
				});
						
			}
		}
	},	

//------------------------------------------------------------------------------- savePurchaseOrder
	
	savePurchaseOrder: function() {
		
		var $grid = $(PurchaseOrder.Selectors.Tables.purchaseItems),
		    $messageContainer = $(PurchaseOrder.Selectors.MessageContainers.purchaseOrder),
		    $distributor = $("#id_distributor")
			userData = $grid.jqGrid("getGridParam", "userdata"),
			distributor = $distributor.val();
		
		if (userData.purchaseItems.length === 0) {
			
			Helpers.Functions.showWarningMsg($messageContainer, 
											 "Não há itens no Pedido de Compras!");
			
		} else if (distributor === "") {
			
			Helpers.Functions.showValidationMsg($messageContainer, 
												["O campo Distribuidora é obrigatório."]);	
		
	    } else {
			
			var data = { 
				purchaseItems: JSON.stringify(userData.purchaseItems),
				distributor: distributor
			};
			
			$.ajax({
				url: "/gerenciarlivraria/pedidodecompra/salvar/",
				type: "POST",
				data: data,
				dataType: "json",
				success: function(response) {
					
					// Limpa o pedido
					$grid.jqGrid("clearGridData");
					$grid.jqGrid("getGridParam", "userdata").purchaseItems = [];
					$distributor.val("");
					
					Helpers.Functions.showSuccessMsg($messageContainer, 
												     response['success_message']);	
												     
					// Limpa livros
					$("#id_book").val("");		
					$("#id_quantity").val("");
							
				},
				error: function() {	
					var msg = Helpers.Messages.All.ERROR_UNEXPECTED;
					Helpers.Functions.showErrorMsg($messageContainer, msg);		
				}
			});
			
		}
		
	},
	
//------------------------------------------------------------------------------- showPurchaseOrder
	
	showPurchaseOrder: function() {
		var data = {},
			grid = $(PurchaseOrder.Selectors.Tables.purchaseItemsView);
		
		data['purchase_order'] = $(PurchaseOrder.Selectors.Combos.purchaseOrders).val();				
	
		$.ajax({
			url: "/gerenciarlivraria/pedidodecompra/exibir",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				
				var $actions = $("#div_purchase_order_view_actions"),
				    orders = [];
				
				if (response != null) {
					$.each(response.items, function(i, item){
		                var order = {
		                	id: item.pk,
		                	bookName: item.fields['name'],
		                	author: item.fields['author'],
		                	spiritualAuthor: item.fields['spiritual_author'],
		                	publisher: item.fields['publisher'],
		                	quantity: item.fields['quantity']
		                }
		                orders[i] = order;
	                });
	                
	                if (response['read_only'] === false) {
	                	$actions.show();
	                } else {
	                	$actions.hide();
	                }	
				} else {
					$actions.hide();
				}
	
				PurchaseOrder.Functions.listFn(orders, grid);						
			},
			error: function() {	
				//var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				//Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});	
	},

//--------------------------------------------------------------------------- concludePurchaseOrder
	
	concludePurchaseOrder: function() {
			
		PurchaseOrder.Functions._actOnPurchaseOrder("finalizar");
		
	},

//---------------------------------------------------------------------------- excludePurchaseOrder
	
	excludePurchaseOrder: function() {
			
		PurchaseOrder.Functions._actOnPurchaseOrder("excluir");
		
	},

//----------------------------------------------------------------------------- _actOnPurchaseOrder
	
	_actOnPurchaseOrder: function(action) {
			
		var $messageContainer = $(PurchaseOrder.Selectors.MessageContainers.purchaseOrderView),
		    $grid = $(PurchaseOrder.Selectors.Tables.purchaseItemsView),
		    purchaseOrderId = $(PurchaseOrder.Selectors.Combos.purchaseOrders).val();				
	
		$.ajax({
			url: "/gerenciarlivraria/pedidodecompra/"+purchaseOrderId+"/"+action,
			dataType: "json",
			success: function(response) {
				Helpers.Functions.showSuccessMsg($messageContainer, response['success_message']);
				$grid.jqGrid("clearGridData");	
			},
			error: function() {	
				//var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				//Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});
		
	},	
			
//------------------------------------------------------------------------- listFn	
	listFn: function(data, grid)
	{		
		grid.clearGridData();
		
		for(var i = 0; i < data.length; i++)
        {
            grid.jqGrid('addRowData', data[i].id, data[i]);
        }
		
	}
}