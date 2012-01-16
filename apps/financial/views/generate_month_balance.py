# encoding: utf-8

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.apps.financial.forms import GenerateMonthBalanceForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session


def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form = GenerateMonthBalanceForm()
            
        return render_to_response('financial/generate_month_balance.html', 
                                  {'form': form}, 
                                  context_instance=RequestContext(request))
    
def generate(request):
    result = {}
    result['warning_message'] = ""
    result['error_message'] = ""
    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        if request.method == 'GET' and 'month_value' in request.GET and 'year_value' in request.GET:
            form = GenerateMonthBalanceForm(request.GET, request.FILES)
            
            if form.is_valid():
                checked_form = form.cleaned_data
                
            response = json.dumps(result)
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 