# encoding: utf-8

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.apps.books.models import Author, Publisher, Book, BookAuthor
from gilbi.apps.books.forms import RegisterAuthorForm, RegisterPublisherForm, RegisterBookForm
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_NEW_AUTHOR, SUCCESS_REGISTER_NEW_PUBLISHER, SUCCESS_REGISTER_NEW_BOOK
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_AUTHOR_NAME, ERROR_REQUIRED_PUBLISHER_NAME, ERROR_REQUIRED_BOOK_NAME


def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_author = RegisterAuthorForm() 
        form_publisher = RegisterPublisherForm() 
        form_book = RegisterBookForm() 
        return render_to_response('books/books_collection.html', 
                                  {
                                   'form_book':form_book,
                                   'form_author': form_author,
                                   'form_publisher':form_publisher
                                   }, 
                                  context_instance=RequestContext(request)) 
            
def register_author(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    result = {}
    result['success_message'] = ""
    result['error_message'] = ""
    result['validation_message'] = []  
         
    if request.method == 'GET' and 'author_name' in request.GET:
        form = RegisterAuthorForm(request.GET, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_author = Author(name = checked_form['author_name'].strip())
            
            new_author.save()           
            result['success_message'] = SUCCESS_REGISTER_NEW_AUTHOR
                    
        else:                              
            if form._errors and 'author_name' in form._errors:
                if form._errors['author_name'][0] == ERROR_REQUIRED_AUTHOR_NAME:
                    result['validation_message'].append(form._errors['author_name'][0])
                else:
                    result['error_message'] = form._errors['author_name'][0]
       
        response = json.dumps(result)                
        return HttpResponse(response, mimetype="text/javascript") 
    else:
        return HttpResponseRedirect('/acervo/') 

       
def register_publisher(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    result = {}
    result['success_message'] = ""
    result['error_message'] = ""
    result['validation_message'] = []  
         
    if request.method == 'GET' and 'publisher_name' in request.GET:
        form = RegisterPublisherForm(request.GET, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_publisher = Publisher(name = checked_form['publisher_name'].strip())
            
            new_publisher.save()           
            result['success_message'] = SUCCESS_REGISTER_NEW_PUBLISHER
                    
        else:                              
            if form._errors and 'publisher_name' in form._errors:
                if form._errors['publisher_name'][0] == ERROR_REQUIRED_PUBLISHER_NAME:
                    result['validation_message'].append(form._errors['publisher_name'][0])
                else:
                    result['error_message'] = form._errors['publisher_name'][0]
       
        response = json.dumps(result)                
        return HttpResponse(response, mimetype="text/javascript") 
    else:
        return HttpResponseRedirect('/acervo/') 
    
    
def register_book(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    result = {}
    result['success_message'] = ""
    result['error_message'] = ""
    result['validation_message'] = []  
     
    if request.method == 'GET' and 'name' in request.GET and \
                                   'photo' in request.GET and \
                                   'description' in request.GET and \
                                   'publisher' in request.GET:    
    
        form = RegisterBookForm(request.GET, request.FILES)
        import pdb
        pdb.set_trace()        
        if form.is_valid():
            checked_form = form.cleaned_data    
 
            new_book = Book(name = checked_form['name'].strip(),
                            photo = checked_form['photo'],
                            description = checked_form['description'].strip(),
                            publisher = checked_form['publisher']
                            )               
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

            result['success_message'] = SUCCESS_REGISTER_NEW_BOOK           
    
        else:                             
            if form._errors and 'name' in form._errors:
                if form._errors['name'][0] == ERROR_REQUIRED_BOOK_NAME:
                    result['validation_message'].append(form._errors['name'][0])
                else:
                    result['error_message'] = form._errors['name'][0]

            if form._errors and 'publisher' in form._errors:
                result['validation_message'].append(form._errors['publisher'][0])
                                                
            if form._errors and 'author' in form._errors:
                result['validation_message'].append(form._errors['author'][0])
                                
            if form._errors and 'spiritual_author' in form._errors:
                result['validation_message'].append(form._errors['spiritual_author'][0])
                       
        response = json.dumps(result)                
        return HttpResponse(response, mimetype="text/javascript") 
    else:
        return HttpResponseRedirect('/acervo/') 
    
    
#def register_author(request):
#    if validate_session(request) == False:
#        return HttpResponseRedirect('/logout/')
#    if validate_manager_session(request) == False:
#        return HttpResponseRedirect('/perfil/')
#        
#    registration_result = ""
#         
#    if request.method == 'POST': # Formulário enviado
#        form = RegisterAuthorForm(request.POST, request.FILES)
#        
#        if form.is_valid():
#            checked_form = form.cleaned_data            
#            new_author = Author(name = checked_form['name'])
#            
#            new_author.save()                        
#            registration_result = SUCCESS_REGISTER_NEW_AUTHOR
#            
#            form = RegisterAuthorForm()    
#            
#    else: # Página acessada via link (método GET)
#        form = RegisterAuthorForm()
#        
#    return render_to_response('books/register_author.html', 
#                              {'form': form,
#                               'registration_result': registration_result}, 
#                              context_instance=RequestContext(request))
#
#def register_publisher(request):
#    if validate_session(request) == False:
#        return HttpResponseRedirect('/logout/')
#    if validate_manager_session(request) == False:
#        return HttpResponseRedirect('/perfil/')
#       
#    registration_result = ""
#    
#    if request.method == 'POST': # Formulário enviado
#        form = RegisterPublisherForm(request.POST, request.FILES)
#        
#        if form.is_valid():
#            checked_form = form.cleaned_data            
#            new_publisher = Publisher(name = checked_form['name'])
#            
#            new_publisher.save()                        
#            registration_result = SUCCESS_REGISTER_NEW_PUBLISHER
#            
#            form = RegisterPublisherForm()    
#            
#    else: # Página acessada via link (método GET)
#        form = RegisterPublisherForm()
#        
#    return render_to_response('books/register_publisher.html', 
#                              {'form': form,
#                               'registration_result': registration_result}, 
#                              context_instance=RequestContext(request))
#    
#def register_book(request):
#    if validate_session(request) == False:
#        return HttpResponseRedirect('/logout/')
#    if validate_manager_session(request) == False:
#        return HttpResponseRedirect('/perfil/')
#    
#    registration_result = ""
#        
#    if request.method == 'POST': # Formulário enviado
#        import pdb
#        pdb.set_trace()
#        form = RegisterBookForm(request.POST, request.FILES)
#        
#        if form.is_valid():
#            checked_form = form.cleaned_data    
#
#            new_book = Book(name = checked_form['name'],
#                            photo = checked_form['photo'],
#                            description = checked_form['description'],
#                            publisher = checked_form['publisher']
#                            )               
#            new_book.save()      
#
#            for author in checked_form['author']:
#                new_author = BookAuthor(author = author,
#                                        book = new_book,
#                                        category = 'F')
#                new_author.save()
# 
#            for author in checked_form['spiritual_author']:
#                new_author = BookAuthor(author = author,
#                                        book = new_book,
#                                        category = 'E')
#                new_author.save()
#                                      
#            registration_result = SUCCESS_REGISTER_NEW_BOOK            
#            form = RegisterBookForm()   
#    
#    else: # Página acessada via link (método GET)
#        form = RegisterBookForm()
#         
#    return render_to_response('books/register_book.html', 
#                              {'form': form,
#                               'registration_result': registration_result}, 
#                              context_instance=RequestContext(request))