from django.db import models
from gilbi.apps.bookstore.models import BookOrder, BookstoreBook, Distributor

  
class PurchaseItem(models.Model):
    book_order = models.ForeignKey(BookOrder, null=True)
    book = models.ForeignKey(BookstoreBook, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
        
    class Meta:
        app_label = 'mistrael'
    
class PurchaseOrder(models.Model):
    date_of_order = models.DateField()
    itens = models.ManyToManyField(PurchaseItem)
    distributor = models.ForeignKey(Distributor)
        
    class Meta:
        app_label = 'mistrael'