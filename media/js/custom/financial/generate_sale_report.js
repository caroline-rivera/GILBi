var GenerateSaleReport = {};

//-------------------------------------------------------------------------------- SELECTORS

GenerateSaleReport.Selectors = {
	
	Buttons: {
		generate: '#button_generate'
	},
	
	Tables: {
		sales: '#table_sales_report'
	}	
}

//-------------------------------------------------------------------------------- FUNCTIONS

GenerateSaleReport.Functions = {

//------------------------------------------------------------------------------------- init	
	init: function()
	{
		var btn = GenerateSaleReport.Selectors.Buttons;
		
		$(btn.generate).click( GenerateSaleReport.Functions.getAllSales );	
	},

//------------------------------------------------------------------------- createSalesTable
	createSalesTable: function()
	{	
		var grid = $(GenerateSaleReport.Selectors.Tables.sales),
		    columnsTitles = ['Livro', 'Autor(es)', 'Autor(es) Espiritual(ais)',
		                     'Editora','Qtd', 'Preço Total', 'Data de Venda'],
			columnsSpecification = [
				{name:'name', index:'name', width:200},
				{name:'author', index:'author', width:145},
		        {name:'spiritual_author', index:'spiritual_author', width:145},
		        {name:'publisher', index:'publisher', width:145},	
		        {name:'quantity', index:'quantity', width:50},
		        {name:'price', index:'price', width:70},
		        {name:'date', index:'date', width:80}
			];
		
		grid.jqGrid({
			datatype: 'local',
			colNames: columnsTitles,
		    colModel:columnsSpecification,
		    rowList:[10,20,30],
		    height: 'auto',
		    pager: '#bsales',
		    sortname: 'name',
		    sortorder: 'asc',
		    multiselect: false,
		    viewrecords: true,
		    caption:'Livros vendidos no período'				
		});
	},
		
//------------------------------------------------------------------------------ getAllSales	
	getAllSales: function()
	{
		var grid = $(GenerateSaleReport.Selectors.Tables.sales),
			$div = $("#sale_report"),
			$messageContainer = $div.find("div.message_container"),
		    data = {};
		
		data['initial_date'] = $("#id_initial_date").val();
		data['ending_date'] = $("#id_ending_date").val();
		
		$.ajax({
			url: "/gerenciarlivraria/relatorios/vendas/listar/",
			dataType: "json",
			data: data,
			async: true,
			success: function(response) {
				if(response.hasOwnProperty('validation_message'))
				{
					if((response['validation_message']).length != 0)
					{
						grid.clearGridData();
						Helpers.Functions.showValidationMsg($messageContainer, 
															response['validation_message']);
					}
				}
				else
				{
					var sales = [];
					$.each(response, function(i, item){
		                var sale = {
		                	name: item.fields['name'],
		                	author: item.fields['author'],
		                	spiritual_author: item.fields['spiritual_author'],
		                	publisher: item.fields['publisher'],
		                	quantity: item.fields['quantity'],
		                	price: item.fields['price'],
		                	date: item.fields['date']
		                };
		                sales[i] = sale;
	                });
	                
					GenerateSaleReport.Functions.createSalesTable();
					Helpers.Functions.listFn(sales, grid);				
				}						
			},
			error: function() {	
				var msg = Helpers.Messages.All.ERROR_LOADING_TABLE;
				Helpers.Functions.showErrorMsg($messageContainer, msg);		
			}
		});		
	}
}	