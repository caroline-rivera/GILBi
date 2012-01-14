from django.db import models
from gilbi.apps.books.models.book import Book

class LibraryBook(models.Model):
    book = models.ForeignKey(Book)
        
    class Meta:
        app_label = 'mistrael'