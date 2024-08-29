from datetime import timedelta

from django.db import models

# Create your models here.
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.datetime_safe import datetime


class BookSeries(models.Model):
    title = models.CharField(max_length=512)
    external_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title

    @property
    def book_count(self):
        return Book.objects.filter(series=self).count()

    @property
    def cover_url(self):
        query_set = Book.objects.filter(series=self, cover_url__isnull=False).order_by('pub_date')
        if len(query_set) == 0:
            return None
        return query_set[0].cover_url


class Book(models.Model):
    title = models.CharField(max_length=512)
    cover_url = models.URLField('URL for cover art', null=True)
    read_online_url = models.URLField('URL to read online', null=True)
    pub_date = models.DateTimeField('date published')
    availability_date = models.DateTimeField('date it was made available', null=True)
    series = models.ForeignKey(BookSeries, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=64, default='Novel')
    external_source = models.CharField(max_length=32, null=True)
    external_id = models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    available_online = models.BooleanField(default=False)
    availability_last_check = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.title


def readable_books_query_set():
    return Book.objects \
        .filter(available_online=1) \
        .exclude(modified_date__lt=timezone.make_aware(datetime.today())-timedelta(days=61))


class BookReadingHistory(models.Model):
    book = models.OneToOneField(Book, related_name='last_read_history', on_delete=models.CASCADE)
    read_date = models.DateTimeField(blank=True, null=True)
    want_to_reread = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.read_date = ReadingHistory.objects.filter(book_id=self.book_id).aggregate(Max('read_date'))[
            'read_date__max']
        super().save(*args, **kwargs)


class ReadingHistory(models.Model):
    book = models.ForeignKey(Book, related_name='reading_history', on_delete=models.CASCADE)
    read_date = models.DateTimeField(auto_now_add=True, blank=True)

    def update_history(self):
        try:
            data = BookReadingHistory.objects.get(book_id=self.book_id)
        except:
            data = BookReadingHistory(book_id=self.book_id)
        data.want_to_reread = False
        data.save()
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_history()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_history()


class ReadingList(models.Model):
    title = models.CharField(max_length=512)
    archived = models.BooleanField(default=False)
    series = models.ManyToManyField(BookSeries, related_name='reading_lists')

    def __str__(self):
        return self.title


@receiver(post_save, sender=Book)
def add_new_entry_to_reading_lists(sender, instance, created, **kwargs):
    """Adds new books to reading lists that follow a series"""
    if not created or instance.series_id is None:
        return
    reading_lists = ReadingList.objects.filter(series__id=instance.series_id)
    for reading_list in reading_lists:
        position = reading_list.entries.aggregate(Max('position'))['position__max'] + 1 or 1
        ReadingListEntry(book=instance, reading_list=reading_list, position=position).save()


class ReadingListEntry(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reading_list = models.ForeignKey(ReadingList, related_name='entries', on_delete=models.CASCADE)
    position = models.IntegerField(default=1)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.book.title


class BookLink(models.Model):
    """
    Book relations (callbacks to previous issues in comics)
    Source is the book the other book is mentioned
    target can be null in case the book is not in the database.
    """
    source = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='target')
    link_text = models.TextField(default="", blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.source.title + " - " + self.link_text
