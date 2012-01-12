from django.db import models

class Payment(models.Model):
    payment_date = models.DateField()
