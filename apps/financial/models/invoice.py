from django.db import models
from gilbi.mistrael.models.purchase import PurchaseOrder
   
class Invoice(models.Model):
    number = models.IntegerField()
    series = models.IntegerField()
    purchase = models.ForeignKey(PurchaseOrder)
        
    class Meta:
        app_label = 'financial'
    

