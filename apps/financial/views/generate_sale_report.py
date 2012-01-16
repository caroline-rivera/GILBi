# encoding: utf-8

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gilbi.apps.financial.forms import GenerateSaleReportForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session


def index(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')

    form = GenerateSaleReportForm()
        
    return render_to_response('financial/generate_sale_report.html', 
                              {'form': form}, 
                              context_instance=RequestContext(request))