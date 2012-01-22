# encoding: utf-8

import json
from decimal import *
from datetime import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from gilbi.apps.books.models import Book
from gilbi.apps.bookstore.models import BookstoreBook
from gilbi.apps.bookstore.forms import RegisterBookstoreBookForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_BOOKSTORE_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOKSTORE_BOOK
from django.db import IntegrityError

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_bookstore_book = RegisterBookstoreBookForm()
        return render_to_response('bookstore/register_bookstore_book.html', 
                                  {'form_bookstore_book': form_bookstore_book},
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
              
        if request.method == 'GET' and 'book' in request.GET and \
                                       'price' in request.GET and \
                                       'total_quantity' in request.GET and \
                                       'available_quantity' in request.GET :
            
            form = RegisterBookstoreBookForm(request.GET, request.FILES)

            if form.is_valid():
                checked_form = form.cleaned_data
                book = checked_form['book']  
                price = checked_form['price']  
                total_quantity = checked_form['total_quantity']  
                available_quantity = checked_form['available_quantity']

                bookstore_book = BookstoreBook(id = book.id,
                                               total_quantity = total_quantity,
                                               available_quantity = available_quantity,
                                               suggested_price = Decimal(price),
                                               name = book.name,
                                               photo = book.photo,
                                               description = book.description,
                                               publisher = book.publisher, 
                                               )

                bookstore_book.save()
                             
                result['success_message'] = SUCCESS_REGISTER_BOOKSTORE_BOOK
                    
            else:                                 
                if form._errors and 'book' in form._errors:
                    if form._errors['book'][0] == ERROR_REQUIRED_BOOKSTORE_BOOK:
                        result['validation_message'].append(form._errors['book'][0])
                    else:
                        result['error_message'] = form._errors['book'][0]
                        
                if form._errors and 'price' in form._errors:
                    result['validation_message'].append(form._errors['price'][0]) 

                if form._errors and 'total_quantity' in form._errors:
                    result['validation_message'].append(form._errors['total_quantity'][0])  
                    
                if form._errors and 'available_quantity' in form._errors:
                    result['validation_message'].append(form._errors['available_quantity'][0]) 
                          
            response = json.dumps(result)   
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 