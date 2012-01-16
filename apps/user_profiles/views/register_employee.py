# -*- encoding: utf-8 -*-
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session
from gilbi.apps.user_profiles.models import User, Seller, Manager
from gilbi.mistrael.messages.warning_messages import *
from gilbi.mistrael.messages.success_messages import *

def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')      
                 
    return render_to_response('user_profiles/register_employee.html', 
                              {}, 
                              context_instance=RequestContext(request))
    
def search(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/') 
    
    if request.method == 'POST':
        return HttpResponseRedirect('/gerenciarlivraria/cadastrarfuncionario/') 
    
    elif 'first_name' in request.GET and 'last_name' in request.GET and 'login' in request.GET and 'email' in request.GET:
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']  
        login = request.GET['login']  
        email = request.GET['email']  
        
        kwargs = {}
        if(first_name != ""):
            kwargs['first_name__contains'] = first_name
        if(last_name != ""):
            kwargs['last_name__contains'] = last_name
        if(login != ""):
            kwargs['login'] = login
        if(email != ""):
            kwargs['email'] = email
        
        if(kwargs != {}):
            users = User.objects.filter(**kwargs).order_by('first_name')
        else:
            users = User.objects.all().order_by('first_name')
            
        response = serializers.serialize("json",  users)     
        return HttpResponse(response, mimetype="text/javascript")
    
    else:
        return HttpResponseRedirect('/gerenciarlivraria/cadastrarfuncionario/') 

def save(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/') 
    
    if request.method == 'GET' and 'users_ids' in request.GET and 'is_manager' in request.GET:        
        str_ids = request.GET['users_ids']
        is_manager = request.GET['is_manager'] 

        result = {}
        result['warning_message'] = ""
        result['success_message'] = ""
                
        str_array_ids = str_ids.split(',')
                  
        for id in str_array_ids:
            int_id = int(id)
            if User.objects.filter(id=int_id).exists() == True: 
                user = User.objects.get(id=int_id)
                                     
                if is_manager == 'false' and Seller.objects.filter(id=int_id).exists() == True:
                    result['warning_message'] += create_message(WARNING_ALREADY_REGISTERED_SELLER,
                                                                user.login)
                    
                elif is_manager == 'true' and Manager.objects.filter(id=int_id).exists() == True:
                    result['warning_message'] += create_message(WARNING_ALREADY_REGISTERED_MANAGER,
                                                                user.login)
                                        
                elif is_manager == 'false' and Seller.objects.filter(id=int_id).exists() == False:
                    seller = Seller(user_ptr_id = user.id)
                    seller.save()
                    user.save()
                    result['success_message'] += create_message(SUCCESS_REGISTER_SELLER,
                                                                user.login)
                    
                else: #cadastrar como gerente
                    seller = Seller(user_ptr_id = user.id)
                    if Seller.objects.filter(id=user.id).exists() == True:
                        seller = Seller.objects.get(id=user.id)
                    seller.save()
                    manager = Manager(seller_ptr_id = seller.id)
                    manager.save()    
                    user.save() 
                    result['success_message'] += create_message(SUCCESS_REGISTER_MANAGER,
                                                                user.login)
                    
        response = json.dumps(result)
        return HttpResponse(response, mimetype="text/javascript")
    else:
        return HttpResponseRedirect('/gerenciarlivraria/cadastrarfuncionario/') 


def create_message(message, name_user):
    result = ""
    result += "<p>"
    result += message
    result += name_user
    result += ".</p>" 
    return result