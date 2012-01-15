# -*- encoding: utf-8 -*-

from django import forms
from gilbi.apps.library.models import Phone, Address
from gilbi.mistrael.messages.error_messages import *
from django.forms import ModelForm

class FormLibraryRegister(ModelForm):  
    ddd1 = forms.CharField(max_length=2, min_length=2, required = False,
                                 widget = forms.TextInput(attrs={'size': 4}))
    phone1 = forms.CharField(max_length=8, min_length=8, required = False,
                                 widget = forms.TextInput(attrs={'size': 10}))
    
    ddd2 = forms.CharField(max_length=2, min_length=2, required = False,
                                 widget = forms.TextInput(attrs={'size': 4}))
    phone2 = forms.CharField(max_length=8, min_length=8, required = False,
                                 widget = forms.TextInput(attrs={'size': 10})) 
    
    ddd3 = forms.CharField(max_length=2, min_length=2, required = False,
                                 widget = forms.TextInput(attrs={'size': 4}))
    phone3 = forms.CharField(max_length=8, min_length=8, required = False,
                                 widget = forms.TextInput(attrs={'size': 10}))
    
    ddd4 = forms.CharField(max_length=2, min_length=2, required = False,
                                 widget = forms.TextInput(attrs={'size': 4}))
    phone4 = forms.CharField(max_length=8, min_length=8, required = False,
                                 widget = forms.TextInput(attrs={'size': 10}))
    
    class Meta:
        model = Address
        fields = ('street', 'number', 'complement', 'zipcode', 'neighborhood') 
        
    def __init__(self, *args, **kwargs):
        self.base_fields['ddd1'].error_messages['min_length'] = ERROR_MINLENGTH_DDD1
        self.base_fields['ddd2'].error_messages['min_length'] = ERROR_MINLENGTH_DDD2
        self.base_fields['ddd3'].error_messages['min_length'] = ERROR_MINLENGTH_DDD3
        self.base_fields['ddd4'].error_messages['min_length'] = ERROR_MINLENGTH_DDD4
        self.base_fields['phone1'].error_messages['min_length'] = ERROR_MINLENGTH_PHONE1
        self.base_fields['phone2'].error_messages['min_length'] = ERROR_MINLENGTH_PHONE2
        self.base_fields['phone3'].error_messages['min_length'] = ERROR_MINLENGTH_PHONE3
        self.base_fields['phone4'].error_messages['min_length'] = ERROR_MINLENGTH_PHONE4
        
        self.base_fields['street'].required = False
        self.base_fields['number'].required = False
        self.base_fields['complement'].required = False
        self.base_fields['zipcode'].required = False
        self.base_fields['neighborhood'].required = False

        self.base_fields['street'].widget = forms.TextInput(attrs={'maxlength': 50, 'size': 50})
        self.base_fields['number'].widget = forms.TextInput(attrs={'maxlength': 5, 'size': 5})
        self.base_fields['complement'].widget = forms.TextInput(attrs={'maxlength': 50, 'size': 50})
        self.base_fields['zipcode'].widget = forms.TextInput(attrs={'maxlength': 9, 'size': 10})
        self.base_fields['neighborhood'].widget = forms.TextInput(attrs={'maxlength': 30, 'size': 30})
                 
        super(FormLibraryRegister, self).__init__(*args, **kwargs)  
        
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            phones = Phone.objects.filter(user = instance.id)
            if len(phones) > 0:
                self.initial['ddd1'] = phones[0].ddd
                self.initial['phone1'] = phones[0].number
            if len(phones) > 1:
                self.initial['ddd2'] = phones[1].ddd
                self.initial['phone2'] = phones[1].number
            if len(phones) > 2:
                self.initial['ddd3'] = phones[2].ddd
                self.initial['phone3'] = phones[2].number
            if len(phones) > 3:
                self.initial['ddd4'] = phones[3].ddd
                self.initial['phone4'] = phones[3].number  
                               
            adress = Address.objects.filter(user = instance.id)
            if len(adress) > 0:
                self.initial['street'] = adress[0].street
                self.initial['number'] = adress[0].number
                self.initial['complement'] = adress[0].complement
                self.initial['zipcode'] = adress[0].zipcode
                self.initial['neighborhood'] = adress[0].neighborhood

    def clean_ddd1(self):
        if (self.cleaned_data['ddd1'].isdigit() == False and \
        self.cleaned_data['ddd1'].strip() !=  ""):
            raise forms.ValidationError(ERROR_INVALID_DDD1)
        return self.cleaned_data['ddd1']

    def clean_phone1(self):
        if self.cleaned_data['phone1'].isdigit() == False and \
        self.cleaned_data['phone1'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_PHONE1)
        return self.cleaned_data['phone1']
    
    def clean_ddd2(self):
        if self.cleaned_data['ddd2'].isdigit() == False and \
        self.cleaned_data['ddd2'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_DDD2)
        return self.cleaned_data['ddd2']

    def clean_phone2(self):
        if self.cleaned_data['phone2'].isdigit() == False and \
        self.cleaned_data['phone2'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_PHONE2)
        return self.cleaned_data['phone2']
        
    def clean_ddd3(self):
        if self.cleaned_data['ddd3'].isdigit() == False and \
        self.cleaned_data['ddd3'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_DDD3)
        return self.cleaned_data['ddd3']        

    def clean_phone3(self):
        if self.cleaned_data['phone3'].isdigit() == False and \
        self.cleaned_data['phone3'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_PHONE3)
        return self.cleaned_data['phone3']
    
    def clean_ddd4(self):
        if self.cleaned_data['ddd4'].isdigit() == False and \
        self.cleaned_data['ddd4'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_DDD4)
        return self.cleaned_data['ddd4']
    
    def clean_phone4(self): 
        if self.cleaned_data['phone4'].isdigit() == False and \
        self.data['phone4'].strip() !=  "":
            raise forms.ValidationError(ERROR_INVALID_PHONE4)
    
        if self.data['phone1'] == "" or self.data['ddd1'] == "":
            if self.data['phone2'] == "" or self.data['ddd2'] == "":
                if self.data['phone3'] == "" or self.data['ddd3'] == "":
                    if self.cleaned_data['phone4'] == "" or self.data['ddd4'] == "":
                        raise forms.ValidationError(ERROR_REQUIRED_PHONE)
        return self.cleaned_data['phone4']
    
    def clean_street(self):
        if self.cleaned_data['street'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_STREET)
        return self.cleaned_data['street'].strip()

    def clean_number(self):
        if self.cleaned_data['number'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_NUMBER)
        return self.cleaned_data['number'].strip()

    def clean_complement(self):
        return self.cleaned_data['complement'].strip()
            
    def clean_zipcode(self):
        if self.cleaned_data['zipcode'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_ZIPCODE)
        return self.cleaned_data['zipcode'].strip()

    def clean_neighborhood(self):
        if self.cleaned_data['neighborhood'].strip() ==  "":
            raise forms.ValidationError(ERROR_REQUIRED_NEIGHBORHOOD)
        return self.cleaned_data['neighborhood'].strip()