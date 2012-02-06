# encoding: utf-8

from django import forms
from datetime import datetime
from django.forms import ModelChoiceField
from gilbi.apps.bookstore.models import PurchaseOrder

class PurchaseOrderChoiceField(ModelChoiceField):

    def label_from_instance(self, purchase_order):
        label = str(purchase_order.id) + ' - '
        
        if purchase_order.date_of_order is None:    
            label += 'Em elaboração'
        else:
            if len(purchase_order.invoice.all()) == 0:
                label += 'Finalizado'
            else:
                label += 'Disponível'
                
        label += ' - '
        label += str(purchase_order.distributor.name)
        
        return label 
        
class PurchaseOrderForm(forms.Form):
    purchase_order = PurchaseOrderChoiceField(queryset=PurchaseOrder.objects.order_by('id'),
                                               empty_label = "Número - Status - Distribuidora") 

       
    def __init__(self, *args, **kwargs):                          
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)