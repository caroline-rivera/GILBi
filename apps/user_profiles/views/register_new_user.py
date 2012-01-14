# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.forms.register_new_user_form import FormRegisterNewUser
from gilbi.mistrael.messages.email_messages import *
from gilbi.mistrael.messages.error_messages import *
from gilbi.mistrael.messages.success_messages import *
from gilbi.mistrael.helpers.email_helper import send_email, create_confirmation_email, encrypt_login_email
from datetime import date
    
def register(request):
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterNewUser(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data
            new_user = User(first_name = checked_form['first_name'],
                            last_name = checked_form['last_name'],
                            login = checked_form['login'],
                            email = checked_form['email'],
                            password = checked_form['password'],
                            gender = checked_form['gender']) 
            new_user.set_encrypted_password(checked_form['password'])
            new_user.set_default_avatar()
            
            new_user.save()
                        
            message = create_confirmation_email(new_user.login, new_user.email, new_user.id)
            if (send_email(TITLE_CONFIRM_REGISTRATION, message, new_user.email) == False):
                registration_result = ERROR_SENDING_REGISTER_EMAIL
                new_user.delete()
            else:
                registration_result = SUCCESS_REGISTER_NEW_USER
               
            return render_to_response('register_new_user.html', 
                                      {'form': form,
                                       'registration_result': registration_result},
                                      context_instance=RequestContext(request))
            
    else: # Página acessada via link (método GET)
        form = FormRegisterNewUser()
        
    return render_to_response('register_new_user.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
    
def activate_account(request, id, code):
    registered_user = None
    
    if User.objects.filter(id=id).exists() == True:
        registered_user = User.objects.get(id=id) 

    if registered_user is None:
        registration_result = ERROR_USER_NOT_REGISTERED
    elif registered_user.member_since is not None:
        registration_result = ERROR_ALREADY_ACTIVE_ACCOUNT
    elif code != encrypt_login_email(registered_user.login, registered_user.email):
        registration_result = ERROR_INVALID_URL          
    else:
        registered_user.member_since = date.today()
        registered_user.save()
        registration_result = SUCCESS_ACTIVATE_ACCOUNT
        
    #TO DO
    #return HttpResponseRedirect('/') #tela de login
        
    return render_to_response('login.html', 
                              {'registration_result': registration_result}, 
                              context_instance=RequestContext(request))

def disable_account(request, id, code):
    registered_user = None
    
    if User.objects.filter(id=id).exists() == True:
        registered_user = User.objects.get(id=id)  
     
    if registered_user is None:
        registration_result = ERROR_USER_NOT_REGISTERED
    elif registered_user.member_since is not None:
        registration_result = ERROR_ALREADY_ACTIVE_ACCOUNT
    elif code != encrypt_login_email(registered_user.login, registered_user.email):
        registration_result = ERROR_INVALID_URL          
    else:
        registered_user.delete()
        registration_result = SUCCESS_DISABLE_ACCOUNT

    #TODO
    #return HttpResponseRedirect('/') #tela de login
            
    return render_to_response('login.html', 
                              {'registration_result': registration_result}, 
                              context_instance=RequestContext(request))
