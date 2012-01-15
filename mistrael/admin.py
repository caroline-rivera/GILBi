from django.contrib import admin
from gilbi.apps.user_profiles.models import User, Seller, Manager
from gilbi.apps.books.models import Author, Publisher, Book, BookAuthor
from gilbi.apps.bookstore.models import Distributor, BookstoreBook, BookOrder, ShelfSale, OrderSale
from gilbi.apps.bookstore.models import PurchaseItem, PurchaseOrder
from gilbi.apps.library.models import LibraryBook, Address, Phone, Loan
from gilbi.apps.financial.models import Invoice, Duplicate, Payment, MonthBalance

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Manager)

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookAuthor)

admin.site.register(Distributor)
admin.site.register(BookstoreBook)
admin.site.register(BookOrder)
admin.site.register(ShelfSale)
admin.site.register(OrderSale)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseOrder)

admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(LibraryBook)
admin.site.register(Loan)

admin.site.register(Invoice)
admin.site.register(Duplicate)
admin.site.register(Payment)
admin.site.register(MonthBalance)