# -*- encoding: utf-8 -*-

import json
from django.core import serializers
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from gilbi.apps.library.models import Loan, Phone, LibraryBook
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session
from gilbi.apps.library.grid_formats import ManagerLoanGridFormat, LibraryBookGridFormat
from gilbi.apps.library.forms import BorrowBookForm
from gilbi.apps.library.forms import ReceiveBookForm
from gilbi.mistrael.messages.success_messages import SUCCESS_BOOK_BORROWED, SUCCESS_BOOK_RENEWED
from gilbi.mistrael.messages.success_messages import SUCCESS_BOOK_RECEIVED

def index(request):   
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_borrow = BorrowBookForm()
        form_receive = ReceiveBookForm()

        return render_to_response('library/manage_library.html', 
                                  {'form_borrow': form_borrow,
                                   'form_receive': form_receive},
                                   #'registration_result': registration_result},
                                  context_instance=RequestContext(request)) 
def borrow_book(request):
    result = {}
    result['success_message'] = ""
    result['book_id_message'] = ""
    result['user_login_message'] = ""
              
    if request.method == 'GET' and 'book1' in request.GET and 'user_login1' in request.GET: # Formulário enviado
        form_borrow = BorrowBookForm(request.GET, request.FILES)
        
        if form_borrow.is_valid():

            checked_form = form_borrow.cleaned_data
            book = checked_form['book1']
            user = User.objects.get(login=checked_form['user_login1'])

            if Loan.objects.filter(
                       user = user.id,
                       return_date__isnull = True
                       ).exists() == True:
                loan = Loan.objects.get(user = user.id, return_date__isnull = True)
                loan.renew_book()
                result['success_message'] = SUCCESS_BOOK_RENEWED + \
                                    loan.expected_return_date.strftime('%d/%m/%Y') + "."
            else:
                loan = Loan(user = user,
                            book = book,
                            loan_date = date.today(),
                            expected_return_date = date.today() + timedelta(days=15),
                            return_date = None)
                result['success_message'] = SUCCESS_BOOK_BORROWED + \
                                    loan.expected_return_date.strftime('%d/%m/%Y') + "."
            loan.save()
               
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript")     
                
    else: # Página acessada via link 
        return HttpResponseRedirect('/gerenciarbiblioteca/')
    
    if form_borrow._errors and 'book1' in form_borrow._errors:
        result['book_id_message'] = form_borrow._errors['book1'][0]
        
    if form_borrow._errors and 'user_login1' in form_borrow._errors:
        result['user_login_message'] = form_borrow._errors['user_login1'][0]
        
    response = json.dumps(result)
    return HttpResponse(response, mimetype="text/javascript")   

def receive_book(request):    
    result = {}
    result['success_message'] = ""
    result['book_id_message'] = ""
    result['user_login_message'] = ""
       
    if request.method == 'GET' and 'book2' in request.GET and 'user_login2' in request.GET: # Formulário enviado
        form_receive = ReceiveBookForm(request.GET, request.FILES)
        
        if form_receive.is_valid():

            checked_form = form_receive.cleaned_data
            book = checked_form['book2']
            user = User.objects.get(login=checked_form['user_login2'])

            if Loan.objects.filter(book = book.id,
                                   user = user.id,
                                   return_date__isnull = True
                                   ).exists() == True:
                loan = Loan.objects.get(book = book.id, user = user.id, return_date__isnull = True)
                loan.receive_book()

            loan.save()
            result['success_message'] = SUCCESS_BOOK_RECEIVED
               
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript")     
            
    else: # Página acessada via link 
        return HttpResponseRedirect('/gerenciarbiblioteca/')
        
    if form_receive._errors and 'book2' in form_receive._errors:
        result['book_id_message'] = form_receive._errors['book2'][0]
        
    if form_receive._errors and 'user_login2' in form_receive._errors:
        result['user_login_message'] = form_receive._errors['user_login2'][0]
        
    response = json.dumps(result)
    return HttpResponse(response, mimetype="text/javascript")  


def list_loans(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        if request.method == 'GET':                        
            loans = Loan.objects.all().order_by('-loan_date')
                  
            grid_loans = transform_to_grid_loan_list(loans)    
    
            response = serializers.serialize("json",  grid_loans)     
            return HttpResponse(response, mimetype="text/javascript")
        else:
            return HttpResponseRedirect('/gerenciarbiblioteca/')

def show_book_informations(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    elif request.method == 'GET' and 'book_id' in request.GET:   
        str_id = request.GET['book_id'] 
        
        book_list = []
        if(str_id != ""):                     
            book_id = int(str_id)            
            library_book = LibraryBook.objects.get(id=book_id)
            book = LibraryBookGridFormat(library_book)            
            book_list.append(book)
               
        response = serializers.serialize("json", book_list)     
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/gerenciarbiblioteca/')        
        
        
                    
def show_user_informations(request, id):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        user = User.objects.get(id=id)
        phones = Phone.objects.filter(user = user.id)

        information = {}   
        str_phones = []
             
        for phone in phones:
            str_phones.append("( " + phone.ddd + " ) " + phone.number)
            
        information['name'] = user.first_name + " " + user.last_name
        information['login'] = user.login
        information['email'] = user.email
        information['phones'] = str_phones
        if len(user.address.all()) == 0:
            information['address'] = ""
        else:
            address = user.address.all()[0]
            information['address'] = address.street + " " + address.number + " " + \
            address.complement + " - " + address.neighborhood + " - CEP: " + \
            address.zipcode
        
        return render_to_response('library/show_user_informations.html', 
                                  {'information': information},
                                  context_instance=RequestContext(request))   
        
def transform_to_grid_loan_list(loans):
    grid_list = []
    for loan in loans:
        loan_grid_format = ManagerLoanGridFormat(loan)   
        grid_list.append(loan_grid_format)
    return grid_list