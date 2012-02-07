# -*- encoding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session 
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session
from gilbi.apps.user_profiles.models import User
from gilbi.apps.user_profiles.forms import EditAccountForm
from gilbi.mistrael.messages.success_messages import SUCCESS_EDIT_ACCOUNT
from gilbi.mistrael.messages.warning_messages import WARNING_EDIT_ACCOUNT


def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login
        
    form = EditAccountForm()  
        
    return render_to_response('user_profiles/edit_account.html', 
                              {
                               'form': form,
                               'is_manager': validate_manager_session(request),
                               'is_seller': validate_seller_session(request)
                               }, 
                               context_instance=RequestContext(request)) 
    
def edit(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login
    
    if request.method == 'POST': # Formulário enviado
        form = EditAccountForm(request.POST, request.FILES)
        result = "" 
        
        if form.is_valid():
            checked_form = form.cleaned_data
            
            id = request.session['user_id']
        
            if User.objects.filter(id=id).exists() == True:
                user = User.objects.get(id=id)     
            
            if checked_form['login'].strip() != "":
                user.login = checked_form['login'].strip().lower()
            if checked_form['password'] != "":  
                user.set_encrypted_password(checked_form['password']) 
                      
            if checked_form['login'].strip() == "" and checked_form['password'] == "":
                result = WARNING_EDIT_ACCOUNT 
            else:
                user.save()            
                result = SUCCESS_EDIT_ACCOUNT    
        
            form = EditAccountForm()  

        return render_to_response('user_profiles/edit_account.html', 
                                  {'form': form,
                                   'result': result, 
                                   'is_manager': validate_manager_session(request),
                                   'is_seller': validate_seller_session(request)}, 
                                   context_instance=RequestContext(request))
            
    return HttpResponseRedirect('/perfil/') #se o método nao for POST        

def exclude(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 

    if request.method == 'POST': 
           
        id = request.session['user_id']
    
        if User.objects.filter(id=id).exists() == True:
            user = User.objects.get(id=id)   
                                    
            user.disable_account()
            
            for book in user.favorite_books.all():
                book.delete()
                            
            user.save() 

            return HttpResponseRedirect('/logout/') 
    
    else: #método GET   
        return HttpResponseRedirect('/perfil/')      