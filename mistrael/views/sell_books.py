# -*- encoding: utf-8 -*-

import json

from decimal import *
from datetime import date

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_seller_session
from gilbi.mistrael.models.user import User
from gilbi.mistrael.models.book_order import BookOrder
from gilbi.mistrael.models.bookstore_book import BookstoreBook
from gilbi.mistrael.models.sale import OrderSale
from gilbi.mistrael.models.sale import ShelfSale
from gilbi.mistrael.forms.shelf_sale_form import FormShelfSale
from gilbi.mistrael.transformers.order_transformer import GridOrderTransform
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_ID, ERROR_REQUIRED_BOOK_PRICE
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_BOOK_PRICE
from gilbi.mistrael.messages.error_messages import ERROR_UNAVAILABLE_BOOK, ERROR_INVALID_BOOK
from gilbi.mistrael.messages.success_messages import SUCCESS_SELLING_BOOK, SUCCESS_SELLING_ORDER
from gilbi.mistrael.messages.error_messages import ERROR_NO_ORDER_ROW_SELECTED, ERROR_INVALID_ORDER
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_ORDER_PRICE,ERROR_UNAVAILABLE_ORDER
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_ORDER_PRICE
from gilbi.mistrael.transformers.book_transformer import GridBookstoreBook

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_seller_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_shelfsale = FormShelfSale()
        return render_to_response('sell_books.html', 
                                  {'form_shelf_sale': form_shelfsale},
                                  context_instance=RequestContext(request)) 
        
        
def show_book_informations(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_seller_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    elif request.method == 'GET' and 'book_id' in request.GET:   
        str_id = request.GET['book_id'] 
        
        book_list = []
        if(str_id != ""):                     
            book_id = int(str_id)            
            bookstore_book = BookstoreBook.objects.get(id=book_id)
            book = GridBookstoreBook(bookstore_book)            
            book_list.append(book)
               
        response = serializers.serialize("json", book_list)     
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/gerenciarbiblioteca/')    
    
def sell_shelf_book(request):   
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_seller_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else: 
        result = {}
        result['validation_message'] = []
        result['success_message'] = ""
        result['error_message'] = ""
            
        if request.method == 'GET' and 'book_id' in request.GET and 'book_price' in request.GET:   

            if request.GET['book_id'] == "":
                result['validation_message'].append(ERROR_REQUIRED_BOOK_ID)
            
            if request.GET['book_price'] == "":
                result['validation_message'].append(ERROR_REQUIRED_BOOK_PRICE)
            else:
                valid_price = validate_price(request.GET['book_price']) 
                if valid_price == None:
                    result['validation_message'].append(ERROR_INVALID_BOOK_PRICE)

            if is_valid_book(request.GET['book_id']) == True:   
                book = BookstoreBook.objects.get(id=int(request.GET['book_id'])) 
                if book.avaiable_quantity == 0 and len(result['validation_message']) == 0:
                    result['error_message'] = ERROR_UNAVAILABLE_BOOK
            else:
                book = None
                if len(result['validation_message']) == 0:
                    result['error_message'] = ERROR_INVALID_BOOK

            if len(result['validation_message']) == 0 and result['error_message'] == "":   
                book.sell_book()
                sale = ShelfSale(date_of_sale = date.today(),
                                 price_of_sale = valid_price,
                                 book = book) 
                sale.save()
                book.save() 
                result['success_message'] = SUCCESS_SELLING_BOOK
                          
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript")    
        
        else:
            return HttpResponseRedirect('/vendas/')
                   
def search_user_orders(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_seller_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:           
        if request.method == 'GET' and 'login' in request.GET and 'email' in request.GET:              
            user_login = request.GET['login'].strip()    
            user_email = request.GET['email'].strip()
            user = None
            available_orders = []
            
            kwargs = {}
            if(user_login != ""):
                kwargs['login'] = user_login
            if(user_email != ""):
                kwargs['email'] = user_email   
                
            if(kwargs != {}):
                if User.objects.filter(**kwargs).exists() == True:
                    user = User.objects.get(**kwargs)     
                               
            if user is not None:
                if BookOrder.objects.filter(
                                       user = user.id,
                                       situation = "D"
                                       ).exists() == True:
                    available_orders = BookOrder.objects.filter(user = user.id, situation = "D")   
                                                      
            user_orders = transform_to_grid_order_list(available_orders)    

            
            response = serializers.serialize("json",  user_orders)     
            return HttpResponse(response, mimetype="text/javascript")
        else:
            return HttpResponseRedirect('/vendas/')

def sell_order_book(request):   
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_seller_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else: 
        result = {}
        result['validation_message'] = []
        result['success_message'] = ""
        result['error_message'] = ""
            
        if request.method == 'GET' and 'order_id' in request.GET and 'order_price' in request.GET:   

            if request.GET['order_id'] == "":
                result['validation_message'].append(ERROR_NO_ORDER_ROW_SELECTED)
            
            if request.GET['order_price'] == "":
                result['validation_message'].append(ERROR_REQUIRED_ORDER_PRICE)
            else:
                valid_price = validate_price(request.GET['order_price']) 
                if valid_price == None:
                    result['validation_message'].append(ERROR_INVALID_ORDER_PRICE)

            if is_valid_order(request.GET['order_id']) == True:   
                order = BookOrder.objects.get(id=int(request.GET['order_id'])) 
                if order.situation != "D" and len(result['validation_message']) == 0:
                    result['error_message'] = ERROR_UNAVAILABLE_ORDER
            else:
                order = None
                if len(result['validation_message']) == 0:
                    result['error_message'] = ERROR_INVALID_ORDER

            if len(result['validation_message']) == 0 and result['error_message'] == "":   
                book = BookstoreBook.objects.get(id=order.book.id)
                book.sell_order()
                order.sell_order()
                sale = OrderSale(date_of_sale = date.today(),
                                 price_of_sale = valid_price,
                                 book_order = order) 
                sale.save()
                order.save() 
                result['success_message'] = SUCCESS_SELLING_ORDER 
                          
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript")    
        
        else:
            return HttpResponseRedirect('/vendas/')
              
def transform_to_grid_order_list(orders):
    grid_list = []
    for order in orders:
        order_grid_format = GridOrderTransform(order)   
        grid_list.append(order_grid_format)
    return grid_list

def is_valid_book(str_book_id):
    try:
        order_id = int(str_book_id)
        if BookstoreBook.objects.filter(id= order_id).exists():
            is_valid = True
        else:
            is_valid = False
    except ValueError:
        is_valid = False
        
    return is_valid  
    
def is_valid_order(str_order_id):
    try:
        order_id = int(str_order_id)
        if BookOrder.objects.filter(id= order_id).exists():
            is_valid = True
        else:
            is_valid = False
    except ValueError:
        is_valid = False
        
    return is_valid  
  
def validate_price(str_price):
    try:
        if str_price.find("R$ ") != -1:
            str_price = str_price.replace("R$ ","")
        price = Decimal(str_price)
        valid_price = price
    except InvalidOperation:
        valid_price = None
        
    return valid_price 