# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelChoiceField
from gilbi.apps.library.models import Phone, Loan, LibraryBook, Address
from gilbi.apps.user_profiles.models import User
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_BOOK_CODE
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_USER_LOGIN
from gilbi.mistrael.messages.error_messages import ERROR_INEXISTENT_LIBRARY_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_INEXISTENT_LOGIN
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_LIBRARY_REGISTER
from gilbi.mistrael.messages.error_messages import ERROR_BOOK_ALREADY_BORROW
from gilbi.mistrael.messages.error_messages import ERROR_USER_ALREADY_BORROWED_A_BOOK
from gilbi.mistrael.messages.error_messages import ERROR_BOOK_ALREADY_RENEWED

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.id
    
class FormBorrowBook(forms.Form):
    book1 = MyModelChoiceField(queryset=LibraryBook.objects.order_by('id')) 
    user_login1 = forms.CharField(max_length=50, 
                             widget = forms.TextInput(attrs={'size': 50}))
    
    def __init__(self, *args, **kwargs):
        self.base_fields['book1'].error_messages['required'] = ERROR_REQUIRED_BOOK_CODE
        self.base_fields['user_login1'].error_messages['required'] = ERROR_REQUIRED_USER_LOGIN                                 
        super(FormBorrowBook, self).__init__(*args, **kwargs)

    def clean_book1(self):   
        book1 = self.cleaned_data['book1']  

        if book1 == None:
            raise forms.ValidationError(ERROR_INEXISTENT_LIBRARY_BOOK)
        elif Loan.objects.filter(
                               book = book1.id,
                               return_date__isnull = True
                               ).exists() == True:
            loan = Loan.objects.get(book = book1.id, return_date__isnull = True)
            if loan.user.login != self.data['user_login1']:
                raise forms.ValidationError(ERROR_BOOK_ALREADY_BORROW)
        
        return self.cleaned_data['book1']

          
    def clean_user_login1(self):  
        user = None
        loan = None 
        
        if User.objects.filter(
                               login=self.cleaned_data['user_login1']
                               ).exists() == True:
            user = User.objects.get(login = self.cleaned_data['user_login1'])
            if Loan.objects.filter(
                                   user = user.id,
                                   return_date__isnull = True
                                   ).exists() == True:
                loan = Loan.objects.get(user = user.id, return_date__isnull = True)
      
        if self.cleaned_data['user_login1'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_USER_LOGIN)
        elif user == None:
            raise forms.ValidationError(ERROR_INEXISTENT_LOGIN)
        elif Address.objects.filter(user=user.id).exists() == False == None or \
        Phone.objects.filter(user=user.id).exists() == False:
            raise forms.ValidationError(ERROR_INVALID_LIBRARY_REGISTER)
        elif loan is not None and self.data['book1'] != "" and \
        loan.book.id != int(self.data['book1']):
            raise forms.ValidationError(ERROR_USER_ALREADY_BORROWED_A_BOOK)
        elif loan is not None and self.data['book1'] != "" and \
        loan.book.id == int(self.data['book1']) and \
        (loan.expected_return_date - loan.loan_date).days >= 30:
            raise forms.ValidationError(ERROR_BOOK_ALREADY_RENEWED)
        
        return self.cleaned_data['user_login1']
