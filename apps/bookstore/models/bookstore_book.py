from django.db import models
from gilbi.apps.books.models import Book

class BookstoreBook(Book):
    total_quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    suggested_price = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    
    def sell_book(self):
        self.total_quantity = (self.total_quantity) - 1
        self.available_quantity = (self.available_quantity) -1
        
    def sell_order(self):
        self.total_quantity = (self.total_quantity) - 1
        
    class Meta:
        app_label = 'bookstore'
