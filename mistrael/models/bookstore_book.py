from django.db import models
from book import Book

class BookstoreBook(Book):
    total_quantity = models.IntegerField()
    avaiable_quantity = models.IntegerField()
    suggested_price = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    
    def sell_book(self):
        self.total_quantity = (self.total_quantity) - 1
        self.avaiable_quantity = (self.avaiable_quantity) -1
        
    def sell_order(self):
        self.total_quantity = (self.total_quantity) - 1