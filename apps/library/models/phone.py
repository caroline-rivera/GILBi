from django.db import models
from gilbi.apps.user_profiles.models import User

class Phone(models.Model):
    user = models.ForeignKey(User, related_name='phones')
    ddd = models.CharField(max_length=2)
    number = models.CharField(max_length=8)
    
    def set_data(self, user, ddd, number):
        self.user = user
        self.ddd = ddd
        self.number = number
        
    class Meta:
        app_label = 'library'