# encoding: utf-8

from django.db import models
from gilbi.apps.user_profiles.models import User
from bookstore_book import BookstoreBook

SITUATION_CHOICES = (
                  ('S', 'Solicitada'),
                  ('A', 'Aceita'),
                  ('R', 'Rejeitada'),
                  ('D', 'Disponível'),
                  ('C', 'Cancelada'),
)

class BookOrder(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    book = models.ForeignKey(BookstoreBook)
    quantity = models.IntegerField()
    situation = models.CharField(max_length=1, choices=SITUATION_CHOICES)
    order_date = models.DateTimeField()
    
    def cancel_order(self):
        self.situation = 'C'
        
    def sell_order(self):
        self.situation = 'V'

    class Meta:
        app_label = 'bookstore'
