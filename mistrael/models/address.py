from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    neighborhood = models.CharField(max_length=30)
    
    def set_data(self, street, number, complement, zipcode, neighborhood):
        self.street = street
        self.number = number
        self.complement = complement
        self.zipcode = zipcode
        self.neighborhood = neighborhood
        
    class Meta:
        app_label = 'mistrael'

