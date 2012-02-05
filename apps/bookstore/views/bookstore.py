# -*- encoding: utf-8 -*-
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from gilbi.mistrael.messages.success_messages import *
from gilbi.mistrael.messages.error_messages import *
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.apps.bookstore.models import BookOrder, BookstoreBook
from gilbi.apps.books.models import Book
from gilbi.apps.user_profiles.models import User
from gilbi.apps.bookstore.grid_formats import BookGridFormat, OrderGridFormat
from datetime import datetime

def index(request):
    c = {}
    c.update(csrf(request))            
    context = RequestContext(request, c)
    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    else:
        template = loader.get_template('bookstore/bookstore.html')
        return HttpResponse(template.render(context)) 
    
def search_books(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    
    if request.method == 'POST':
        return HttpResponseRedirect('/livraria/') 
    
    elif 'name' in request.GET and 'author' in request.GET and 'publisher' in request.GET:
        book_name = request.GET['name']
        author_name = request.GET['author']  
        publisher_name = request.GET['publisher']  
        
        books = []

        if(book_name != ""):
            all_books = BookstoreBook.objects.filter(name__icontains = book_name)
        else:
            all_books = BookstoreBook.objects.all()
        
        if(author_name != ""):
            for book in all_books:
                authors = book.authors.all()
                for author in authors:
                    if author.name.upper().find( author_name.upper()) != -1:
                        books.append(book)

        if(publisher_name != ""):
            for book in all_books:
                if book.publisher.name.upper().find( publisher_name.upper()) != -1:
                    if not (book in books):
                        books.append(book)     
                       
        if (book_name == "") and (author_name == "") and (publisher_name == ""):
            books = BookstoreBook.objects.all()  
        elif (author_name == "") and (publisher_name == ""):
            for book in all_books:
                books.append(book)    
          
        grid_books = transform_to_grid_book_list(books)    
 
        response = serializers.serialize("json",  grid_books)     
        return HttpResponse(response, mimetype="text/javascript")
    
    else:
        return HttpResponseRedirect('/livraria/') 

def add_favorites(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    
    if request.method == 'GET' and 'book_ids' in request.GET:        
        str_ids = request.GET['book_ids']          
        str_array_ids = str_ids.split(',')
        
        user_id = request.session['user_id']        
        user = User.objects.get(id=user_id)
        
        total_favorites = 0      
                 
        for id in str_array_ids:
            book_id = int(id)

            if Book.objects.filter(id=book_id).exists() == True:
                book = Book.objects.get(id=book_id)
                
                favorites = user.favorite_books.all()
                if book not in favorites:
                    user.favorite_books.add(book)
                    total_favorites += 1
            
        result = {}
        result['success_message'] = ""
        result['warning_message'] = ""
        result['error_message'] = ""  
        result['validation_message'] = []
                       
        if(total_favorites == 0):
            result['warning_message'] = ERROR_ADD_FAVORITE_BOOK
        else:
            result['success_message'] = SUCCESS_ADD_FAVORITE_BOOK + str(total_favorites)
                    
        response = json.dumps(result)
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/livraria/') 

def order_books(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')

    result = {}
    result['success_message'] = ""
    result['error_message'] = ""
    result['warning_message'] = ""
    result['validation_message'] = []
            
    if request.method == 'GET' and 'book_ids' in request.GET and 'quantity' in request.GET:              
        if validate_quantity(request.GET['quantity']) == False:
            result['validation_message'].append(ERROR_INVALID_QUANTITY)
        else:
            book_id = int(request.GET['book_ids'])
            quantity = int(request.GET['quantity'])  
            user_id = request.session['user_id']    
                
            user = User.objects.get(id=user_id)  
            book = BookstoreBook.objects.get(id=book_id)  
            
            book_order = BookOrder(user=user,
                                   book=book,
                                   quantity = quantity,
                                   situation='S', #Solicitada
                                   order_date= datetime.now())
            
            book_order.save()
            result['success_message'] = SUCCESS_ORDERING_BOOK
            
        response = json.dumps(result)
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/livraria/') 

def list_orders(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
            
    if request.method == 'GET':              
        user_id = request.session['user_id']    
            
        user = User.objects.get(id=user_id)  
        
        orders = BookOrder.objects.filter(user=user)
            
        user_orders = transform_to_grid_order_list(orders)    

        response = serializers.serialize("json",  user_orders)     
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/livraria/')

def cancel_orders(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')

    result = {}
    result['success_message'] = ""
    result['error_message'] = ""
    result['warning_message'] = ""
    result['validation_message'] = []
            
    if request.method == 'GET' and 'order_ids' in request.GET:              
        order_id = int(request.GET['order_ids'])
 
        order = BookOrder.objects.get(id=order_id) 
        
        if (order.situation == 'R' or order.situation == 'A' or \
            order.situation == 'D' or order.situation == 'V'):
            result['error_message'] = ERROR_CANCELING_ORDER
        elif(order.situation == 'C'):
            result['error_message'] = ERROR_ORDER_ALREADY_CANCELED
        else:
            order.cancel_order()        
            order.save()
            result['success_message'] = SUCCESS_CANCELING_ORDER
            
        response = json.dumps(result)
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/livraria/')
       
def transform_to_grid_book_list(books):
    grid_list = []
    for book in books:
        book_grid_format = BookGridFormat(book)   
        grid_list.append(book_grid_format)
    return grid_list

def transform_to_grid_order_list(orders):
    grid_list = []
    for order in orders:
        order_grid_format = OrderGridFormat(order)   
        grid_list.append(order_grid_format)
    return grid_list

def validate_quantity(str_quantity):
    try:
        quantity = int(str_quantity)
        if quantity >= 1 and quantity <= 20:
            is_valid = True
        else:
            is_valid = False
    except ValueError:
        is_valid = False
        
    return is_valid