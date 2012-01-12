# -*- encoding: utf-8 -*-

from django import forms
from gilbi.mistrael.messages.error_messages import *

class FormChangePassword(forms.Form):
    new_password = forms.CharField(max_length=16, 
                                   min_length=8, 
                                   widget=forms.PasswordInput(attrs={'size': 25},
                                                              render_value=True))
    password_confirmation = forms.CharField(max_length=16, 
                                            widget=forms.PasswordInput(attrs={'size': 25},
                                                                       render_value=True))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['new_password'].error_messages['required'] = ERROR_REQUIRED_NEW_PASSWORD
        self.base_fields['password_confirmation'].error_messages['required'] = ERROR_REQUIRED_NEW_CONFIRMATION_PASSWORD                   
        self.base_fields['new_password'].error_messages['min_length'] = ERROR_MIN_LENGTH_NEW_PASSWORD                                           
        super(FormChangePassword, self).__init__(*args, **kwargs)     
    
    def clean_password_confirmation(self):
        if self.cleaned_data['password_confirmation'] != self.data['new_password']:
            raise forms.ValidationError(ERROR_DIFFERENT_NEW_PASSWORDS)
        return self.cleaned_data['password_confirmation']