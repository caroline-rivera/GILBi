# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.books.models import Author
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_AUTHOR_NAME
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_AUTHOR

class RegisterAuthorForm(forms.Form):
    author_name = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['author_name'].error_messages['required'] = ERROR_REQUIRED_AUTHOR_NAME                               
        super(RegisterAuthorForm, self).__init__(*args, **kwargs)  
    
    def clean_author_name(self):
        if self.cleaned_data['author_name'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_AUTHOR_NAME)
        
        if Author.objects.filter(
                               name=self.cleaned_data['author_name'].strip()
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_AUTHOR)
        return self.cleaned_data['author_name']