from django.db import models

# Create your models here.
from django.db.models import Max


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

    @property
    def read(self):
        return ReadingHistory.objects.filter(book_id=self.id).aggregate(Max('read_date'))['read_date__max']

    def __str__(self):
        return self.title

class ReadingHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateTimeField(auto_now_add=True, blank=True)

class ReadingList(models.Model):
    title = models.CharField(max_length=512)

    @property
    def progress(self):
        return len([e for e in self.entries.all() if e.book.read is not None])

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