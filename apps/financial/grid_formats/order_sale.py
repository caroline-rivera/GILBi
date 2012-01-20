# encoding: utf-8
from django.db import models
from gilbi.apps.books.models import BookAuthor

class OrderSaleGridFormat(models.Model):
    name = models.CharField()
    author = models.CharField()
    spiritual_author = models.CharField()
    publisher = models.CharField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    date = models.CharField()
    def __init__(self, order_sale):
        self.id = order_sale.id
        self.name = order_sale.book_order.book.name
        self.author = self.set_authors(order_sale.book_order.book)
        self.spiritual_author = self.set_spiritual_authors(order_sale.book_order.book)
        self.publisher = order_sale.book_order.book.publisher.name
        self.quantity = order_sale.book_order.quantity
        self.price = order_sale.price_of_sale
        self.date = order_sale.date_of_sale.strftime('%d/%m/%Y')
        
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