# encoding: utf-8

from django.db import models
    
class ManagerLoanGridFormat(models.Model):
    book_name = models.CharField()
    loan_date = models.CharField()
    expected_return_date = models.CharField()
    return_date = models.CharField()
    user_name = models.CharField()
    
    def __init__(self, loan):
        self.id = loan.book.id
        self.book_name = loan.book.book.name
        self.loan_date = self.set_date(loan.loan_date)
        self.expected_return_date = self.set_date(loan.expected_return_date)
        self.return_date = self.set_date(loan.return_date)
        self.user_name = self.set_user_name(loan.user)
        
    def set_date(self, date):
        if date == None:
            str_date = ""
        else:
            str_date = date.strftime('%d/%m/%Y')
        return str_date
    
    def set_user_name(self, user):
        link = "<a href=\"/gerenciarbiblioteca/informacoes/usuario/" + str(user.id) + "/\">" +\
        user.first_name + " " + user.last_name + "</a>"
        
        return link