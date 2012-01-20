# encoding: utf-8

from django.db import models
from gilbi.apps.books.models import BookAuthor

class OrderGridFormat(models.Model):
    name = models.CharField()
    author = models.CharField()
    spiritual_author = models.CharField()
    order_date = models.CharField()
    quantity = models.IntegerField()
    situation = models.CharField()
    def __init__(self, order):
        self.id = order.id
        self.name = order.book.name
        self.author = self.set_authors(order.book)
        self.spiritual_author = self.set_spiritual_authors(order.book)
        self.order_date = self.set_date(order.order_date)
        self.quantity = order.quantity
        self.situation = self.set_situation(order.situation)
        
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
    
    def set_situation(self, situation):
        if situation == "A": 
            str_situation = "Aceita"
        elif situation == "R":
            str_situation = "Rejeitada"
        elif situation == "D":
            str_situation = "Disponível"
        elif situation == "C":
            str_situation = "Cancelada"
        elif situation == "V":
            str_situation = "Vendida"
        else: # "S"
            str_situation = "Solicitada"
        return str_situation
    
    def set_date(self, order_date):
        str_date = order_date.strftime('%d/%m/%Y %H:%M:%S')
        return str_date