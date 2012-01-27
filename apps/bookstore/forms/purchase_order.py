# encoding: utf-8

from django import forms
from datetime import datetime
from django.forms import ModelChoiceField
from gilbi.apps.bookstore.models import PurchaseOrder

class PurchaseOrderChoiceField(ModelChoiceField):

    def label_from_instance(self, purchase_order):
        label = str(purchase_order.id) + ' - '
        
        if purchase_order.date_of_order is not None:
            label += datetime.strftime(purchase_order.date_of_order, "%d/%m/%Y")
        else:
            label += 'Em elaboração'
            
        label += ' - '
        label += str(purchase_order.distributor.name)
        
        return label 
        
class PurchaseOrderForm(forms.Form):
    purchase_orders = PurchaseOrderChoiceField(queryset=PurchaseOrder.objects.order_by('id'),
                                               empty_label = "Número - Data de Encomenda - Distribuidora") 


       
    def __init__(self, *args, **kwargs):                          
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)