from django.db import models
from book_order import BookOrder
from sale import Sale

class OrderSale(Sale):
    book_order = models.ForeignKey(BookOrder)
        
    class Meta:
        app_label = 'bookstore'