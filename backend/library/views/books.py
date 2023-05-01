from django.db.models import Min, Max, F, Count
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils.datetime_safe import date
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.exceptions import bad_request
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import BookSeries, Book, ReadingHistory, ReadingList, BookLink, ReadingListEntry, BookReadingHistory
from library.serializers import BookSeriesSerializer, BookSerializer, ReadingHistorySerializer, ReadingListSerializer, \
    BookLinkSerializer, ReadingListEntrySerializer


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
            search_terms = search.split(" ")
            for term in search_terms:
                queryset = queryset.filter(title__icontains=term)

        queryset = queryset.annotate(pub_date=Min("book__pub_date")).order_by('pub_date')

        return queryset


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('pub_date')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        series = self.request.query_params.get('series', None)
        search = self.request.query_params.get('search', None)
        exclude_term = self.request.query_params.get('exclude_term', None)
        only_available = self.request.query_params.get('only_available', None)
        only_published = self.request.query_params.get('only_published', None)

        external_source = self.request.query_params.get('external_source', None)
        external_id = self.request.query_params.get('external_id', None)

        if external_source is not None:
            queryset = queryset.filter(external_source=external_source)
            if external_id is not None:
                queryset = queryset.filter(external_id=external_id)

        if series is not None:
            queryset = queryset.filter(series_id=series)
        if search is not None:
            search_terms = search.split(" ")
            for term in search_terms:
                queryset = queryset.filter(title__icontains=term)
        if exclude_term is not None:
            exclude = exclude_term.split(",")
            for term in exclude:
                queryset = queryset.exclude(title__icontains=term)

        if only_available is not None:
            queryset = queryset.filter(availability_date__lte=date.today())
        if only_published is not None:
            queryset = queryset.filter(pub_date__lte=date.today())

        return queryset

    @action(methods=['post'], detail=True)
    def read(self, request, pk=None):
        history = ReadingHistory(book_id=pk)

        read_date = request.data['read_date'] if 'read_date' in request.data else None
        history.save()

        if read_date:
            history.read_date = parse_datetime(read_date)

        history.save()
        serializer = ReadingHistorySerializer(history)
        return Response(serializer.data)


class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all().order_by('title')
    serializer_class = ReadingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('entries__book').prefetch_related('entries__book__last_read_history')
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(title__contains=search)

        archived = self.request.query_params.get('archived', None)
        if archived:
            queryset = queryset.filter(archived=archived)

        return queryset


class ReadingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ReadingHistory.objects.all().order_by('-read_date')
    serializer_class = ReadingHistorySerializer
    permission_classes = [IsAuthenticated]


class BookLinkViewSet(viewsets.ModelViewSet):
    queryset = BookLink.objects.all().order_by('-created')
    serializer_class = BookLinkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        source_id = request.data['source']
        target_id = request.data.get('target', None)
        link_text = request.data['link_text']

        link = BookLink(source_id=source_id, target_id=target_id, link_text=link_text)
        link.save()

        serializer = BookLinkSerializer(link)
        return Response(serializer.data)


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


@permission_classes((IsAuthenticated,))
class ReadingListSeriesViewSet(viewsets.ViewSet):
    def list(self, request, reading_list_pk):
        queryset = ReadingListEntry.objects.filter(reading_list_id=reading_list_pk).order_by('position')
        serializer = ReadingListEntrySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, reading_list_pk, pk=None):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, reading_list_pk):
        if request.data['series_id'] is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        series = get_object_or_404(BookSeries.objects, pk=request.data['series_id'])
        ReadingList.objects.get(pk=reading_list_pk).series.add(series)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, reading_list_pk, pk=None):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, reading_list_pk, pk=None):
        series = get_object_or_404(BookSeries.objects, pk=pk)
        ReadingList.objects.get(pk=reading_list_pk).series.remove(series)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def read_history(request):
    read = BookReadingHistory.objects \
        .filter(read_date__gte=parse_datetime('2020-05-16T00:00:00Z')) \
        .values('read_date__date') \
        .order_by('read_date__date') \
        .annotate(read=Count('id'))

    for read_entry in read:
        read_entry['date'] = read_entry['read_date__date']
        del read_entry['read_date__date']

    return Response(read)


@api_view(['GET'])
def book_links_graph(request):
    links = BookLink.objects.exclude(target_id__isnull=True).all()
    nodes = {}
    edges = []
    for link in links:
        for node in [link.source, link.target]:
            if node.id not in nodes:
                nodes[node.id] = {
                    'data': {
                        'id': str(node.id),
                        'SUID': node.id,
                        'name': node.title,
                        'shared_name': node.title,
                        'img': node.cover_url
                    }
                }
        edges.append({
            'data': {
                "source": str(link.source_id),
                "target": str(link.target_id),
            }
        })
    return Response({
        'elements': {
            'nodes': nodes.values(),
            'edges': edges
        }
    })
