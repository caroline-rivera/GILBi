# encoding: utf-8

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from books.models.author import Author
from books.models.publisher import Publisher
from books.models.book import Book
from books.models.book_author import BookAuthor
from books.forms.register_author import RegisterAuthorForm
from books.forms.register_publisher import RegisterPublisherForm
from books.forms.register_book import RegisterBookForm
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_NEW_AUTHOR, SUCCESS_REGISTER_NEW_PUBLISHER, SUCCESS_REGISTER_NEW_BOOK
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session


def register_author(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
        
    registration_result = ""
         
    if request.method == 'POST': # Formulário enviado
        form = RegisterAuthorForm(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_author = Author(name = checked_form['name'])
            
            new_author.save()                        
            registration_result = SUCCESS_REGISTER_NEW_AUTHOR
            
            form = RegisterAuthorForm()    
            
    else: # Página acessada via link (método GET)
        form = RegisterAuthorForm()
        
    return render_to_response('books/register_author.html', 
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
        form = RegisterPublisherForm(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_publisher = Publisher(name = checked_form['name'])
            
            new_publisher.save()                        
            registration_result = SUCCESS_REGISTER_NEW_PUBLISHER
            
            form = RegisterPublisherForm()    
            
    else: # Página acessada via link (método GET)
        form = RegisterPublisherForm()
        
    return render_to_response('books/register_publisher.html', 
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
        form = RegisterBookForm(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data    

            new_book = Book(name = checked_form['name'],
                            photo = checked_form['photo'],
                            description = checked_form['description'],
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
                                      
            registration_result = SUCCESS_REGISTER_NEW_BOOK            
            form = RegisterBookForm()   
    
    else: # Página acessada via link (método GET)
        form = RegisterBookForm()
         
    return render_to_response('books/register_book.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))