from django.db import models
from gilbi.apps.books.models.book import Book
from address import Address
from gilbi.mistrael.helpers.constants import FEMALE_IMG_PATH, MALE_IMG_PATH, GENDER_CHOICES

import hashlib

def set_upload_path(instance, filename):
    photo_path = 'img/users/' + str(instance.id) + '/' + filename
    return photo_path

class User(models.Model): 
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=56)
    email = models.CharField(max_length=50, unique=True)    
    member_since = models.DateField(null=True)
    photo = models.ImageField(null=True, upload_to= set_upload_path)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    institution = models.CharField(max_length=30, null=True)
    profile_phrase = models.CharField(max_length=100, null=True)
    address = models.ForeignKey(Address, null=True)
    favorite_books = models.ManyToManyField(Book) #nao precisa criar a tabela 
    
    def set_encrypted_password(self, password):
        self.password = hashlib.sha224(password).hexdigest()
        
    def set_profile_data(self, profile_data):
        self.first_name = profile_data['first_name']
        self.last_name = profile_data['last_name']
        self.photo = profile_data['photo']
        self.gender = profile_data['gender']
        self.institution = profile_data['institution']
        self.birthday = profile_data['birthday']
        if profile_data['photo'] == None:
            self.set_default_avatar()
        else:
            self.photo = profile_data['photo']
        
    def set_default_avatar(self):
        if self.gender == 'F':
            self.photo = FEMALE_IMG_PATH
        else:
            self.photo = MALE_IMG_PATH
            
    def set_profile_phrase(self, profile_phrase):
        self.profile_phrase = profile_phrase
        
    class Meta:
        app_label = 'mistrael'
                    
#class User(models.Model):
#    GENDER_CHOICES = (
#                      ('M', 'Mulher'),
#                      ('H', 'Homem'),
#    )
#    id = models.AutoField(primary_key=True)
    #first_name = models.CharField(max_length=20)
    #last_name = models.CharField(max_length=20)
    #login = models.CharField(max_length=20, unique=True)
    #password = models.CharField(max_length=50)
    #member_since = models.DateField()
    #photo = models.ImageField(null=True)
    #birthday = models.DateField(null=True)
    #gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    #institution = models.CharField(max_length=30, null=True)
    #profile_phrase = models.CharField(max_length=50)
    #favorite_books = models.ManyToManyField(Book) #pesquisar trade name
    #ordered_books = models.ManyToManyField(Book)    
