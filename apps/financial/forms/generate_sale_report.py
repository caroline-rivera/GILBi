# encoding: utf-8

from datetime import date
from django.forms.extras.widgets import SelectDateWidget
from django import forms

    
class GenerateSaleReportForm(forms.Form):
    initial_date = forms.DateField()
    ending_date = forms.DateField()
    
    def __init__(self, *args, **kwargs):
        #self.base_fields['initial_date'].widget = SelectDateWidget(years=range(date.today().year,2010,-1))
        #self.base_fields['ending_date'].widget = SelectDateWidget(years=range(date.today().year,2010,-1))                              
        super(GenerateSaleReportForm, self).__init__(*args, **kwargs)     
