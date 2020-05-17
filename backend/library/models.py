from django.db import models

# Create your models here.
from django.db.models import Max
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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
    availability_date = models.DateTimeField('date it was made available', null=True)
    series = models.ForeignKey(BookSeries, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=64, default='Novel')
    external_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.title

class BookReadingHistory(models.Model):
    book = models.OneToOneField(Book, related_name='last_read_history', on_delete=models.CASCADE)
    read_date = models.DateTimeField(blank=True, null=True)

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