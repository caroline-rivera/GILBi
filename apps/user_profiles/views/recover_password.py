# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from gilbi.apps.user_profiles.forms import RecoverPasswordForm, ChangePasswordForm
from gilbi.mistrael.messages.email_messages import TITLE_RECOVER_PASSWORD
from gilbi.mistrael.messages.error_messages import *
from gilbi.mistrael.messages.success_messages import *
from gilbi.mistrael.helpers.email_helper import send_email, create_change_password_email
from gilbi.mistrael.helpers.encryption_helper import encrypt_login_email
from gilbi.apps.user_profiles.models import User

def recover(request):
    if request.method == 'POST': # Formulário enviado
        form = RecoverPasswordForm(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data
    
            user = User.objects.get(email=checked_form['email'])
        
            message = create_change_password_email(user.login, user.email, user.id)
            if (send_email(TITLE_RECOVER_PASSWORD, 
                           message, 
                           user.email) == False):
                result_operation = ERROR_SENDING_RECOVER_PASSWORD_EMAIL
            else:
                result_operation = SUCCESS_RECOVER_PASSWORD
            return render_to_response('user_profiles/recover_password.html', 
                                      {'form': form, 'result_operation': result_operation},
                                      context_instance=RequestContext(request))  
            

    else: # Página acessada via link (método GET)
        form = RecoverPasswordForm()
        
    return render_to_response('user_profiles/recover_password.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))
    
def change_password(request, id, code):
    result = ""
    
    if request.method == 'POST': # Formulário enviado     
        form = ChangePasswordForm(request.POST, request.FILES)
                
        if form.is_valid():
            checked_form = form.cleaned_data
    
            user = User.objects.get(id=id)
            user.set_encrypted_password(checked_form['new_password'])
            user.save()
            
            result = SUCCESS_CHANGE_PASSWORD
            
    else: # Página acessada via link (método GET)
        user = None    
        if User.objects.filter(id=id).exists() == True:
            user = User.objects.get(id=id)         

        if user is None:
            result = ERROR_USER_NOT_REGISTERED
        elif user.member_since is None:
            result = ERROR_INACTIVE_ACCOUNT
        elif code != encrypt_login_email(user.login, user.email):
            result = ERROR_INVALID_URL          
        else:
            pass
        form = ChangePasswordForm()  
            
    return render_to_response('user_profiles/change_password.html', 
                              {'form': form, 'result': result}, 
                              context_instance=RequestContext(request))   
            