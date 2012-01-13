# -*- encoding: utf-8 -*-
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.models.user import User
from gilbi.mistrael.models.seller import Seller
from gilbi.mistrael.models.manager import Manager
from gilbi.books.models.book import Book
from gilbi.mistrael.forms.edit_profile_form import FormEditProfile
from gilbi.mistrael.messages.success_messages import SUCCESS_EDIT_PROFILE
from gilbi.mistrael.messages.error_messages import ERROR_MAX_LENGTH_STATUS
from gilbi.mistrael.helpers.constants import FEMALE_IMG_PATH, MALE_IMG_PATH

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/') #tela de login
    
    id = request.session['user_id']
    
    user = None
    
    if User.objects.filter(id=id).exists() == True:
        user = User.objects.get(id=id)     
            
    favorite_books = user.favorite_books.all()
    
#    if Seller.objects.filter(id=user.id).exists() == True:
#        seller = True;
#    else:
#        seller = False;
#
#    if Manager.objects.filter(id=user.id).exists() == True:
#        manager = True;
#    else:
#        manager = False;
            
    return render_to_response('profile.html', 
                              {'user': user,
                               'favorite_books': favorite_books},
                               #'manager': manager,
                               #'seller': seller}, 
                              context_instance=RequestContext(request))
    
def edit(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login

    id = request.session['user_id']

    user = None    
    if User.objects.filter(id=id).exists() == True:
        user = User.objects.get(id=id)
    
    result = ""
           
    if request.method == 'POST': # Formulário enviado    
        form = FormEditProfile(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data
            
            data = {}
            data['first_name'] = checked_form['first_name']
            data['last_name'] = checked_form['last_name']
            data['photo'] = checked_form['photo']
            data['institution'] = checked_form['institution']
            data['gender'] = checked_form['gender']
            data['birthday'] = checked_form['birthday']
            
            user.set_profile_data(data)          
            user.save()
            result = SUCCESS_EDIT_PROFILE
            
    else: #método GET          
        form = FormEditProfile(instance=user)      
    
    return render_to_response('edit_profile.html', 
                              {'form': form,
                               'result': result}, 
                              context_instance=RequestContext(request))
    
def change_status(request):   
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    
    if request.method == 'POST': 
        
        user = None   
        id = request.session['user_id']          
        if User.objects.filter(id=id).exists() == True:
                user = User.objects.get(id=id)
                       
        profile_phrase = request.POST['description'] 
               
        if len(profile_phrase) > 100:
            error_msg = ERROR_MAX_LENGTH_STATUS
            return render_to_response('profile.html', 
                                      {'user': user,
                                       'error_msg': error_msg,
                                       'profile_phrase': profile_phrase}, 
                                      context_instance=RequestContext(request))
        else:
            user.set_profile_phrase(profile_phrase)
            user.save()
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