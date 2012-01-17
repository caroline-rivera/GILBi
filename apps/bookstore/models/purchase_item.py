from django.db import models
from book_order import BookOrder
from bookstore_book import  BookstoreBook
  
class PurchaseItem(models.Model):
    book_order = models.ManyToManyField(BookOrder)
    book = models.ForeignKey(BookstoreBook)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
        
    class Meta:
        app_label = 'bookstore'