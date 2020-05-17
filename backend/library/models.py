from django.db import models

# Create your models here.
from django.db.models import Max

from django.core.cache import cache
from django.utils.functional import cached_property


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
        query_set = Book.objects.filter(series=self).order_by('pub_date')
        if len(query_set) == 0:
            return None
        return query_set[0].cover_url

class Book(models.Model):
    title = models.CharField(max_length=512)
    cover_url = models.URLField('URL for cover art', null=True)
    read_online_url = models.URLField('URL to read online', null=True)
    pub_date = models.DateTimeField('date published')
    series = models.ForeignKey(BookSeries, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=64, default='Novel')
    external_id = models.CharField(max_length=256, null=True)

    @cached_property
    def read(self):
        cache_key='book-read:'+str(self.id)
        value = cache.get(cache_key)
        if value is None:
            value = ReadingHistory.objects.filter(book_id=self.id).aggregate(Max('read_date'))['read_date__max']
            cache.set(cache_key, value, 3600)
        return value

    def __str__(self):
        return self.title

class ReadingHistory(models.Model):
    book = models.ForeignKey(Book, related_name='reading_history', on_delete=models.CASCADE)
    read_date = models.DateTimeField(auto_now_add=True, blank=True)

    def invalidate_book_cache(self):
        cache.delete('book-read:'+str(self.book_id))

    def save(self, *args, **kwargs):
        self.invalidate_book_cache()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.invalidate_book_cache()
        return super().delete(using=using, keep_parents=keep_parents)

class ReadingList(models.Model):
    title = models.CharField(max_length=512)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ReadingListEntry(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reading_list = models.ForeignKey(ReadingList, related_name='entries', on_delete=models.CASCADE)
    position = models.IntegerField(default=1)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.book.title