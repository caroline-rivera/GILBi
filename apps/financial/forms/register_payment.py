# encoding: utf-8

from django import forms
from datetime import datetime
from django.forms import ModelChoiceField
from gilbi.apps.financial.models import Invoice, Duplicate
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_INVOICE, ERROR_REQUIRED_DUPLICATE
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_INVOICE_DUPLICATE
from gilbi.mistrael.messages.error_messages import ERROR_DUPLICATE_ALREADY_PAID
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_PAYMENT_DATE, ERROR_INVALID_PAYMENT_DATE


class InvoiceChoiceField(ModelChoiceField):
    
    def label_from_instance(self, invoice):
        label = str(invoice.number)+' - '+str(invoice.series)
        return label 

class DuplicateChoiceField(ModelChoiceField):
    
    def label_from_instance(self, duplicate):
        label = str(duplicate.number) + ' - ' + \
                datetime.strftime(duplicate.expiration_date, "%d/%m/%Y") + \
                ' - R$ ' + str(duplicate.value)
        return label 
        
class RegisterPaymentForm(forms.Form):
    invoice = InvoiceChoiceField(queryset=Invoice.objects.all(),
                                 empty_label = "Número - Série")  
    duplicate = DuplicateChoiceField(queryset=Duplicate.objects.order_by('invoice', 'id'),
                                 empty_label = "Número - Data Expiração - Valor")
#    duplicate = DuplicateChoiceField(queryset=Duplicate.objects.filter(payment__isnull=True),
#                                 empty_label = "Número - Data Expiração - Valor")
    payment_date = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%y"))
    
    def __init__(self, *args, **kwargs):
        
        self.base_fields['invoice'].error_messages['required'] = ERROR_REQUIRED_INVOICE
        self.base_fields['duplicate'].error_messages['required'] = ERROR_REQUIRED_DUPLICATE 
        
        self.base_fields['payment_date'].error_messages['required'] = ERROR_REQUIRED_PAYMENT_DATE 
        self.base_fields['payment_date'].error_messages['invalid'] = ERROR_INVALID_PAYMENT_DATE   
                                     
        super(RegisterPaymentForm, self).__init__(*args, **kwargs)

    def clean_invoice(self):     
             
        return self.cleaned_data['invoice']
          
    def clean_duplicate(self):  

        if self.data['invoice'] != "" and self.data['duplicate'] != "":
            invoice = self.cleaned_data['invoice']
            duplicate = self.cleaned_data['duplicate']
            
            if duplicate.invoice.id != invoice.id:             
                raise forms.ValidationError(ERROR_INVALID_INVOICE_DUPLICATE)
            
            if duplicate.payment is not None:
                raise forms.ValidationError(ERROR_DUPLICATE_ALREADY_PAID)
        
        return self.cleaned_data['duplicate']

    def clean_payment_date(self):       
           
        return self.cleaned_data['payment_date']
        
#    def get_unpaid_invoices(self):
#        invoices = Invoice.objects.all()
#        unpaid_invoices = []
#        
#        for invoice in invoices:
#            duplicates = invoices.duplicates.all()
#            for duplicate in duplicates:
#                if duplicate.payment is not None:
#                    unpaid_invoices.append(invoice)
#                    break      
#                
#        return unpaid_invoices        
