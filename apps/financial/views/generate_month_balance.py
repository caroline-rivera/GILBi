# encoding: utf-8

import json
from decimal import Decimal
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.apps.bookstore.models import ShelfSale
from gilbi.apps.bookstore.models import OrderSale
from gilbi.apps.financial.models import MonthBalance
from gilbi.apps.financial.models import Payment
from gilbi.apps.financial.models import Duplicate
from gilbi.apps.financial.forms import GenerateMonthBalanceForm
from gilbi.apps.financial.forms.generate_month_balance import get_previous_month_year
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session
from gilbi.mistrael.messages.error_messages import ERROR_MISSING_PREVIOUS_BALANCE


def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form = GenerateMonthBalanceForm()
            
        return render_to_response('financial/generate_month_balance.html', 
                                  {
                                   'form': form,
                                   'is_manager': validate_manager_session(request),
                                   'is_seller': validate_seller_session(request) 
                                   },
                                  context_instance=RequestContext(request))
    
def calculate(request):           
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        result = {}
        result['validation_message'] = []
        result['error_message'] = "" 
            
        if request.method == 'GET' and 'month' in request.GET and 'year' in request.GET:
            form = GenerateMonthBalanceForm(request.GET, request.FILES)
            
            if form.is_valid():
                checked_form = form.cleaned_data
                str_month = checked_form['month']
                str_year = checked_form['year']
                
                int_month = int(str_month)
                int_year = int(str_year)
                
                previous_month_year = get_previous_month_year(int_month, int_year)
                
                previous_balance = get_previous_balance(previous_month_year)     
                sale_total = get_total_of_sales(int_month, int_year)        
                payment_total = get_total_of_payments(int_month, int_year)
                current_balance = previous_balance + sale_total - payment_total
                                                  
                result['previous_balance'] = str(previous_balance)
                result['sale_total'] = str(sale_total)
                result['payment_total'] = str(payment_total)
                result['current_balance'] = str(current_balance)     
                                              
                if MonthBalance.objects.filter(month = int_month, year = int_year).exists() == False:                 
                    balance = MonthBalance (month = int_month,
                                            year = int_year,
                                            value = current_balance)
                    balance.save()
                    
                else:
                    balance = MonthBalance.objects.get(month = int_month, year = int_year)
                    
                    if (int_year < date.today().year) or (int_year == date.today().year \
                                                          and int_month < date.today().month):
                        result['current_balance'] = str(balance.value)
                    else:    
                        balance.update_value(current_balance)
                        balance.save()
                
            if form._errors and 'month' in form._errors:
                result['validation_message'].append(form._errors['month'][0])  
                              
            if form._errors and 'year' in form._errors:
                if form._errors['year'][0] == ERROR_MISSING_PREVIOUS_BALANCE:
                    result['error_message'] = form._errors['year'][0]
                else:
                    result['validation_message'].append(form._errors['year'][0])
       
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 
        
def get_previous_balance(previous_month_year):
    previous_balance = Decimal('0.00')
    
    if MonthBalance.objects.filter(month = previous_month_year['previous_month'], 
                                   year = previous_month_year['previous_year']).exists() == True:
        month_balance = MonthBalance.objects.get(month = previous_month_year['previous_month'], 
                                                 year = previous_month_year['previous_year'])
        previous_balance = month_balance.value
    
    return previous_balance

def get_total_of_sales(month, year):
    total_of_sales = Decimal('0.00')
    
    shelf_sale = ShelfSale.objects.filter(date_of_sale__month = month, 
                                          date_of_sale__year = year)
    
    order_sale = OrderSale.objects.filter(date_of_sale__month = month, 
                                          date_of_sale__year = year)
    
    for sale in shelf_sale:
        total_of_sales = total_of_sales + sale.price_of_sale
        
    for sale in order_sale:
        total_of_sales = total_of_sales + sale.price_of_sale  
        
    return Decimal(str(total_of_sales))

def get_total_of_payments(month, year):
    total_of_payments = Decimal('0.00')
    duplicates = []
    
    payments = Payment.objects.filter(payment_date__month = month, 
                                      payment_date__year = year)
    
    for payment in payments:
        duplicate = Duplicate.objects.get(payment = payment.id)
        duplicates.append(duplicate)
        
    for duplicate in duplicates:
        total_of_payments = total_of_payments + duplicate.value
        
    return Decimal(str(total_of_payments))