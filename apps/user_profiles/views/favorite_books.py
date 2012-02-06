# encoding: utf-8

import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.apps.user_profiles.models import User
from gilbi.apps.books.models import Book
from gilbi.mistrael.messages.success_messages import SUCCESS_ADD_FAVORITE_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_ADD_FAVORITE_BOOK

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
               
    return render_to_response('user_profiles/favorite_books.html', 
                              {},
                              context_instance=RequestContext(request))

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
        return HttpResponseRedirect('/perfil/') 
    
    
def remove_favorite_book(request, id):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    
    if request.method == 'GET': 

        user_id = request.session['user_id']          
        if User.objects.filter(id=user_id).exists() == True and Book.objects.filter(id=id).exists() == True:
            user = User.objects.get(id=user_id)    
            book = Book.objects.get(id=id)
            user.favorite_books.remove(book)
            
            response = serializers.serialize("json",  {})     
            return HttpResponse(response, mimetype="text/javascript")      
      
    return HttpResponseRedirect('/perfil/')