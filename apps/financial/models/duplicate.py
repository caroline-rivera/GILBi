from django.db import models
from invoice import Invoice
from payment import Payment
     
class Duplicate(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='duplicates')
    number = models.IntegerField()
    value = models.DecimalField(max_digits=6, decimal_places=2)
    expiration_date = models.DateField()
    payment = models.ForeignKey(Payment)
        
    class Meta:
        app_label = 'financial'
    

