from django.contrib import admin
from watchlist_app.models import OnlineLibrary, Book, Review

# Register your models here.
admin.site.register(OnlineLibrary)
admin.site.register(Book)
admin.site.register(Review)
