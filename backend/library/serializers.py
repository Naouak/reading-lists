from .models import BookSeries, Book, ReadingList, ReadingListEntry, ReadingHistory, BookReadingHistory
from rest_framework import serializers

class BookSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'book_count', 'cover_url']

class BookReadingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReadingHistory
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    last_read_history = BookReadingHistorySerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'external_id', 'cover_url', 'pub_date', 'read_online_url', 'series', 'title', 'type', 'last_read_history', 'availability_date']

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
    series = BookSeriesSerializer(many=True, read_only=True, )
    class Meta:
        model = ReadingList
        fields = ['id', 'title', 'entries', 'series', 'archived']
