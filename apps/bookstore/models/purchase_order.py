from django.db import models
from distributor import Distributor
from purchase_item import PurchaseItem
   
class PurchaseOrder(models.Model):
    date_of_order = models.DateField()
    itens = models.ManyToManyField(PurchaseItem)
    distributor = models.ForeignKey(Distributor)
        
    class Meta:
        app_label = 'bookstore'