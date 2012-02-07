# encoding: utf-8

import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from decimal import Decimal
from gilbi.apps.financial.forms import GenerateSaleReportForm
from gilbi.apps.financial.grid_formats import ShelfSaleGridFormat, OrderSaleGridFormat
from gilbi.apps.bookstore.models import ShelfSale
from gilbi.apps.bookstore.models import OrderSale
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')

    form = GenerateSaleReportForm()
        
    return render_to_response('financial/generate_sale_report.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
    
def list_sales(request):     
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        result = {}
        result['validation_message'] = []
                        
        if request.method == 'GET' and 'initial_date' in request.GET and 'ending_date' in request.GET:
         
            form = GenerateSaleReportForm(request.GET, request.FILES)
            
            if form.is_valid():
                checked_form = form.cleaned_data
                initial_date = checked_form['initial_date']
                ending_date = checked_form['ending_date']
                
                shelf_sales = ShelfSale.objects.filter(date_of_sale__range = (initial_date, ending_date))
                order_sales = OrderSale.objects.filter(date_of_sale__range = (initial_date, ending_date))    
                
                shelf_sale_grid_format = get_shelf_sale_grid_format(shelf_sales)
                order_sale_grid_format = get_order_sale_grid_format(order_sales)
                
                sales = get_all_sales(shelf_sale_grid_format, order_sale_grid_format)  
                                
                total_sales_price = calculate_total_of_sales(shelf_sales, order_sales) 

                partial_response = serializers.serialize("json", sales)        
                sales_json = json.loads(partial_response)
                                    
                response_dic = {
                    'sales': sales_json,
                    'total_sales_price': str(total_sales_price),
                }
                
                response = json.dumps(response_dic)       
       
            else:
                if form._errors and 'initial_date' in form._errors:
                    result['validation_message'].append(form._errors['initial_date'][0])  
                                  
                if form._errors and 'ending_date' in form._errors:
                    result['validation_message'].append(form._errors['ending_date'][0])
       
                response = json.dumps(result)
                
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 

def get_shelf_sale_grid_format(shelf_sales):
    shelf_sales_grid_format = []
    
    for sale in shelf_sales:
        shelf_sale_grid_format = ShelfSaleGridFormat(sale)  
        shelf_sales_grid_format.append(shelf_sale_grid_format)
        
    return shelf_sales_grid_format
              

def get_order_sale_grid_format(order_sales):
    order_sales_grid_format = []
    
    for sale in order_sales:
        order_sale_grid_format = OrderSaleGridFormat(sale)  
        order_sales_grid_format.append(order_sale_grid_format)
        
    return order_sales_grid_format

def get_all_sales(shelf_sales, order_sales):
    all_sales = []
    
    for sale in shelf_sales:
        all_sales.append(sale)
        
    for sale in order_sales:
        all_sales.append(sale)
    
    return all_sales

def calculate_total_of_sales(shelf_sales, order_sales):
    total_sales_price = Decimal('0.00')  
      
    for sale in shelf_sales:
        total_sales_price = total_sales_price + sale.price_of_sale
        
    for sale in order_sales:
        total_sales_price = total_sales_price + sale.price_of_sale  
        
    return total_sales_price
