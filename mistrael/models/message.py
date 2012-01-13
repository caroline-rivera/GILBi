from django.db import models
from user import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sended_messages')
    receiver = models.ForeignKey(User, related_name='received_messages')
    date_of_message = models.DateTimeField()
    text = models.TextField()
        
    class Meta:
        app_label = 'mistrael'

# Sobre related_name
# Posso chamar user.sended_messages
# Posso chamar user.received_messages