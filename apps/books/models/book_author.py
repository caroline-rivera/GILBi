# encoding: utf-8

from django.db import models
from book import Book
from author import Author

CATEGORY_CHOICES = (
    ('F', 'Físico'),
    ('E', 'Espiritual'),
) 
    
class BookAuthor(models.Model):
    author = models.ForeignKey(Author)
    book = models.ForeignKey(Book)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='F')
        
    class Meta:
        app_label = 'books'