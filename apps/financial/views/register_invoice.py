# encoding: utf-8

import json
from decimal import *
from datetime import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from gilbi.apps.financial.models import Duplicate, Invoice, Payment
from gilbi.apps.bookstore.models import BookstoreBook
from gilbi.apps.financial.forms import RegisterInvoiceForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_PURCHASE_ORDER
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_INVOICE

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_invoice = RegisterInvoiceForm()
        return render_to_response('financial/register_invoice.html', 
                                  {
                                   'form_invoice': form_invoice,
                                   'is_manager': validate_manager_session(request),
                                   'is_seller': validate_seller_session(request) 
                                   },
                                  context_instance=RequestContext(request)) 
        
def register(request):

    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        result = {}
        result['success_message'] = ""
        result['error_message'] = ""
        result['validation_message'] = []      
              
        if request.method == 'GET' and 'purchase_order' in request.GET and \
                                       'number' in request.GET and \
                                       'series' in request.GET and \
                                       'duplicates_number' in request.GET :
            
            form = RegisterInvoiceForm(request.GET, request.FILES)
            duplicates = separate_duplicate_fields(request.GET)
            validated_duplicates = validate_duplicates(duplicates)

        
            if form.is_valid() and len(validated_duplicates['messages']) == 0:
                checked_form = form.cleaned_data
                purchase_order = checked_form['purchase_order']  
                number = checked_form['number']  
                series = checked_form['series']  

                new_invoice = Invoice(number = number,
                                      series = series,
                                      purchase_order = purchase_order
                                  )
                new_invoice.save()
                  
                for duplicate in validated_duplicates['duplicates']:
                    new_duplicate = Duplicate(invoice = new_invoice,
                                              number = duplicate[0],
                                              expiration_date = duplicate[1],
                                              value = duplicate[2]
                                              )
                    new_duplicate.save()
    
                
                update_books_quantity(purchase_order)
                             
                result['success_message'] = SUCCESS_REGISTER_INVOICE      
                    
            else:                                 
                if form._errors and 'purchase_order' in form._errors:
                    if form._errors['purchase_order'][0] == ERROR_REQUIRED_PURCHASE_ORDER:
                        result['validation_message'].append(form._errors['purchase_order'][0])
                    else:
                        result['error_message'] = form._errors['purchase_order'][0]
                        
                if form._errors and 'number' in form._errors:
                    result['validation_message'].append(form._errors['number'][0]) 

                if form._errors and 'series' in form._errors:
                    result['validation_message'].append(form._errors['series'][0])  
                
                if len(validated_duplicates['messages']) != 0:
                    for message in validated_duplicates['messages']:
                        result['validation_message'].append(message)
          
            response = json.dumps(result)                
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 
        
def separate_duplicate_fields(request_get):
    duplicates_quantity_str = request_get['duplicates_number']
    duplicates_number = int(duplicates_quantity_str)
    duplicates = []
    
    for i in range(1,duplicates_number + 1):
        field = 'duplicate_' + str(i)
        if field in request_get :
            duplicate = request_get[field].split(';')
            duplicates.append(duplicate)
            
    return duplicates

def validate_duplicates(duplicates):
    result = {}
    validation_message = []
    number = 1
        
    for duplicate in duplicates:
        duplicate[0] = number
        try:
            date = datetime.strptime(duplicate[1], "%d/%m/%Y")
            duplicate[1] = date
        except ValueError:
            validation_message.append("A Data de Expiração da Duplicata número " + str(number) + " é inválida.")
        
        try:
            if duplicate[2].find("R$ ") != -1:
                str_value = duplicate[2].replace("R$ ","")
            value = Decimal(str_value)
            duplicate[2] = value            
        except InvalidOperation:
            validation_message.append("O Valor da Duplicata número " + str(number) + " é inválido.")
        
        number += 1 
  
    result['messages'] = validation_message
    result['duplicates'] = duplicates  
    
    return result   

def update_books_quantity(purchase_order):
    items = purchase_order.itens.all()
    
    for item in items:
        reserved_quantity = 0
        
        orders = item.book_order.all()
        for order in orders:
            order.available_order() # setar situacao para 'D'
            order.save()
            reserved_quantity += order.quantity
        
        available_quantity = item.quantity - reserved_quantity
        
        bookstore_book = BookstoreBook.objects.get(id=item.book.id)
        bookstore_book.update_book_quantity(item.quantity, available_quantity)
        bookstore_book.save()
        