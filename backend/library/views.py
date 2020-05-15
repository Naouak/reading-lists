from django.db.models import F, Max
from django.http import HttpResponse

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import bad_request
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import BookSeries, Book, ReadingList, ReadingListEntry, ReadingHistory
from library.serializers import BookSeriesSerializer, BookSerializer, ReadingListSerializer, ReadingListEntrySerializer, \
    ReadingHistorySerializer


def index(request):
    return HttpResponse("Hello World")


class BookSeriesViewSet(viewsets.ModelViewSet):
    queryset = BookSeries.objects.all().order_by('id')
    serializer_class = BookSeriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)

        if search is not None:
            queryset = queryset.filter(title__contains=search)

        return queryset


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('pub_date')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        series = self.request.query_params.get('series', None)
        search = self.request.query_params.get('search', None)

        if series is not None:
            queryset = queryset.filter(series_id=series)
        if search is not None:
            queryset = queryset.filter(title__contains=search)

        return queryset

    @action(methods=['post'], detail=True)
    def read(self, request, pk=None):
        history = ReadingHistory(book_id=pk)
        history.save()
        serializer = ReadingHistorySerializer(history)
        return Response(serializer.data)

class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all().order_by('title')
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)

        if search is not None:
            queryset = queryset.filter(title__contains=search)

        return queryset

class ReadingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ReadingHistory.objects.all().order_by('-read_date')
    serializer_class = ReadingHistorySerializer
    permission_classes = [IsAuthenticated]

@permission_classes((IsAuthenticated,))
class ReadingListEntryViewSet(viewsets.ViewSet):
    def list(self, request, reading_list_pk):
        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk).order_by('position')
        serializer = ReadingListEntrySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, reading_list_pk, pk=None):
        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk)
        entry = get_object_or_404(queryset, pk=pk)
        serializer = ReadingListEntrySerializer(entry)
        return Response(serializer.data)

    def create(self, request, reading_list_pk):
        book = request.data['book']
        position = request.data['position'] if 'position' in request.data else None

        if book is None:
            raise bad_request(request, Exception())

        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk)

        if len(queryset.filter(book_id=book)):
            raise bad_request(request, Exception())

        if position is None:
            position = (queryset.aggregate(Max('position'))['position__max'] or 0) + 1

        entry = ReadingListEntry(book_id=book, position=position, reading_list_id=reading_list_pk)
        entry.save()

        serializer = ReadingListEntrySerializer(entry)
        return Response(serializer.data)

    def update(self, request, reading_list_pk, pk=None):
        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk)
        entry = get_object_or_404(queryset, pk=pk)

        queryset = queryset.exclude(pk=pk)

        if request.data['position'] < entry.position:
            queryset \
                .filter(position__gte=request.data['position'], position__lte=entry.position) \
                .update(position=F('position') + 1)
        if request.data['position'] > entry.position:
            queryset \
                .filter(position__gte=entry.position, position__lte=request.data['position']) \
                .update(position=F('position') - 1)

        entry.position = request.data['position']
        entry.save()

        serializer = ReadingListEntrySerializer(entry)
        return Response(serializer.data)

    def destroy(self, request, reading_list_pk, pk=None):
        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk)
        entry = get_object_or_404(queryset, pk=pk)

        queryset = queryset.exclude(pk=pk)
        queryset.filter(position__gt=entry.position).update(position=F('position') - 1)

        entry.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
