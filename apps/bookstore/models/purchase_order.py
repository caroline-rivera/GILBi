from datetime import date
from django.db import models
from distributor import Distributor
from purchase_item import PurchaseItem
   
class PurchaseOrder(models.Model):
    date_of_order = models.DateField(null=True)
    itens = models.ManyToManyField(PurchaseItem)
    distributor = models.ForeignKey(Distributor)
    
    def conclude(self):
        self.date_of_order = date.today()
        
    class Meta:
        app_label = 'bookstore'