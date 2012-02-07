# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json
from django.shortcuts import render_to_response
from gilbi.apps.financial.models import Payment
from gilbi.apps.financial.models import Duplicate
from gilbi.apps.financial.forms import RegisterPaymentForm
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session, validate_seller_session
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_DUPLICATE
from gilbi.mistrael.messages.success_messages import SUCCESS_REGISTER_PAYMENT

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_payment = RegisterPaymentForm()
        return render_to_response('financial/register_payment.html', 
                                  {
                                   'form_payment': form_payment,
                                   'is_manager': validate_manager_session(request),
                                   'is_seller': validate_seller_session(request) 
                                   },
                                  context_instance=RequestContext(request)) 
        
def register(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/')
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        result = {}
        result['success_message'] = ""
        result['error_message'] = ""
        result['validation_message'] = []      
              
        if request.method == 'GET' and 'invoice' in request.GET and \
                                       'duplicate' in request.GET and \
                                       'payment_date' in request.GET:
         
            form = RegisterPaymentForm(request.GET, request.FILES)

            if form.is_valid():
                checked_form = form.cleaned_data
                form_duplicate = checked_form['duplicate']  
                form_date = checked_form['payment_date']                
               
                payment = Payment(payment_date = form_date)
                payment.save()
                
                payment = Payment.objects.order_by('-id')[0]
                duplicate = Duplicate.objects.get(id=form_duplicate.id)
                duplicate.set_payment(payment)
                duplicate.save()
                
                result['success_message'] = SUCCESS_REGISTER_PAYMENT       
                    
            else:
                if form._errors and 'invoice' in form._errors:
                    result['validation_message'].append(form._errors['invoice'][0])  
                                  
                if form._errors and 'duplicate' in form._errors:
                    if form._errors['duplicate'][0] == ERROR_REQUIRED_DUPLICATE:
                        result['validation_message'].append(form._errors['duplicate'][0])
                    else:
                        result['error_message'] = form._errors['duplicate'][0]
                        
                if form._errors and 'payment_date' in form._errors:
                    result['validation_message'].append(form._errors['payment_date'][0]) 
       
            response = json.dumps(result)                
            return HttpResponse(response, mimetype="text/javascript") 
        else:
            return HttpResponseRedirect('/gerenciarlivraria/') 