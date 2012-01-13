from django.db import models

class Distributor(models.Model):
    name = models.CharField(max_length=50)
        
    class Meta:
        app_label = 'mistrael'