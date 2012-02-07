# encoding: utf-8

import json
from datetime import date
from decimal import Decimal
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from gilbi.apps.bookstore.forms import NewPurchaseItemForm, NewPurchaseOrderForm, PurchaseOrderForm
from gilbi.apps.bookstore.models import PurchaseOrder, PurchaseItem, Distributor, BookstoreBook, BookOrder
from gilbi.mistrael.helpers.session_helper import validate_session
from gilbi.mistrael.helpers.session_helper import validate_manager_session
from django.core import serializers
from gilbi.apps.bookstore.grid_formats import PurchaseItemGridFormat
from gilbi.mistrael.messages.success_messages import SUCCESS_NEW_PURCHASE_ORDER

def index(request):    
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    elif validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    else:
        form_purchase_item = NewPurchaseItemForm()
        form_new_purchase_order = NewPurchaseOrderForm()
        form_purchase_order = PurchaseOrderForm()
        
        return render_to_response('bookstore/purchase_order.html', 
                                  {'form_purchase_item': form_purchase_item,
                                   'form_new_purchase_order': form_new_purchase_order,
                                   'form_purchase_order': form_purchase_order},
                                  context_instance=RequestContext(request))

def save(request):
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
                                        
    if request.method == 'POST':
        distributor_id = int(request.POST['distributor'])        
        purchase_items = json.loads(request.POST['purchaseItems'])
        
        distributor = Distributor.objects.get(id=distributor_id)
        
        #TODO: Tirar o date_of_order e rodar syncdb        
        purchase_order = PurchaseOrder(distributor=distributor)  
        purchase_order.save()
        
        for purchase_item in purchase_items:
            book_id = int(purchase_item['bookId'])
            book_orders_ids = [int(p) for p in purchase_item['bookOrdersIds']]
            quantity = int(purchase_item['quantity'])
            
            # TODO: Tirar o price e rodar o syncdb            
            purchase_item = PurchaseItem(book=BookstoreBook.objects.get(id=book_id),
                                         quantity=quantity,
                                         price=Decimal("100.00"))  
            purchase_item.save()
            
            #TODO trocar para book_orders em PurchaseItem Model
            for book_order_id in book_orders_ids:
                book_order = BookOrder.objects.get(id=book_order_id)                                
                purchase_item.book_order.add(book_order)
                
                book_order.accept_order()
                book_order.save()
                
            #TODO trocar para items em PurchaseOrder Model    
            purchase_order.itens.add(purchase_item)
    
        result = {}
        result['success_message'] = SUCCESS_NEW_PURCHASE_ORDER + str(purchase_order.id) + ")"   
      
        response = json.dumps(result)
        return HttpResponse(response, mimetype="text/javascript") 
    
    else: #Método GET
        return HttpResponseRedirect('/gerenciarlivraria/pedidodecompra/')
        

def show(request):  
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    if request.method == 'GET' and 'purchase_order' in request.GET:   
        form = PurchaseOrderForm(request.GET, request.FILES)

        if form.is_valid():
            checked_form = form.cleaned_data
            purchase_order = checked_form['purchase_order']  
    
            items = purchase_order.itens.all()
            
            items_grid_format = [PurchaseItemGridFormat(item) for item in items]
            
            partial_response = serializers.serialize("json", items_grid_format)
    
            items_json = json.loads(partial_response)
            response_dic = {
                'read_only': purchase_order.date_of_order is not None,
                'items': items_json,
            }
    
            response = json.dumps(response_dic)
            return HttpResponse(response, mimetype="text/javascript")
        else:
            return HttpResponse([], mimetype="text/javascript")            
    else:
        return HttpResponseRedirect('/gerenciarlivraria/')
    

def conclude(request, purchase_order_id):  
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    
    purchase_order.conclude()
    purchase_order.save()        
    
    result = {}
    result['success_message'] = 'Pedido finalizado com sucesso!'
  
    response = json.dumps(result)
    return HttpResponse(response, mimetype="text/javascript")

def exclude(request, purchase_order_id):  
    if validate_session(request) == False:
        return HttpResponseRedirect('/logout/') 
    
    if validate_manager_session(request) == False:
        return HttpResponseRedirect('/perfil/')
    
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    purchase_items = purchase_order.itens.all()
    
    for item in purchase_items:
        orders = item.book_order.all()
        
        for order in orders:
            order.return_order()
            order.save()
    
    purchase_order.delete()
    
    result = {}
    result['success_message'] = 'Pedido excluído com sucesso!'
  
    response = json.dumps(result)
    return HttpResponse(response, mimetype="text/javascript") 
    