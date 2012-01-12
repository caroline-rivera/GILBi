from django.db import models
from book_order import BookOrder
from bookstore_book import BookstoreBook
from distributor import Distributor

  
class PurchaseItem(models.Model):
    book_order = models.ForeignKey(BookOrder, null=True)
    book = models.ForeignKey(BookstoreBook, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
class PurchaseOrder(models.Model):
    date_of_order = models.DateField()
    itens = models.ManyToManyField(PurchaseItem)
    distributor = models.ForeignKey(Distributor)