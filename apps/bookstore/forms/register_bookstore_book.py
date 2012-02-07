# encoding: utf-8

from django import forms
from decimal import Decimal,InvalidOperation
from django.forms import ModelChoiceField
from gilbi.apps.bookstore.models import BookstoreBook
from gilbi.apps.books.models import Book
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOKSTORE_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOKSTORE_BOOK_PRICE
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOKSTORE_BOOK_TOTAL_QUANTITY
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOKSTORE_BOOK_AVAILABLE_QUANTITY
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_PRICE
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_BOOKSTORE_BOOK_TOTAL_QUANTITY
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_BOOKSTORE_BOOK_AVAILABLE_QUANTITY
from gilbi.mistrael.messages.error_messages import ERROR_EXISTENT_BOOKSTORE_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_BOOKSTOREBOOK_QUANTITIES

  
class BookChoiceField(ModelChoiceField):
    
    def label_from_instance(self, book):
        label = book.name
        return label 
        
class RegisterBookstoreBookForm(forms.Form):
    book = BookChoiceField(queryset=Book.objects.order_by('name'))  
    price = forms.CharField(max_length=8, 
                             widget = forms.TextInput(attrs={'size': 8}))
    total_quantity = forms.CharField(max_length=4,
                                     widget = forms.TextInput(attrs={'size': 9}))
    available_quantity = forms.CharField(max_length=4,
                                         widget = forms.TextInput(attrs={'size': 9}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book'].error_messages['required'] = ERROR_REQUIRED_BOOKSTORE_BOOK
        self.base_fields['price'].error_messages['required'] = ERROR_REQUIRED_BOOKSTORE_BOOK_PRICE 
        self.base_fields['total_quantity'].error_messages['required'] = ERROR_REQUIRED_BOOKSTORE_BOOK_TOTAL_QUANTITY
        self.base_fields['available_quantity'].error_messages['required'] = ERROR_REQUIRED_BOOKSTORE_BOOK_AVAILABLE_QUANTITY         
                                
        super(RegisterBookstoreBookForm, self).__init__(*args, **kwargs)

         
    def clean_book(self):
        if self.data['book'] != "":
            book = self.cleaned_data['book']
            
            if BookstoreBook.objects.filter(id = book.id).exists() == True:             
                raise forms.ValidationError(ERROR_EXISTENT_BOOKSTORE_BOOK)
        
        return self.cleaned_data['book']
    
    def clean_total_quantity(self):
        if self.data['total_quantity'] != "":
            str_total_quantity = self.data['total_quantity']
            
            try:
                total_quantity = int(str_total_quantity)
                self.cleaned_data['total_quantity'] = total_quantity
                
                if total_quantity < 0:
                    raise forms.ValidationError(ERROR_INVALID_BOOKSTORE_BOOK_TOTAL_QUANTITY)
                
            except ValueError:            
                raise forms.ValidationError(ERROR_INVALID_BOOKSTORE_BOOK_TOTAL_QUANTITY)
        
        return self.cleaned_data['total_quantity']
    
    def clean_available_quantity(self):
        if self.data['available_quantity'] != "":
            str_total_quantity = self.data['available_quantity']
            
            try:
                available_quantity = int(str_total_quantity)
                self.cleaned_data['available_quantity'] = available_quantity
                
                if available_quantity < 0:
                    raise forms.ValidationError(ERROR_INVALID_BOOKSTORE_BOOK_AVAILABLE_QUANTITY)
            except ValueError:            
                raise forms.ValidationError(ERROR_INVALID_BOOKSTORE_BOOK_AVAILABLE_QUANTITY)

        if 'total_quantity' in self.cleaned_data:
            if available_quantity > self.cleaned_data['total_quantity']:
                raise forms.ValidationError(ERROR_INVALID_BOOKSTOREBOOK_QUANTITIES)
        
        return self.cleaned_data['available_quantity']

    def clean_price(self):
        if self.data['price'] != "":
            str_price = self.data['price']
            
        try:
            if str_price.find("R$ ") != -1:
                str_price = str_price.replace("R$ ","")
            price = Decimal(str_price)
            self.cleaned_data['price'] = price
        except InvalidOperation:
            raise forms.ValidationError(ERROR_INVALID_PRICE)
        
        return self.cleaned_data['price'] 