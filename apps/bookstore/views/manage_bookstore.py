# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core import serializers
import json
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from gilbi.apps.books.models import Book
from gilbi.apps.bookstore.grid_formats import BookGridFormat
from gilbi.apps.bookstore.models import Distributor
from gilbi.apps.bookstore.forms import RegisterDistributorForm
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_NEW_DISTRIBUTOR
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
        template = loader.get_template('bookstore/manage_bookstore.html')
        return HttpResponse(template.render(context))
    
def get_book_json(request, book_id):
    book = Book.objects.get(id=book_id)

    # TODO: Usar o serializers e acabar com essa nojeira
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
            new_distributor = Distributor(name = checked_form['name'])
            
            new_distributor.save()                        
            registration_result = SUCCESS_REGISTER_NEW_DISTRIBUTOR
            
            form = RegisterDistributorForm()    
            
    else: # Página acessada via link (método GET)
        form = RegisterDistributorForm()
        
    return render_to_response('bookstore/register_distributor.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))