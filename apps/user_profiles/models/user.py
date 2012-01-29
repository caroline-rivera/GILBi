# encoding: utf-8

from django.db import models
from gilbi.apps.books.models.book import Book

import hashlib


FEMALE_IMG_PATH = "img/users/default/avatar-female.png"

MALE_IMG_PATH = "img/users/default/avatar-male.png"

GENDER_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)


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
    favorite_books = models.ManyToManyField(Book) #nao precisa criar a tabela 
    
    def set_encrypted_password(self, password):
        self.password = hashlib.sha224(password).hexdigest()
        
    def set_profile_data(self, profile_data):        
        if str(self.photo) != FEMALE_IMG_PATH and str(self.photo) != MALE_IMG_PATH:
            self.photo.delete()
            
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
        
    def disable_account(self):        
        if str(self.photo) != FEMALE_IMG_PATH and str(self.photo) != MALE_IMG_PATH:
            self.photo.delete()
            
        self.set_default_avatar()
        self.member_since = None
        self.profile_phrase = None
                
    class Meta:
        app_label = 'user_profiles'