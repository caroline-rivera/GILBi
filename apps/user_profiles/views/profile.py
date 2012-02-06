# encoding: utf-8

import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.apps.user_profiles.models import User, Seller, Manager
from gilbi.apps.books.models import Book
from gilbi.apps.user_profiles.forms import EditProfileForm
from gilbi.mistrael.messages.success_messages import SUCCESS_EDIT_PROFILE
from gilbi.mistrael.messages.error_messages import ERROR_MAX_LENGTH_STATUS
from gilbi.mistrael.messages.success_messages import SUCCESS_ADD_FAVORITE_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_ADD_FAVORITE_BOOK

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
            
    return render_to_response('user_profiles/profile.html', 
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
        form = EditProfileForm(request.POST, request.FILES)
        
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
        form = EditProfileForm(instance=user)      
    
    return render_to_response('user_profiles/edit_profile.html', 
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
            return render_to_response('user_profiles/profile.html', 
                                      {'user': user,
                                       'error_msg': error_msg,
                                       'profile_phrase': profile_phrase}, 
                                      context_instance=RequestContext(request))
        else:
            user.set_profile_phrase(profile_phrase)
            user.save()
    return HttpResponseRedirect('/perfil/')