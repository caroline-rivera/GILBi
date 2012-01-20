# encoding: utf-8

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from gilbi.apps.bookstore.forms import NewPurchaseItemForm
from gilbi.apps.bookstore.forms import NewPurchaseOrderForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_purchase_item = NewPurchaseItemForm()
        form_purchase_order = NewPurchaseOrderForm()
        
        return render_to_response('bookstore/purchase_order.html', 
                                  {'form_purchase_item': form_purchase_item,
                                   'form_purchase_order': form_purchase_order},
                                  context_instance=RequestContext(request)) 
        