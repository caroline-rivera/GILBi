# -*- encoding: utf-8 -*-

from django import forms
from books.models.author import Author
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_AUTHOR_NAME
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_AUTHOR

class RegisterAuthorForm(forms.Form):
    name = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['name'].error_messages['required'] = ERROR_REQUIRED_AUTHOR_NAME                               
        super(RegisterAuthorForm, self).__init__(*args, **kwargs)  
    
    def clean_name(self):   
        if Author.objects.filter(
                               name=self.cleaned_data['name']
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_AUTHOR)
        return self.cleaned_data['name']