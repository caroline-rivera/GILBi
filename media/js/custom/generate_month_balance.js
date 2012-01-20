var GenerateMonthBalance = {};

//-------------------------------------------------------------------------------- SELECTORS

GenerateMonthBalance.Selectors = {
	
	Buttons: {
		generate: '#button_generate'
	},
	
	Tables: {
		balance: '#table_month_balance'
	}	
}

//-------------------------------------------------------------------------------- FUNCTIONS

GenerateMonthBalance.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = GenerateMonthBalance.Selectors.Buttons;
		
		$(btn.generate).click( GenerateMonthBalance.Functions.calculateMonthBalance );	
	},

//------------------------------------------------------------------------- listMonthBalance
	listMonthBalance: function()
	{	
		var grid = $(GenerateMonthBalance.Selectors.Tables.balance),
		    columnsTitles = ['Saldo do Mês anterior', '(+) Total de Vendas do Mês', 
		                     '(-) Total de Compras do Mês','Saldo do Mês'],
			columnsSpecification = [
				{name:'previous_balance', index:'previous_balance', width:200},
				{name:'sale_total', index:'sale_total', width:200},
		        {name:'payment_total', index:'payment_total', width:200},
		        {name:'current_balance', index:'current_balance', width:200}	
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    height: 'auto',
		    multiselect: false,
		    viewrecords: true,
		    caption:'Contabilidade do Mês'				
		});
	},
	
//-------------------------------------------------------------------- calculateMonthBalance	
	calculateMonthBalance: function()
	{
		var grid = $(GenerateMonthBalance.Selectors.Tables.balance),
			$div = $("#month_balance"),
			$messageContainer = $div.find("div.message_container"),
		    data = {};
		
		if ( $('#id_month').val() == "0" ){		
			data['month'] = "";
		}
		else {
			data['month'] = $('#id_month').val();
		}
		
		if ( $('#id_year').val() == "0" ){		
			data['year'] = "";
		}
		else {
			data['year'] = $('#id_year').val();
		}
		
		$.ajax({
			url: "/gerenciarlivraria/relatorios/contabilidade/gerar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				
				if((response['validation_message']).length != 0)
				{
					Helpers.Functions.showValidationMsg($messageContainer, 
														response['validation_message']);
				}
				else
				{
					if (response['error_message'] != "")
					{
						Helpers.Functions.showErrorMsg($messageContainer, 
													   response['error_message']);
					}		
					else
					{
						var arrayBalance = [];
		                var balance = {
		                	previous_balance: response['previous_balance'],
		                	sale_total: response['sale_total'],
		                	payment_total: response['payment_total'],
		                	current_balance: response['current_balance']
		                };
		                arrayBalance[0] = balance;
						GenerateMonthBalance.Functions.listMonthBalance();
						GenerateMonthBalance.Functions.listFn(arrayBalance, grid);					
					}			
				}						
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
		
	}
}	