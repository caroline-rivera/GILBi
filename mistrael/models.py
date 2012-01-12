#from model_classes.user import User
#from model_classes.seller import Seller
#from model_classes.manager import Manager
#from model_classes.message import Message
#from model_classes.friendship import Friendship
#from model_classes.author import Author
#from model_classes.publisher import Publisher
#from model_classes.book import Book
#from model_classes.favorite_book import FavoriteBook
#from model_classes.ordered_book import OrderedBook
#from model_classes.payment import Payment

#import hashlib
#
#from django.db import models
#
#class User(models.Model):
#    GENDER_CHOICES = (
#                      ('M', 'Mulher'),
#                      ('H', 'Homem'),
#    )    
#    first_name = models.CharField(max_length=20)
#    last_name = models.CharField(max_length=20)
#    login = models.CharField(max_length=20, unique=True)
#    password = models.CharField(max_length=56)
#    email = models.CharField(max_length=50, unique=True)    
#    member_since = models.DateField(null=True)
#    photo = models.ImageField(null=True, upload_to='img/users')
#    birthday = models.DateField(null=True)
#    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
#    institution = models.CharField(max_length=30, null=True)
#    profile_phrase = models.CharField(max_length=50, null=True)
#    
#    def set_encrypted_password(self, password):
#        self.password = hashlib.sha224(password).hexdigest()

#class Seller(User):
#    def bla(self):
#        pass
#    
#class Manager(User):
#    def bla(self):
#        pass
        
#class Distributor(models.Model):
#    name = models.CharField(max_length=50)
#            
#class Publisher(models.Model):
#    name = models.CharField(max_length=50)
#    
#class Author(models.Model):
#    name = models.CharField(max_length=50)
#            
#class Book(models.Model):
#    name = models.CharField(max_length=50)
#    photo = models.ImageField(null=True, upload_to='photos/books') #colocar alguns parametros
#    description = models.TextField(null=True)
#    publisher = models.ForeignKey(Publisher)  
#
#class BookstoreBook(models.Model):
#    id = models.ForeignKey(Book, primary_key=True)
#    total_quantity = models.IntegerField()
#    avaiable_quantity = models.IntegerField()
#    suggested_price = models.DecimalField(max_digits=4, decimal_places=2)
#
#class LibraryBook(models.Model):
#    id = models.ForeignKey(Book, primary_key=True)
#    total_quantity = models.IntegerField()
#    avaiable_quantity = models.IntegerField()
#            
#class AuthorBookCategory(models.Model):
#    author = models.ForeignKey(Author)
#    book = models.ForeignKey(Book)
#    
#class Loan(models.Model):
#    user = models.ForeignKey(User)
#    book = models.ForeignKey(LibraryBook)
#    loan_date = models.DateField()
#    expected_return_date = models.DateField()
#    return_date = models.DateField(null=True)
    
#class Friendship(models.Model):
#    sender_friend = models.ForeignKey(User)
#    receiver_friend = models.ForeignKey(User)    
#    friends_since = models.DateField(null=True)
    
#class Message(models.Model):
#    receiver = models.ForeignKey(User)
#    sender = models.ForeignKey(User)
#    date = models.DateTimeField()
#    text = models.TextField()
    


