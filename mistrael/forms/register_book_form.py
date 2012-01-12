# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelChoiceField
from django.forms import ModelMultipleChoiceField
from gilbi.mistrael.models.publisher import Publisher
from gilbi.mistrael.models.author import Author
from gilbi.mistrael.models.book import Book
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_NAME
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_PUBLISHER_NAME
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_ONE_AUTHOR_NAME
from gilbi.mistrael.messages.error_messages import ERROR_SAME_PHYSICAL_SPIRITUAL_AUTHOR
from gilbi.mistrael.messages.error_messages import ERROR_ALREADY_REGISTERED_BOOK

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
    
class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class FormRegisterBook(forms.Form):
    name = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    photo = forms.ImageField(required=False)
    description = forms.CharField(required=False,
                                  widget = forms.Textarea(attrs={'rows': 8, 'cols': 65}))
    publisher = MyModelChoiceField(queryset=Publisher.objects.order_by('name'), empty_label=None) 
    author = MyModelMultipleChoiceField(queryset=Author.objects.order_by('name'))
    spiritual_author = MyModelMultipleChoiceField(required=False,
                                                  queryset=Author.objects.order_by('name')) 
    
    def __init__(self, *args, **kwargs):
        self.base_fields['name'].error_messages['required'] = ERROR_REQUIRED_BOOK_NAME
        self.base_fields['publisher'].error_messages['required'] = ERROR_REQUIRED_PUBLISHER_NAME
        self.base_fields['author'].error_messages['required'] = ERROR_REQUIRED_ONE_AUTHOR_NAME                                  
        super(FormRegisterBook, self).__init__(*args, **kwargs)
          
    def clean_name(self):   
        if Book.objects.filter(
                               name=self.cleaned_data['name']
                               ).exists() == True:
            raise forms.ValidationError(ERROR_ALREADY_REGISTERED_BOOK)
        return self.cleaned_data['name']
    
    def clean_spiritual_author(self):
        if 'author' in self.cleaned_data and 'spiritual_author' in self.cleaned_data:
            for spiritual_author in self.cleaned_data['spiritual_author']:
                for author in self.cleaned_data['author']:
                    if spiritual_author.id == author.id:
                        raise forms.ValidationError(ERROR_SAME_PHYSICAL_SPIRITUAL_AUTHOR)
        return self.cleaned_data['spiritual_author']