from django.db import models
from author import Author
from publisher import Publisher

class Book(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(null=True, upload_to='img/books/')
    description = models.TextField(null=True)
    publisher = models.ForeignKey(Publisher)  
    authors = models.ManyToManyField(Author, through='BookAuthor')
        
    class Meta:
        app_label = 'books'


