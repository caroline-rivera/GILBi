from django.db import models
from book import Book

class LibraryBook(models.Model):
    book = models.ForeignKey(Book)