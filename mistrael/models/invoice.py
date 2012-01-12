from django.db import models
from payment import Payment
from purchase import PurchaseOrder
   
class Invoice(models.Model):
    number = models.IntegerField()
    series = models.IntegerField()
    purchase = models.ForeignKey(PurchaseOrder)
    
class Duplicate(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='duplicates')
    number = models.IntegerField()
    value = models.DecimalField(max_digits=4, decimal_places=2)
    expiration_date = models.DateField()
    payment = models.ForeignKey(Payment)
    

