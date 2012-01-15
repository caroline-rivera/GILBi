# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from gilbi.apps.bookstore.models import Distributor
from gilbi.mistrael.forms.register_distributor_form import FormRegisterDistributor
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
        template = loader.get_template('manager_bookstore.html')
        return HttpResponse(template.render(context)) 
    
def register_distributor(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    registration_result = ""
        
    if request.method == 'POST': # Formulário enviado
        form = FormRegisterDistributor(request.POST, request.FILES)
        
        if form.is_valid():
            checked_form = form.cleaned_data            
            new_distributor = Distributor(name = checked_form['name'])
            
            new_distributor.save()                        
            registration_result = SUCCESS_REGISTER_NEW_DISTRIBUTOR
            
            form = FormRegisterDistributor()    
            
    else: # Página acessada via link (método GET)
        form = FormRegisterDistributor()
        
    return render_to_response('register_distributor.html', 
                              {'form': form,
                               'registration_result': registration_result}, 
                              context_instance=RequestContext(request))