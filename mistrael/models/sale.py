from django.db import models
from bookstore_book import BookstoreBook
from book_order import BookOrder

class Sale(models.Model):
    date_of_sale = models.DateField()
    price_of_sale = models.DecimalField(max_digits=4, decimal_places=2)
    
    class Meta:
        abstract = True
        
class ShelfSale(Sale):
    book = models.ForeignKey(BookstoreBook)
    
class OrderSale(Sale):
    book_order = models.ForeignKey(BookOrder)
    