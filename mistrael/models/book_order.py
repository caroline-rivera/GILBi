from django.db import models
from user import User
from bookstore_book import BookstoreBook
from gilbi.mistrael.helpers.constants import SITUATION_CHOICES
  
class BookOrder(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    book = models.ForeignKey(BookstoreBook)
    quantity = models.IntegerField()
    situation = models.CharField(max_length=1, choices=SITUATION_CHOICES)
    order_date = models.DateTimeField()
    
    def cancel_order(self):
        self.situation = 'C'
        
    class Meta:
        app_label = 'mistrael'