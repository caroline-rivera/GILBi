# encoding: utf-8

from django import forms
from django.forms import ModelChoiceField
from gilbi.apps.books.models import Book
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_LIBRARY_BOOK

class BookChoiceField(ModelChoiceField):
    
    def label_from_instance(self, book):
        label = book.name
        return label 
        
class RegisterLibraryBookForm(forms.Form):
    book = BookChoiceField(queryset=Book.objects.order_by('name'))  
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book'].error_messages['required'] = ERROR_REQUIRED_LIBRARY_BOOK        
                                
        super(RegisterLibraryBookForm, self).__init__(*args, **kwargs)
