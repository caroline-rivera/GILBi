# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelChoiceField
from gilbi.mistrael.models.bookstore_book import BookstoreBook
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_CODE
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_USER_LOGIN

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
    
class FormShelfSale(forms.Form):
    book = MyModelChoiceField(queryset=BookstoreBook.objects.order_by('name')) 
    book_price = forms.CharField(max_length=9, 
                             widget = forms.TextInput(attrs={'size': 9}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book'].error_messages['required'] = ERROR_REQUIRED_BOOK_CODE
        self.base_fields['book_price'].error_messages['required'] = ERROR_REQUIRED_USER_LOGIN                                 
        super(FormShelfSale, self).__init__(*args, **kwargs)

    def clean_book(self):          
        return self.cleaned_data['book']

          
    def clean_book_price(self):          
        return self.cleaned_data['book_price']
