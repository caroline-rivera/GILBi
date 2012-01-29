# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.messages.error_messages import *
from gilbi.apps.user_profiles.models.user import GENDER_CHOICES

class RegisterNewUserForm(forms.Form):   
    first_name = forms.CharField(max_length=20,
                                 widget = forms.TextInput(attrs={'size': 25}))
    last_name = forms.CharField(max_length=20,
                                widget = forms.TextInput(attrs={'size': 25}))
    gender= forms.ChoiceField(required= True,
                               label= False,
                               widget= forms.Select(),
                               choices= GENDER_CHOICES,
                               initial= 'H')
    login = forms.CharField(max_length=20,
                            widget = forms.TextInput(attrs={'size': 25}))
    email = forms.EmailField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 25}))
    password = forms.CharField(max_length=16, 
                               min_length=8, 
                               widget=forms.PasswordInput(attrs={'size': 25},
                                                          render_value=True))
    password_confirmation = forms.CharField(max_length=16, 
                                            widget=forms.PasswordInput(attrs={'size': 25},
                                                                       render_value=True))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['first_name'].error_messages['required'] = ERROR_REQUIRED_FIRST_NAME 
        self.base_fields['last_name'].error_messages['required'] = ERROR_REQUIRED_LAST_NAME
        self.base_fields['login'].error_messages['required'] = ERROR_REQUIRED_LOGIN
        self.base_fields['email'].error_messages['required'] = ERROR_REQUIRED_EMAIL
        self.base_fields['password'].error_messages['required'] = ERROR_REQUIRED_PASSWORD 
        self.base_fields['gender'].error_messages['required'] = ERROR_REQUIRED_GENDER     
        self.base_fields['password'].error_messages['min_length'] = ERROR_MIN_LENGTH_PASSWORD         
        self.base_fields['password_confirmation'].error_messages['required'] = ERROR_REQUIRED_CONFIRMATION_PASSWORD                                       
        super(RegisterNewUserForm, self).__init__(*args, **kwargs)  

    def clean_first_name(self):   
        if self.cleaned_data['first_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_FIRST_NAME)
        return self.cleaned_data['first_name']
    
    def clean_last_name(self):   
        if self.cleaned_data['last_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_LAST_NAME)
        return self.cleaned_data['last_name']
        
    def clean_email(self):   
        if User.objects.filter(
                               email=self.cleaned_data['email'].strip().lower()
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_EMAIL)
        return self.cleaned_data['email']
    
    def clean_login(self):   
        if User.objects.filter(
                               login=self.cleaned_data['login'].strip().lower()
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_LOGIN)
        return self.cleaned_data['login']
    
    def clean_password_confirmation(self):
        if self.cleaned_data['password_confirmation'] != self.data['password']:
            raise forms.ValidationError(ERROR_DIFFERENT_PASSWORDS)
        return self.cleaned_data['password_confirmation']