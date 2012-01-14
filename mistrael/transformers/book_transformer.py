# -*- encoding: utf-8 -*-
from django.db import models
from books.models.book_author import BookAuthor
from gilbi.mistrael.models.loan import Loan

class GridBookTransform(models.Model):
    name = models.CharField()
    author = models.CharField()
    spiritual_author = models.CharField()
    publisher = models.CharField()
    avaiable_quantity = models.IntegerField()
    def __init__(self, book):
        self.id = book.id
        self.name = book.name
        self.author = self.set_authors(book)
        self.spiritual_author = self.set_spiritual_authors(book)
        self.publisher = book.publisher.name
        self.avaiable_quantity = book.avaiable_quantity
        
    def set_authors(self, book):
        authors = book.authors.all()
        authors_list = []
        for author in authors:
            bookauthor = BookAuthor.objects.filter(book = book.id).filter(author = author.id)
            if bookauthor[0].category == 'F':
                authors_list.append(author.name)
        str_author = "\n".join(authors_list)
        return str_author
        
    def set_spiritual_authors(self, book):
        authors = book.authors.all()
        authors_list = []
        for author in authors:
            bookauthor = BookAuthor.objects.filter(book = book.id).filter(author = author.id)
            if bookauthor[0].category == 'E':
                authors_list.append(author.name)
        str_author = "\n".join(authors_list)
        return str_author
    
class GridLibraryBook(models.Model):
    name = models.CharField()
    author = models.CharField()
    spiritual_author = models.CharField()
    publisher = models.CharField()
    situation = models.CharField()
    def __init__(self, book):
        self.id = book.id
        self.name = book.book.name
        self.author = self.set_authors(book.book)
        self.spiritual_author = self.set_spiritual_authors(book.book)
        self.publisher = book.book.publisher.name
        self.situation = self.set_situation(book)
        
    def set_authors(self, book):
        authors = book.authors.all()
        authors_list = []
        for author in authors:
            bookauthor = BookAuthor.objects.filter(book = book.id).filter(author = author.id)
            if bookauthor[0].category == 'F':
                authors_list.append(author.name)
        str_author = "\n".join(authors_list)
        return str_author
        
    def set_spiritual_authors(self, book):
        authors = book.authors.all()
        authors_list = []
        for author in authors:
            bookauthor = BookAuthor.objects.filter(book = book.id).filter(author = author.id)
            if bookauthor[0].category == 'E':
                authors_list.append(author.name)
        str_author = "\n".join(authors_list)
        return str_author
    
    def set_situation(self, book):
        if Loan.objects.filter(book = book.id, return_date__isnull = True).exists() == True:
            situation = "Emprestado"
        else:
            situation = "Disponivel"
        return situation