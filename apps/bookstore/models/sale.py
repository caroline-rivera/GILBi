from django.db import models


class Sale(models.Model):
    date_of_sale = models.DateField()
    price_of_sale = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        abstract = True
        app_label = 'bookstore'    
  

    