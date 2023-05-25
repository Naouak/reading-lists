from datetime import timedelta

from django.db.models import Count, Min, Max
from django.db.models.functions import ExtractYear, ExtractMonth

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from library.models import Book, BookReadingHistory, readable_books_query_set
from library.serializers import CompletionSeriesSerializer, ReadingHistorySerializer


@api_view(['GET'])
def statistics(request):
    stats = {}

    book_queryset = readable_books_query_set()

    stats['total_books'] = book_queryset.count()
    stats['read_books'] = BookReadingHistory.objects.count()

    current_date = timezone.make_aware(datetime.today())

    last_week = current_date - timedelta(days=7)
    previous_week = last_week - timedelta(days=7)
    last_month = current_date - timedelta(days=30)
    previous_month = last_month - timedelta(days=30)
    last_year = current_date - timedelta(days=365)
    previous_year = last_year - timedelta(days=365)

    stats['read_last_week'] = BookReadingHistory.objects.filter(read_date__gte=last_week).count()
    stats['read_previous_week'] = BookReadingHistory.objects.filter(read_date__gte=previous_week,
                                                                    read_date__lt=last_week).count()
    stats['read_last_month'] = BookReadingHistory.objects.filter(read_date__gte=last_month).count()
    stats['read_previous_month'] = BookReadingHistory.objects.filter(read_date__gte=previous_month,
                                                                     read_date__lt=last_month).count()
    stats['read_last_year'] = BookReadingHistory.objects.filter(read_date__gte=last_year).count()
    stats['read_previous_year'] = BookReadingHistory.objects.filter(read_date__gte=previous_year,
                                                                    read_date__lt=last_year).count()

    stats['added_last_week'] = book_queryset.filter(availability_date__gte=last_week).count()
    stats['added_previous_week'] = book_queryset.filter(availability_date__gte=previous_week,
                                                        availability_date__lt=last_week).count()
    stats['added_last_month'] = book_queryset.filter(availability_date__gte=last_month).count()
    stats['added_previous_month'] = book_queryset.filter(availability_date__gte=previous_month,
                                                         availability_date__lt=last_month).count()
    stats['added_last_year'] = book_queryset.filter(availability_date__gte=last_year).count()
    stats['added_previous_year'] = book_queryset.filter(availability_date__gte=previous_year,
                                                        availability_date__lt=last_year).count()

    return Response(stats)


@api_view(['GET'])
def completion(request):
    start = request.query_params.get('from', None)
    end = request.query_params.get('to', None)

    book_count = Book.objects \
        .exclude(title__icontains="trade paperback") \
        .exclude(title__icontains='(Hardcover)') \
        .annotate(year=ExtractYear('pub_date'), month=ExtractMonth('pub_date')) \
        .values('year', 'month') \
        .annotate(books=Count('id')) \
        .order_by('year', 'month') \
        .all()

    query_set = Book.objects
    if start:
        try:
            query_set = query_set.filter(last_read_history__read_date__gt=parse_datetime(start))
        except:
            pass
    if end:
        try:
            query_set = query_set.filter(last_read_history__read_date__lte=parse_datetime(end))
        except:
            pass

    book_read = query_set \
        .annotate(year=ExtractYear('pub_date'), month=ExtractMonth('pub_date')) \
        .values('year', 'month') \
        .annotate(read=Count('last_read_history__id')) \
        .order_by('year', 'month') \
        .all()

    book_read_map = {}
    for book_stat in book_read:
        book_read_map[str(book_stat['year']) + "-" + str(book_stat['month'])] = book_stat['read']

    for book_count_stats in book_count:
        key = str(book_count_stats['year']) + "-" + str(book_count_stats['month'])
        book_count_stats['read'] = book_read_map[key] if key in book_read_map else 0

    return Response(book_count)


@api_view(['GET'])
def monthly_completion(request):
    start = request.query_params.get('from', None)
    end = request.query_params.get('to', None)

    query_set = Book.objects
    if start:
        try:
            query_set = query_set.filter(last_read_history__read_date__gt=parse_datetime(start))
        except:
            pass
    if end:
        try:
            query_set = query_set.filter(last_read_history__read_date__lte=parse_datetime(end))
        except:
            pass

    book_read = query_set \
        .filter(last_read_history__isnull=False) \
        .annotate(pub_year=ExtractYear('pub_date')) \
        .values('pub_year') \
        .annotate(read_year=ExtractYear('last_read_history__read_date'), read_month=ExtractMonth('last_read_history__read_date'), read=Count('last_read_history__id')) \
        .order_by('read_year', 'read_month', 'pub_year') \
        .all()

    book_read_map = {}
    for book_stat in book_read:
        if book_stat['read_year'] is None:
            continue
        read_period = str(book_stat['read_year']) + "-" + ("00"+str(book_stat['read_month']))[-2:]
        pub_year = str(book_stat['pub_year'])
        if read_period not in book_read_map:
            book_read_map[read_period] = {}
        book_read_map[read_period][pub_year] = book_stat['read']

    return Response(book_read_map)


@api_view(['GET'])
def completion_series(request):
    start = request.query_params.get('from', None)
    end = request.query_params.get('to', None)

    query_set = readable_books_query_set()

    if start:
        try:
            query_set = query_set.filter(last_read_history__read_date__gt=parse_datetime(start))
        except:
            pass
    if end:
        try:
            query_set = query_set.filter(last_read_history__read_date__lte=parse_datetime(end))
        except:
            pass

    book_read = query_set \
        .values('series__title') \
        .annotate(book_count=Count('id'), book_read=Count('last_read_history__id'), first_book=Min('pub_date'),
                  last_book=Max('pub_date')) \
        .exclude(book_count__lte=1)

    serializer = CompletionSeriesSerializer(book_read, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def reading_report(request):
    default_date = datetime.today()
    year = request.query_params.get('year', default_date.year)
    month = request.query_params.get('month', None)

    read_books = BookReadingHistory.objects.filter(read_date__year=year)
    if month:
        read_books = read_books.filter(read_date__month=month)

    read_series = {}
    for read_book in read_books:
        series = read_book.book.series
        if series.title not in read_series:
            read_series[series.title] = []
        read_series[series.title].append(read_book)

    seriesList = {}
    for series in read_series:
        seriesList[series] = ReadingHistorySerializer(read_series[series], many=True).data

    read_reading_list = {}
    for read_book in read_books:
        reading_list_entries = read_book.book.readinglistentry_set.all()
        for reading_list_entry in reading_list_entries:
            reading_list = reading_list_entry.reading_list

            if reading_list.title not in read_reading_list:
                read_reading_list[reading_list.title] = {
                    'total_count': reading_list.entries.count(),
                    'read': []
                }
            read_reading_list[reading_list.title]['read'].append(read_book)

    readingLists = {}
    for readingList in read_reading_list:
        readingLists[readingList] = {
            'total_count': read_reading_list[readingList]['total_count'],
            'read': ReadingHistorySerializer(read_reading_list[readingList]['read'], many=True).data
        }

    return Response({
        'read_books': ReadingHistorySerializer(read_books, many=True).data,
        'read_series': seriesList,
        'read_lists': readingLists,
    })
