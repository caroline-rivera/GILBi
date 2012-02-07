# -*- encoding: utf-8 -*-

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session
from gilbi.mistrael.messages.success_messages import SUCCESS_LIBRARY_REGISTER
from gilbi.apps.user_profiles.models import User
from gilbi.apps.library.models import Address, Phone, LibraryBook, Loan
from gilbi.apps.library.forms import LibraryRegisterForm
from gilbi.apps.library.grid_formats import UserLoanGridFormat, LibraryBookGridFormat


def index(request):  
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')

    id = request.session['user_id']

    user = None   
    if User.objects.filter(id=id).exists() == True:
        user = User.objects.get(id=id)
    
    result = ""

    if request.method == 'POST': # Formulário enviado    
        form = LibraryRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            checked_form = form.cleaned_data  
            street = checked_form['street']
            number = checked_form['number']
            complement = checked_form['complement']
            zipcode = checked_form['zipcode']
            neighborhood =  checked_form['neighborhood']
    
            if len(user.address.all()) == 0:          
                address = Address(user = user,
                                  street = street,
                                  number = number,
                                  complement = complement,
                                  zipcode = zipcode,
                                  neighborhood = neighborhood)
            else:
                address = user.address.all()[0]
                address.set_data(street, number, complement, zipcode,neighborhood)

            registered_phones = Phone.objects.filter(user = user.id)
            for phone in registered_phones:
                phone.delete()
                
            register_phone(user, checked_form['ddd1'], checked_form['phone1'])
            register_phone(user, checked_form['ddd2'], checked_form['phone2'])
            register_phone(user, checked_form['ddd3'], checked_form['phone3'])
            register_phone(user, checked_form['ddd4'], checked_form['phone4'])
            
            address.save()                         
                
            result = SUCCESS_LIBRARY_REGISTER
            
    else: #método GET   
   
        form = LibraryRegisterForm(instance=user)      
    
    return render_to_response('library/library.html', 
                              {'form': form,
                               'result': result,
                               'is_manager': validate_manager_session(request),
                               'is_seller': validate_seller_session(request)
                               }, 
                              context_instance=RequestContext(request))
 
def search_books(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    
    if request.method == 'POST':
        return HttpResponseRedirect('/biblioteca/') 
    
    elif 'name' in request.GET and 'author' in request.GET and 'publisher' in request.GET:
        book_name = request.GET['name']
        author_name = request.GET['author']  
        publisher_name = request.GET['publisher']  
        
        all_books = []
        books = []
        
        #teste
        library_books = LibraryBook.objects.all()
        
        if(book_name != ""):
            for book in library_books:
                if book.book.name.upper().find( book_name.upper()) != -1:
                    all_books.append(book)
        else:
            all_books = library_books
          
        if(author_name != ""):
            for book in all_books:
                authors = book.book.authors.all()
                for author in authors:
                    if author.name.upper().find( author_name.upper()) != -1:
                        if not (book in books):
                            books.append(book)
                    
        if(publisher_name != ""):
            for book in all_books:
                if book.book.publisher.name.upper().find( publisher_name.upper()) != -1:
                    if not (book in books):
                        books.append(book)
                    
        if (book_name == "") and (author_name == "") and (publisher_name == ""):
            books = library_books
        elif (author_name == "") and (publisher_name == ""):
            for book in all_books:
                books.append(book) 
                
        grid_books = transform_to_grid_book_list(books)    

        response = serializers.serialize("json",  grid_books)     
        return HttpResponse(response, mimetype="text/javascript")
    
    else:
        return HttpResponseRedirect('/biblioteca/') 
   
def list_loans(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
  
    if request.method == 'GET':              
        user_id = request.session['user_id']    
            
        user = User.objects.get(id=user_id)  
        
        loans = Loan.objects.filter(user=user)
              
        user_loans = transform_to_grid_loan_list(loans)    

        response = serializers.serialize("json",  user_loans)     
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/biblioteca/')

def transform_to_grid_book_list(books):
    grid_list = []
    for book in books:
        book_grid_format = LibraryBookGridFormat(book)   
        grid_list.append(book_grid_format)
    return grid_list

def transform_to_grid_loan_list(loans):
    grid_list = []
    for loan in loans:
        loan_grid_format = UserLoanGridFormat(loan)   
        grid_list.append(loan_grid_format)
    return grid_list

def register_phone(user, ddd, number):
    if ddd != "" and number != "":
        phone = Phone(user= user,
                      ddd = ddd,
                      number = number)
        phone.save()