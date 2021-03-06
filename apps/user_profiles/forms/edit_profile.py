# -*- encoding: utf-8 -*-

from datetime import date
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_FIRST_NAME, ERROR_REQUIRED_LAST_NAME
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_GENDER, ERROR_INVALID_DATE
from django.forms import ModelForm

def set_upload_path(instance):
    return '/'.join(['FormEditProfile', instance.User.id])   
    
class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'photo', 'institution', 'birthday')  
       
    def __init__(self, *args, **kwargs):
        self.base_fields['birthday'].required = False
        self.base_fields['photo'].required = False
        self.base_fields['institution'].required = False
                
        self.base_fields['birthday'].widget = SelectDateWidget(years=range(date.today().year,1910,-1))    
        self.base_fields['first_name'].widget = forms.TextInput(attrs={'maxlength': 20, 'size': 25})
        self.base_fields['last_name'].widget = forms.TextInput(attrs={'maxlength': 20, 'size': 25})
        self.base_fields['institution'].widget = forms.TextInput(attrs={'maxlength': 30, 'size': 30})
                
        self.base_fields['first_name'].error_messages['required'] = ERROR_REQUIRED_FIRST_NAME 
        self.base_fields['last_name'].error_messages['required'] = ERROR_REQUIRED_LAST_NAME
        self.base_fields['gender'].error_messages['required'] = ERROR_REQUIRED_GENDER 
        self.base_fields['birthday'].error_messages['invalid'] = ERROR_INVALID_DATE    
                               
        super(EditProfileForm, self).__init__(*args, **kwargs)  

    def clean_first_name(self):   
        if self.cleaned_data['first_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_FIRST_NAME)
        return self.cleaned_data['first_name']
    
    def clean_last_name(self):   
        if self.cleaned_data['last_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_LAST_NAME)
        return self.cleaned_data['last_name']