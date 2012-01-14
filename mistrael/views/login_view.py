# -*- encoding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.messages.error_messages import *
from gilbi.mistrael.helpers.password_helper import compare_passwords
from gilbi.mistrael.helpers.session_helper import create_session
from gilbi.mistrael.helpers.session_helper import destroy_session

def login(request):  
    c = {}
    c.update(csrf(request)) 
       
    if request.method == 'POST': # Formulário enviado
        provided_login = request.POST['login']   
        provided_password = request.POST['password']
        registered_user = None
        
        if User.objects.filter(login=provided_login).exists() == True:
            registered_user = User.objects.get(login=provided_login)  
        if(provided_login == "" or provided_password == ""):
            c['error'] = ERROR_MANDATORY_FIELDS
        elif registered_user is None:
            c['error'] = ERROR_LOGIN_NOT_REGISTERED
        elif registered_user.member_since is None:
            c['error'] = ERROR_INACTIVE_ACCOUNT
        elif compare_passwords(provided_password, registered_user.password) == False:
            c['error'] = ERROR_INVALID_PASSWORD
        else: #sucesso na validação
            create_session(request, registered_user.id)
            return HttpResponseRedirect('perfil/')
#            context = RequestContext(request, c)        
#            template = loader.get_template('user_profile.html')
#            return HttpResponse(template.render(context)) 
            
    context = RequestContext(request, c)
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context))  

def logout(request):
    destroy_session(request)  
    return HttpResponseRedirect('/') #tela de login