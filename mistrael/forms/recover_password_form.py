# -*- encoding: utf-8 -*-

from django import forms
from gilbi.mistrael.models.user import User
from gilbi.mistrael.messages.error_messages import *

class FormRecoverPassword(forms.Form):
    email = forms.EmailField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 30}))

    
    def __init__(self, *args, **kwargs):
        self.base_fields['email'].error_messages['required'] = ERROR_REQUIRED_EMAIL                                  
        super(FormRecoverPassword, self).__init__(*args, **kwargs)  
    
    def clean_email(self):   
        if User.objects.filter(
                               email=self.cleaned_data['email']
                               ).exists() == False:
            raise forms.ValidationError(ERROR_EMAIL_NOT_REGISTERED)
        return self.cleaned_data['email']