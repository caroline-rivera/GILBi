from django.db import models
from gilbi.apps.bookstore.models.purchase_order import PurchaseOrder
   
class Invoice(models.Model):
    number = models.IntegerField()
    series = models.IntegerField()
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='invoice')
        
    class Meta:
        app_label = 'financial'
    

