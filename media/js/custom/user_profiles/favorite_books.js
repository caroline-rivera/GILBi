var FavoriteBooks = {};

//------------------------------------------------------------------------------ SELECTORS

FavoriteBooks.Selectors = {
	
	Buttons: {
		search: '#button_search',
		add: '#button_add'
	},
	
	Tables: {
		favorites: '#table_favorites'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

FavoriteBooks.Functions = {

//------------------------------------------------------------------------------ init

	init: function(serverParams)
	{
		var btn = FavoriteBooks.Selectors.Buttons,
			grid = $(FavoriteBooks.Selectors.Tables.favorites);
					
		FavoriteBooks.Functions.listBooksFavoritesTab();
		
		$(btn.search).click( function() {
			
			FavoriteBooks.Functions.searchBooksFn();
		});	
		
		$(btn.add).click( function() {

			FavoriteBooks.Functions.getSelectedColumnsFn(grid);	
		});			
	},

//------------------------------------------------------------------------- listBooksFavoritesTab
	listBooksFavoritesTab: function()
	{	
		var table = FavoriteBooks.Selectors.Tables,	
			grid = $(table.favorites),
			columnsTitles = ['Id', 'Nome do Livro','Autor(es)', 'Autor(es) Espiritual(ais)', 'Editora'],
			columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'name', index:'name', width:270},
	        {name:'author', index:'author', width:160},
	        {name:'spiritual_author', index:'author', width:160},
	        {name:'publisher', index:'publisher', width:170} 		
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


//------------------------------------------------------------------------- searchBooksFn	
	searchBooksFn: function()
	{
		var grid = $(FavoriteBooks.Selectors.Tables.favorites),
			$messageContainer = $("#message_container");
			data = {};
				
		data['name'] = $('#name').val().trim();
		data['author'] = $('#author').val().trim();
		data['publisher'] = $('#publisher').val().trim();	
	
		
		$.ajax({
			url: "/acervo/livros/pesquisar/",
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

				FavoriteBooks.Functions.listFn(books, grid);							
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
	getSelectedColumnsFn: function(grid)
	{
		var $messageContainer = $("#message_container"),
			selArrowNumerations = grid.getGridParam('selarrrow'),
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
			FavoriteBooks.Functions.addFavorites(bookIds);
		}
	},


//------------------------------------------------------------------------- addFavorites		
	addFavorites: function(ids)
	{
		var data = {},	
			url = "/perfil/livrosfavoritos/adicionar/",
			grid = $(FavoriteBooks.Selectors.Tables.favorites),
			$messageContainer = $("#message_container");
		
		data['book_ids'] = [ids];
		
	
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
	}
    
}
