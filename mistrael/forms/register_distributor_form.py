# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.bookstore.models import Distributor
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_DISTRIBUTOR_NAME
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_DISTRIBUTOR

class FormRegisterDistributor(forms.Form):
    name = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['name'].error_messages['required'] = ERROR_REQUIRED_DISTRIBUTOR_NAME                               
        super(FormRegisterDistributor, self).__init__(*args, **kwargs)  
    
    def clean_name(self):   
        if Distributor.objects.filter(
                               name=self.cleaned_data['name']
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_DISTRIBUTOR)
        return self.cleaned_data['name']