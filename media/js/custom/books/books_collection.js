var BooksCollection = {};

//-------------------------------------------------------------------------------- SELECTORS

BooksCollection.Selectors = {
	
	Buttons: {
		register_author: '#button_register_author',
		register_book: '#button_register_book',
		register_publisher: '#button_register_publisher'
	}
}

//-------------------------------------------------------------------------------- FUNCTIONS

BooksCollection.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = BooksCollection.Selectors.Buttons;

		$("a[href=#tab1]").click(function(){
			location.reload();
		});
		
		$("a[href=#tab2]").click(function(){
			BooksCollection.Functions.cleanPageData();
		});
		
		$("a[href=#tab3]").click(function(){
			BooksCollection.Functions.cleanPageData();
		});	
			
		$(btn.register_book).click( BooksCollection.Functions.registerNewBook );
		$(btn.register_author).click( BooksCollection.Functions.registerNewAuthor );
		$(btn.register_publisher).click( BooksCollection.Functions.registerNewPublisher );	
	},

//--------------------------------------------------------------------------- registerNewBook	
	registerNewBook: function()
	{
		var $tab = $('#tab1'),
			$messageContainer = $tab.find("div.message_container"),
			url = "/acervo/cadastrarlivro/?name="
		    data = {};		
		
		url += $("#id_name").val();
		url += "&photo=";
		url += $("#id_photo").val();
		url += "&description=";
		url += $("#id_description").val();
		url += "&publisher=";
		url += $("#id_publisher").val();

		if ($("#id_author").val() != null)
		{
			var authors  = $("#id_author").val();
			
			for(var i = 0; i < authors.length; i++)
			{
				url += "&author=";
				url += authors[i];
			}
		}

		if ($("#id_spiritual_author").val() != null)
		{
			var authors  = $("#id_spiritual_author").val();
			
			for(var i = 0; i < authors.length; i++)
			{
				url += "&spiritual_author=";
				url += authors[i];
			}
		}	

		/*			
		data['name'] = $("#id_name").val();
		data['photo'] = $("#id_photo").val();
		data['description'] = $("#id_description").val();
		data['publisher'] = $("#id_publisher").val();
		data['author'] = [];
		
		if ($("#id_author").val() != null)
		{
			//data['author'] = $("#id_author").val();
			var authors  = $("#id_author").val();
			
			for(var i = 0; i < authors.length; i++)
			{
				data['author'][i] = authors[i];
			}
		}

		if ($("#id_spiritual_author").val() != null)
		{
			data['spiritual_author'] = $("#id_spiritual_author").val();
		}	
*/
		BooksCollection.Functions.sendData(url, data, $messageContainer)		
	},

//--------------------------------------------------------------------------- registerNewAuthor	
	registerNewAuthor: function()
	{
		var $tab = $('#tab2'),
			$messageContainer = $tab.find("div.message_container"),
			url = "/acervo/cadastrarautor/",
		    data = {};		

		data['author_name'] = $("#id_author_name").val();
		
		BooksCollection.Functions.sendData(url, data, $messageContainer);		
	},

//------------------------------------------------------------------------ registerNewPublisher	
	registerNewPublisher: function()
	{
		var $tab = $('#tab3'),
			$messageContainer = $tab.find("div.message_container"),
			url = "/acervo/cadastrareditora/",
		    data = {};		

		data['publisher_name'] = $("#id_publisher_name").val();
		
		BooksCollection.Functions.sendData(url, data, $messageContainer);		
	},
		
//--------------------------------------------------------------------------- sendData	
	sendData: function(url, data, $messageContainer)
	{
		$.ajax({
			url: url,
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {				
				if( (response['validation_message']).length != 0 )
				{
					Helpers.Functions.showValidationMsg($messageContainer, 
														response['validation_message']);
				}
				else
				{
					if( (response['error_message']).length != 0 )
					{
						Helpers.Functions.showErrorMsg($messageContainer, 
															response['error_message']);
					}
					if( (response['success_message']).length != 0 )
					{
						BooksCollection.Functions.cleanPageData();
						Helpers.Functions.showSuccessMsg($messageContainer, 
															response['success_message']);
					}
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
		$('#id_name').val("");	
		$('#id_photo').val("");	
		$('#id_description').val("");
		$('#id_author').val("");
		$('#id_spiritual_author').val("");
		$('#id_publisher').val("");

		$('#id_author_name').val("");
		
		$('#id_publisher_name').val("");
	},
}	