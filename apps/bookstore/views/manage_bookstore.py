# encoding: utf-8

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.shortcuts import render_to_response
from gilbi.apps.books.models import Book
from gilbi.apps.bookstore.models import BookOrder
from gilbi.apps.bookstore.grid_formats import OrderGridFormat
from gilbi.apps.bookstore.models import Distributor
from gilbi.apps.bookstore.forms import RegisterDistributorForm
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_NEW_DISTRIBUTOR, SUCCESS_REJECT_BOOK_ORDER
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:   
        return render_to_response('bookstore/manage_bookstore.html', 
                                  {
                                   'is_manager': validate_manager_session(request),
                                   'is_seller': validate_seller_session(request)
                                   }, 
                                   context_instance=RequestContext(request))

    
def get_book_json(request, book_id):
    book = Book.objects.get(id=book_id)

    # TODO: Usar o serializers
    book_dictionary = {
        'id': book.id,
        'name': book.name,
        'author': '\n'.join([str(book_author) for book_author in book.bookauthor_set.filter(category='F')]),
        'spiritualAuthor': '\n'.join([str(book_author) for book_author in book.bookauthor_set.filter(category='E')]),
        #'author': [str(book_author) for book_author in book.bookauthor_set.filter(category='F')],
        #'spiritualAuthor': [str(book_author) for book_author in book.bookauthor_set.filter(category='E')],
        'publisher': str(book.publisher)
    }
    
    response = json.dumps(book_dictionary)
    return HttpResponse(response, mimetype="text/javascript")

def get_requested_orders(request):
    orders = BookOrder.objects.filter(situation="S")
    orders_grid_format = []
    
    for order in orders:
        order_grid_format = OrderGridFormat(order)
        orders_grid_format.append(order_grid_format)
    
    response = serializers.serialize("json", orders_grid_format)     
    return HttpResponse(response, mimetype="text/javascript")

def get_book_order_book_json(request, book_order_id):  
    book_order = BookOrder.objects.get(id=book_order_id) 
    
    book = {
        "id": book_order.book.id,
        "name": book_order.book.name,
        "author": '\n'.join([str(book_author) for book_author in book_order.book.bookauthor_set.filter(category='F')]),
        "spiritualAuthor": '\n'.join([str(book_author) for book_author in book_order.book.bookauthor_set.filter(category='E')]),
        "publisher": str(book_order.book.publisher)
    }
    
    # TODO: Usar o serializers
    book_dictionary = {
        'book': book,
        'quantity': book_order.quantity
    }
    
    response = json.dumps(book_dictionary)
    return HttpResponse(response, mimetype="text/javascript") 

def reject_book_order(request, book_order_id):  
    book_order = BookOrder.objects.get(id=book_order_id) 

    book_order.reject_order();
    
    book_order.save()
    
    result = {}
    result['success_message'] = SUCCESS_REJECT_BOOK_ORDER   
      
    response = json.dumps(result)
    return HttpResponse(response, mimetype="text/javascript") 

def register_distributor(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    registration_result = ""
        
    if request.method == 'POST': # Formulário enviado
        form = RegisterDistributorForm(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_distributor = Distributor(name = checked_form['name'].strip())
            
            new_distributor.save()                        
            registration_result = SUCCESS_REGISTER_NEW_DISTRIBUTOR
            
            form = RegisterDistributorForm()    
            
    else: # Página acessada via link (método GET)
        form = RegisterDistributorForm()
        
    return render_to_response('bookstore/register_distributor.html', 
                              {'form': form,
                               'registration_result': registration_result,
                               'is_manager': validate_manager_session(request),
                               'is_seller': validate_seller_session(request)
                               }, 
                              context_instance=RequestContext(request))