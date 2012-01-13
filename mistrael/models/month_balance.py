from django.db import models

class MonthBalance(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    value = models.DecimalField(max_digits=7, decimal_places=2)
        
    class Meta:
        app_label = 'mistrael'

    