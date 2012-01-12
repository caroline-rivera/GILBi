from django.db import models
from author import Author
from publisher import Publisher
from gilbi.mistrael.helpers.constants import CATEGORY_CHOICES

class Book(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(null=True, upload_to='img/books/')
    description = models.TextField(null=True)
    publisher = models.ForeignKey(Publisher)  
    authors = models.ManyToManyField(Author, through='BookAuthor') 
    
class BookAuthor(models.Model):
    author = models.ForeignKey(Author)
    book = models.ForeignKey(Book)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='F')


