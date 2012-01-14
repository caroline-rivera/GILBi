# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_LOGIN 
from gilbi.mistrael.messages.error_messages import ERROR_MIN_LENGTH_PASSWORD, ERROR_DIFFERENT_PASSWORDS

class EditAccountForm(forms.Form):
    login = forms.CharField(max_length=20,
                            widget = forms.TextInput(attrs={'size': 25}),
                            required = False)
    password = forms.CharField(max_length=16, 
                               min_length=8, 
                               widget=forms.PasswordInput(attrs={'size': 25},
                                                          render_value=True),
                               required = False)
    password_confirmation = forms.CharField(max_length=16, 
                                            widget=forms.PasswordInput(attrs={'size': 25},
                                                                       render_value=True),
                                            required = False)
    
    def __init__(self, *args, **kwargs):
        self.base_fields['password'].error_messages['min_length'] = ERROR_MIN_LENGTH_PASSWORD                    
        super(EditAccountForm, self).__init__(*args, **kwargs)  
    
    def clean_login(self):   
        if User.objects.filter(
                               login=self.cleaned_data['login']
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_LOGIN)
        return self.cleaned_data['login']
    
    def clean_password_confirmation(self):
        if self.cleaned_data['password_confirmation'] != self.data['password']:
            raise forms.ValidationError(ERROR_DIFFERENT_PASSWORDS)
        return self.cleaned_data['password_confirmation']