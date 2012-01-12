# -*- encoding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.models.user import User
from gilbi.mistrael.forms.edit_account_form import FormEditAccount
from gilbi.mistrael.messages.success_messages import SUCCESS_EDIT_ACCOUNT, SUCCESS_EXCLUDE_ACCOUNT
from gilbi.mistrael.messages.warning_messages import WARNING_EDIT_ACCOUNT

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login
        
    form = FormEditAccount()  
        
    return render_to_response('edit_account.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request)) 
    
def edit(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login
    
    if request.method == 'POST': # Formulário enviado
        form = FormEditAccount(request.POST, request.FILES)
        result = "" 
        
        if form.is_valid():
            checked_form = form.cleaned_data
            
            id = request.session['user_id']
        
            if User.objects.filter(id=id).exists() == True:
                user = User.objects.get(id=id)     
            
            if checked_form['login'] != "":
                user.login = checked_form['login']
            if checked_form['password'] != "":  
                user.set_encrypted_password(checked_form['password']) 
                      
            if checked_form['login'] == "" and checked_form['password'] == "":
                result = WARNING_EDIT_ACCOUNT 
            else:
                user.save()            
                result = SUCCESS_EDIT_ACCOUNT    
        
            form = FormEditAccount()  

        return render_to_response('edit_account.html', 
                                  {'form': form,
                                   'result': result}, 
                                  context_instance=RequestContext(request))
            
    return HttpResponseRedirect('/perfil/') #se o método nao for POST        

def exclude(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') #tela de login

    if request.method == 'POST': # Formulário enviado
           
        id = request.session['user_id']
    
        if User.objects.filter(id=id).exists() == True:
            user = User.objects.get(id=id)   
            user.delete() 
            # TO DO: colocar todos os deletes 
        return HttpResponseRedirect('/logout/') 
    
    else: #método GET   
        return HttpResponseRedirect('/perfil/')      