from django.contrib import admin
from gilbi.apps.user_profiles.models import User, Seller, Manager
from gilbi.apps.books.models import Author, Publisher, Book
from gilbi.apps.bookstore.models import Distributor, BookstoreBook
from gilbi.apps.library.models import LibraryBook

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Manager)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Distributor)
admin.site.register(Book)
admin.site.register(LibraryBook)
admin.site.register(BookstoreBook)