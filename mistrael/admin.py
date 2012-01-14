from django.contrib import admin
from gilbi.mistrael.models.user import User
from gilbi.mistrael.models.seller import Seller
from gilbi.mistrael.models.manager import Manager
from gilbi.apps.books.models import Author, Publisher, Book
from gilbi.mistrael.models.distributor import Distributor
from gilbi.mistrael.models.library_book import LibraryBook
from gilbi.mistrael.models.bookstore_book import BookstoreBook

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Manager)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Distributor)
admin.site.register(Book)
admin.site.register(LibraryBook)
admin.site.register(BookstoreBook)