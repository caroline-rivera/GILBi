# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelChoiceField
from gilbi.mistrael.models.user import User
from gilbi.mistrael.models.loan import Loan
from gilbi.mistrael.models.library_book import LibraryBook
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_CODE
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_USER_LOGIN
from gilbi.mistrael.messages.error_messages import ERROR_INEXISTENT_LIBRARY_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_INEXISTENT_LOGIN
from gilbi.mistrael.messages.error_messages import ERROR_BOOK_NOT_BORROWED
from gilbi.mistrael.messages.error_messages import ERROR_BOOK_BORROWED_WITH_ANOTHER_USER

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.id
    
class FormReceiveBook(forms.Form):
    book2 = MyModelChoiceField(queryset=LibraryBook.objects.order_by('id')) 
    user_login2 = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book2'].error_messages['required'] = ERROR_REQUIRED_BOOK_CODE
        self.base_fields['user_login2'].error_messages['required'] = ERROR_REQUIRED_USER_LOGIN                                 
        super(FormReceiveBook, self).__init__(*args, **kwargs)

    def clean_book2(self):   
        book2 = self.cleaned_data['book2']  

        if book2 == None:
            raise forms.ValidationError(ERROR_INEXISTENT_LIBRARY_BOOK)
        elif Loan.objects.filter(
                               book = book2.id,
                               return_date__isnull = True
                               ).exists() == False:
            raise forms.ValidationError(ERROR_BOOK_NOT_BORROWED)
        
        return self.cleaned_data['book2']

          
    def clean_user_login2(self):  
        user = None
        loan = None
                
        book_id = None
        if self.data['book2'] != "---------":
            book_id = int(self.data['book2'])
        
        if User.objects.filter(
                               login=self.cleaned_data['user_login2']
                               ).exists() == True:
            user = User.objects.get(login = self.cleaned_data['user_login2'])
            if Loan.objects.filter(
                                   book = book_id,
                                   return_date__isnull = True
                                   ).exists() == True:
                loan = Loan.objects.get(book = book_id, return_date__isnull = True)
      
        if self.cleaned_data['user_login2'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_USER_LOGIN)
        elif user == None:
            raise forms.ValidationError(ERROR_INEXISTENT_LOGIN)
        elif loan != None and loan.user.login != self.cleaned_data['user_login2']:
            raise forms.ValidationError(ERROR_BOOK_BORROWED_WITH_ANOTHER_USER)
        
        return self.cleaned_data['user_login2']
