# encoding: utf-8

from django import forms
from datetime import datetime
from django.forms import ModelChoiceField
from gilbi.apps.financial.models import Invoice
from gilbi.apps.bookstore.models import PurchaseOrder
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_PURCHASE_ORDER, ERROR_REQUIRED_INVOICE_NUMBER
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_INVOICE_SERIES
from gilbi.mistrael.messages.error_messages import ERROR_EXISTENT_INVOICE
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_INVOICE_NUMBER, ERROR_INVALID_INVOICE_SERIES


class PurchaseOrderChoiceField(ModelChoiceField):
    
    def label_from_instance(self, purchase_order):
        label = str(purchase_order.id) + ' - ' + \
                datetime.strftime(purchase_order.date_of_order, "%d/%m/%Y") + \
                ' - ' + str(purchase_order.distributor.name)
        return label 
        
class RegisterInvoiceForm(forms.Form):
    purchase_order = PurchaseOrderChoiceField(queryset=PurchaseOrder.objects.order_by('date_of_order'),
                                 empty_label = "Número - Data de Encomenda - Distribuidora")  
    number = forms.IntegerField()
    series = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        
        self.base_fields['purchase_order'].error_messages['required'] = ERROR_REQUIRED_PURCHASE_ORDER
        self.base_fields['number'].error_messages['required'] = ERROR_REQUIRED_INVOICE_NUMBER         
        self.base_fields['series'].error_messages['required'] = ERROR_REQUIRED_INVOICE_SERIES 
        
        self.base_fields['number'].error_messages['invalid'] = ERROR_INVALID_INVOICE_NUMBER  
        self.base_fields['series'].error_messages['invalid'] = ERROR_INVALID_INVOICE_SERIES 
                                     
        super(RegisterInvoiceForm, self).__init__(*args, **kwargs)

         
    def clean_purchase_order(self):
        if self.data['purchase_order'] != "":
            purchase_order = self.cleaned_data['purchase_order']
            
            if Invoice.objects.filter(purchase_order = purchase_order.id).exists() == True:             
                raise forms.ValidationError(ERROR_EXISTENT_INVOICE)
        
        return self.cleaned_data['purchase_order']

    def clean_payment_date(self):       
           
        return self.cleaned_data['payment_date']
    