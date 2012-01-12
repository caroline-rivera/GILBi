# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from gilbi.mistrael.models.author import Author
from gilbi.mistrael.models.publisher import Publisher
from gilbi.mistrael.models.distributor import Distributor
from gilbi.mistrael.models.book import Book
from gilbi.mistrael.models.book import BookAuthor
from gilbi.mistrael.models.bookstore_book import BookstoreBook
from gilbi.mistrael.forms.register_author_form import FormRegisterAuthor
from gilbi.mistrael.forms.register_publisher_form import FormRegisterPublisher
from gilbi.mistrael.forms.register_distributor_form import FormRegisterDistributor
from gilbi.mistrael.forms.register_book_form import FormRegisterBook
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_NEW_AUTHOR, SUCCESS_REGISTER_NEW_PUBLISHER, SUCCESS_REGISTER_NEW_DISTRIBUTOR, SUCCESS_REGISTER_NEW_BOOK
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session

def index(request):
    c = {}
    c.update(csrf(request))            
    context = RequestContext(request, c)
    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        template = loader.get_template('manager_bookstore.html')
        return HttpResponse(template.render(context)) 

def register_author(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
        
    registration_result = ""
         
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterAuthor(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_author = Author(name = checked_form['name'])
            
            new_author.save()                        
            registration_result = SUCCESS_REGISTER_NEW_AUTHOR
            
            form = FormRegisterAuthor()    
            
    else: # Página acessada via link (método GET)
        form = FormRegisterAuthor()
        
    return render_to_response('register_author.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))

def register_publisher(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
       
    registration_result = ""
    
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterPublisher(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_publisher = Publisher(name = checked_form['name'])
            
            new_publisher.save()                        
            registration_result = SUCCESS_REGISTER_NEW_PUBLISHER
            
            form = FormRegisterPublisher()    
            
    else: # Página acessada via link (método GET)
        form = FormRegisterAuthor()
        
    return render_to_response('register_publisher.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))
    
def register_distributor(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    registration_result = ""
        
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterDistributor(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_distributor = Distributor(name = checked_form['name'])
            
            new_distributor.save()                        
            registration_result = SUCCESS_REGISTER_NEW_DISTRIBUTOR
            
            form = FormRegisterAuthor()    
            
    else: # Página acessada via link (método GET)
        form = FormRegisterDistributor()
        
    return render_to_response('register_distributor.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))
    
def register_book(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    registration_result = ""
        
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterBook(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data    

            new_book = BookstoreBook(name = checked_form['name'],
                                     photo = checked_form['photo'],
                                     description = checked_form['description'],
                                     publisher = checked_form['publisher'],
                                     total_quantity = 0,
                                     avaiable_quantity = 0)               
            new_book.save()      

            for author in checked_form['author']:
                new_author = BookAuthor(author = author,
                                        book = new_book,
                                        category = 'F')
                new_author.save()
 
            for author in checked_form['spiritual_author']:
                new_author = BookAuthor(author = author,
                                        book = new_book,
                                        category = 'E')
                new_author.save()
                                      
            registration_result = SUCCESS_REGISTER_NEW_BOOK            
            form = FormRegisterBook()   
    
    else: # Página acessada via link (método GET)
        form = FormRegisterBook()
         
    return render_to_response('register_book.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))