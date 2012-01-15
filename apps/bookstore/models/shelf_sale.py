from django.db import models
from bookstore_book import BookstoreBook
from sale import Sale

class ShelfSale(Sale):
    book = models.ForeignKey(BookstoreBook)
        
    class Meta:
        app_label = 'bookstore'