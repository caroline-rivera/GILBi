var RegisterEmployee = {};

//------------------------------------------------------------------------------ SELECTORS

RegisterEmployee.Selectors = {
	
	Buttons: {
		search: '#search_button',
		save: '#save_button'
	},
	
	SearchFields: {
		firstName: '#first_name',
		lastName: '#last_name',
		login: '#login',
		email: '#email'
	}
}

//------------------------------------------------------------------------------ FUNCTIONS

RegisterEmployee.Functions = {
	
	init: function()
	{
		var btn = RegisterEmployee.Selectors.Buttons,		
			grid = $('#table_users'),
			columnsTitles = ['Id','Nome','Sobrenome', 'Login', 'E-mail'],
			columnsSpecification = [
			{name:'id', index:'id', hidden:true},
	        {name:'first_name', index:'first_name', width:120},
	        {name:'last_name', index:'last_name', width:120},
	        {name:'login', index:'login', width:120},
	        {name:'email', index:'email', width:300} 		
		];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
			rowList:[5,10,20],
		    height: 'auto',
		    pager: '#busers',		    		    
		    multiselect: true,
		    sortname: 'first_name',
		    viewrecords: true,
		    sortorder: 'asc',
		    caption:'Lista de usuários disponíveis'		    				
		});
		
		$(btn.search).button();
		$(btn.save).button();
									
		$(btn.search).click(RegisterEmployee.Functions.searchFn);
		
		$(btn.save).click(function(){
			var selArrowNumerations = grid.getGridParam('selarrrow');
			var userIds = [];
			
			for (var i = 0; i < selArrowNumerations.length; i++)
			{
				var numeration = selArrowNumerations[i]
				userIds[i] = grid.getRowData(numeration)['id'];
			}
						
			if (userIds.length == 0)
			{
				var msg = Helpers.Messages.RegisterEmployee.NO_SEL_ARROW;
				Helpers.Functions.showPopUpErrorMsg($("#message"), "message", msg);
			}
			else
			{		
				RegisterEmployee.Functions.saveFn(userIds);
			}
		});
	},
		
	searchFn: function()
	{
		var searchFields = RegisterEmployee.Selectors.SearchFields;
		var data = {};
		
		data['first_name'] = $(searchFields.firstName).val().trim();
		data['last_name'] = $(searchFields.lastName).val().trim();
		data['login'] = $(searchFields.login).val().trim();
		data['email'] = $(searchFields.email).val().trim();
		
		$.ajax({
			url: "/cadastrarfuncionario/pesquisar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				var users = [];
				$.each(response, function(i, item){
	                var user = {
	                	id: item.pk,
	                	first_name: item.fields['first_name'],
	                	last_name: item.fields['last_name'],
	                	login: item.fields['login'],
	                	email: item.fields['email']
	                }
	                users[i] = user;
                });
				
				RegisterEmployee.Functions.listFn(users)							
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showPopUpErrorMsg($("#message"), "message", msg);		
			}
		});
	},	
	
	listFn: function(users)
	{		
		var grid = $('#table_users');
		
		grid.clearGridData();
		
		for(var i=0;i<users.length;i++)
        {
            grid.jqGrid('addRowData', i, users[i]);
        }
		
	},
	
	saveFn: function(ids)
	{
		var data = {};		
		data['users_ids'] = [ids];
		data['is_manager'] = $('#manager').is(':checked');
		
		
		$.ajax({
			traditional: true,
			url: "/cadastrarfuncionario/salvar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				if(response['warning_message'] != "")
				{
					Helpers.Functions.showPopUpWarningMsg($("#message"), 
															"message", 
															response['warning_message']);
				}
				
				if(response['success_message'] != "")
				{
					Helpers.Functions.showPopUpSuccessMsg($("#warning_message"), 
															"warning_message", 
															response['success_message']);
				}				
			},
			error: function() {	
				var msg = Helpers.Messages.RegisterEmployee.ERROR_SAVING_EMPLOYEE;
				Helpers.Functions.showPopUpErrorMsg($("#message"), "message", msg);		
			}
		});	
	}
}