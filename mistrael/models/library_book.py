from django.db import models
from books.models.book import Book

class LibraryBook(models.Model):
    book = models.ForeignKey(Book)
        
    class Meta:
        app_label = 'mistrael'