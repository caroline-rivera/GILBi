from django.db import models
from gilbi.books.models.book import Book

class BookstoreBook(Book):
    total_quantity = models.IntegerField()
    avaiable_quantity = models.IntegerField()
    suggested_price = models.DecimalField(max_digits=4, decimal_places=2, null=True)
        
    class Meta:
        app_label = 'mistrael'