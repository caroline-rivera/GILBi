# encoding: utf-8

from datetime import date
from django import forms
from gilbi.apps.financial.models import MonthBalance
from gilbi.mistrael.messages.error_messages import ERROR_REQUIRED_MONTH, ERROR_REQUIRED_YEAR 
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_MONTH, ERROR_INVALID_YEAR 
from gilbi.mistrael.messages.error_messages import ERROR_INVALID_MONTH_YEAR, ERROR_MISSING_PREVIOUS_BALANCE

MONTH_CHOICES = (
    (0, '---------'),
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
)

YEAR_CHOICES = [(0, '---------')]
YEAR_CHOICES.extend([(year, str(year)) for year in range(2011, date.today().year + 1)])
    
class GenerateMonthBalanceForm(forms.Form):
    month = forms.ChoiceField(choices = MONTH_CHOICES)
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    
    def __init__(self, *args, **kwargs):
        self.base_fields['month'].error_messages['required'] = ERROR_REQUIRED_MONTH
        self.base_fields['year'].error_messages['required'] = ERROR_REQUIRED_YEAR                                         
        super(GenerateMonthBalanceForm, self).__init__(*args, **kwargs)     
    
    def clean_month(self):                 
        if self.cleaned_data['month'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_MONTH)
        
        int_month = int(self.cleaned_data['month'])
        
        if int_month not in range(1,13):
            raise forms.ValidationError(ERROR_INVALID_MONTH)

        return self.cleaned_data['month']
    
    def clean_year(self): 
        if self.data['month'] != "":
            int_month = int(self.data['month'])
        else:
            int_month = None
            
        if self.cleaned_data['year'].strip() == "":
            raise forms.ValidationError(ERROR_REQUIRED_YEAR)        
        int_year = int(self.cleaned_data['year'])
        
        if int_year not in range(2009, date.today().year + 1):
            raise forms.ValidationError(ERROR_INVALID_YEAR)
        
        if int_year == date.today().year and int_month is not None and \
        int_month > date.today().month:
            raise forms.ValidationError(ERROR_INVALID_MONTH_YEAR)
        
        if int_month is not None:
            previous_month_year = get_previous_month_year(int_month, int_year)

            if MonthBalance.objects.filter(
                                           month = previous_month_year['previous_month'], 
                                           year = previous_month_year['previous_year']
                                           ).exists() == False and \
                MonthBalance.objects.filter(
                                            month = int_month, 
                                            year = int_year
                                            ).exists() == False:
                raise forms.ValidationError(ERROR_MISSING_PREVIOUS_BALANCE)
        
        return self.cleaned_data['year']
    
def get_previous_month_year(current_month, current_year):
    data = {}
    
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year
        
    data['previous_month'] = previous_month
    data['previous_year'] = previous_year
    
    return data