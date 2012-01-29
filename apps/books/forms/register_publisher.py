# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.books.models import Publisher
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_PUBLISHER_NAME
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_PUBLISHER

class RegisterPublisherForm(forms.Form):
    publisher_name = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['publisher_name'].error_messages['required'] = ERROR_REQUIRED_PUBLISHER_NAME                               
        super(RegisterPublisherForm, self).__init__(*args, **kwargs)  
    
    def clean_publisher_name(self): 
        if self.cleaned_data['publisher_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_PUBLISHER_NAME)
          
        if Publisher.objects.filter(
                               name=self.cleaned_data['publisher_name'].strip()
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_PUBLISHER)
        return self.cleaned_data['publisher_name']