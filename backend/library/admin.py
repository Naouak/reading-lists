from django.contrib import admin

from .models import BookSeries, Book, ReadingList, ReadingListEntry

# Register your models here.
admin.site.register(BookSeries)
admin.site.register(Book)
admin.site.register(ReadingList)
admin.site.register(ReadingListEntry)