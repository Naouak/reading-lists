from .models import BookSeries, Book, ReadingList, ReadingListEntry, ReadingHistory
from rest_framework import serializers

class BookSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'book_count', 'cover_url']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'external_id', 'cover_url', 'pub_date', 'read_online_url', 'series', 'title', 'type', 'read']

class ReadingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingHistory
        fields = '__all__'
        depth = 1

class ReadingListEntrySerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = ReadingListEntry
        exclude= ['reading_list']
        depth = 1

class ReadingListSerializer(serializers.ModelSerializer):
    entries = ReadingListEntrySerializer(many=True, read_only=True, )
    class Meta:
        model = ReadingList
        fields = ['id', 'title', 'entries', 'progress']
