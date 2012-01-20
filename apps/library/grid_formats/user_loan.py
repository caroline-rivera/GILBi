# encoding: utf-8

from django.db import models
from gilbi.apps.books.models import BookAuthor

class UserLoanGridFormat(models.Model):
    name = models.CharField()
    author = models.CharField()
    spiritual_author = models.CharField()
    loan_date = models.CharField()
    expected_return_date = models.CharField()
    return_date = models.CharField()
    def __init__(self, loan):
        self.id = loan.book.id
        self.name = loan.book.book.name
        self.author = self.set_authors(loan.book.book)
        self.spiritual_author = self.set_spiritual_authors(loan.book.book)
        self.loan_date = self.set_date(loan.loan_date)
        self.expected_return_date = self.set_date(loan.expected_return_date)
        self.return_date = self.set_date(loan.return_date)
        
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
    
    def set_date(self, date):
        if date == None:
            str_date = ""
        else:
            str_date = date.strftime('%d/%m/%Y')
        return str_date