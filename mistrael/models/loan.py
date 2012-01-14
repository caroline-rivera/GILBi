from django.db import models
from gilbi.apps.user_profiles.models import User
from library_book import LibraryBook

from datetime import timedelta, date

class Loan(models.Model):
    user = models.ForeignKey(User, related_name='book_loans')
    book = models.ForeignKey(LibraryBook)
    loan_date = models.DateField()
    expected_return_date = models.DateField()
    return_date = models.DateField(null=True)
    
    def renew_book(self):
        actual_date = self.expected_return_date
        self.expected_return_date = actual_date + timedelta(days=15) 
        
    def receive_book(self):
        self.return_date = date.today()
        
    class Meta:
        app_label = 'mistrael'