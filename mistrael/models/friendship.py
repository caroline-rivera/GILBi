from django.db import models
from user import User
    
class Friendship(models.Model):
    sender_friend = models.ForeignKey(User)
    receiver_friend = models.ForeignKey(User)    
    friends_since = models.DateField(null=True)