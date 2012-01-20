# encoding: utf-8

from django import forms
from django.forms import ModelChoiceField
from gilbi.apps.bookstore.models import Distributor
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_DISTRIBUTOR

class DistributorChoiceField(ModelChoiceField):
    def label_from_instance(self, distributor):
        return distributor.name
    
class NewPurchaseOrderForm(forms.Form):
    distributor = DistributorChoiceField(queryset=Distributor.objects.order_by('name')) 

    
    def __init__(self, *args, **kwargs):
        self.base_fields['distributor'].error_messages['required'] = ERROR_REQUIRED_DISTRIBUTOR                              
        super(NewPurchaseOrderForm, self).__init__(*args, **kwargs)