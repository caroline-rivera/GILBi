# encoding: utf-8

from django import forms
from django.forms import ModelChoiceField
from gilbi.apps.bookstore.models import BookstoreBook
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_QUANTITY

class BookChoiceField(ModelChoiceField):
    def label_from_instance(self, book):
        return book.name
    
class NewPurchaseItemForm(forms.Form):
    book = BookChoiceField(queryset=BookstoreBook.objects.order_by('name')) 
    quantity = forms.CharField(max_length=3, 
                             widget = forms.TextInput(attrs={'size': 10}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book'].error_messages['required'] = ERROR_REQUIRED_BOOK
        self.base_fields['quantity'].error_messages['required'] = ERROR_REQUIRED_BOOK_QUANTITY                                 
        super(NewPurchaseItemForm, self).__init__(*args, **kwargs)