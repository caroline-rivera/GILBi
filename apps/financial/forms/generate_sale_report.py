# encoding: utf-8

from django import forms
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_INITIAL_DATE, ERROR_REQUIRED_ENDING_DATE 
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_INITIAL_DATE, ERROR_INVALID_ENDING_DATE 
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_INVALID_DATES

class GenerateSaleReportForm(forms.Form):
    
    initial_date = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%y"))
    ending_date = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%y"))
        
    def __init__(self, *args, **kwargs):

        self.base_fields['initial_date'].error_messages['required'] = ERROR_REQUIRED_INITIAL_DATE 
        self.base_fields['ending_date'].error_messages['required'] = ERROR_REQUIRED_ENDING_DATE 
        
        self.base_fields['initial_date'].error_messages['invalid'] = ERROR_INVALID_INITIAL_DATE
        self.base_fields['ending_date'].error_messages['invalid'] = ERROR_INVALID_ENDING_DATE        
                           
        super(GenerateSaleReportForm, self).__init__(*args, **kwargs)     
        
   
    def clean_initial_date(self):       
           
        return self.cleaned_data['initial_date']
    
    def clean_ending_date(self):  
        
        if 'initial_date' in self.cleaned_data:             
            if self.cleaned_data['ending_date'] < self.cleaned_data['initial_date']:
                raise forms.ValidationError(ERROR_REQUIRED_INVALID_DATES)

        return self.cleaned_data['ending_date']