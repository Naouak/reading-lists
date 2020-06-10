from django.core.management import BaseCommand
from library.models import BookSeries, Book

from library.utils.marvel_api import get_client


class Command(BaseCommand):
    help = 'checkout marvel api for new data'

    def __init__(self):
        super().__init__()
        self.api_client = get_client()

    def add_arguments(self, parser):
        parser.add_argument('type', choices=['series', 'comics'], type=str)

    def handle(self, *args, **options):
        type = options['type']

        if type == "comics":
            self.doComics()
        elif type == "series":
            self.doSeries()

    def import_series(self, series_list):
        for series in series_list:
            query_set = BookSeries.objects.filter(external_id=series.id)
            if len(query_set) >= 1:
                self.stdout.write(self.style.SUCCESS('Updating series "%s"' % series.title))
                object = query_set[0]
            else:
                self.stdout.write(self.style.SUCCESS('Importing series "%s"' % series.title))
                object = BookSeries(external_id=series.id)
            object.title = series.title
            object.save()

    def import_comics(self, comics):
        for book in comics:
            if book.digital_id is None:
                continue

            if not book.dates.unlimited:
                continue


            query_set = Book.objects.filter(external_id=book.id)
            if len(query_set) >= 1:
                self.stdout.write(self.style.SUCCESS('Updating comic "%s"' % book.title))
                object = query_set[0]
            else:
                self.stdout.write(self.style.SUCCESS('Importing comic "%s"' % book.title))
                object = Book(external_id=book.id, type='comic')
            object.external_source = 'marvel'
            object.title = book.title
            # cover_url
            if len(book.images) > 0:
                object.cover_url = book.images[0]
            # read_online_url
            object.read_online_url = "https://read.marvel.com/#/book/%s" % book.digital_id
            # pub_date
            object.pub_date = book.dates.on_sale
            object.availability_date = book.dates.unlimited
            # series
            if book.series:
                series_id = book.series.id
                series_query_set = BookSeries.objects.filter(external_id=series_id)
                if len(series_query_set) >= 1:
                    object.series = series_query_set[0]
                else:
                    series = BookSeries(title=book.series.name, external_id=book.series.id)
                    series.save()
                    object.series = series
            object.save()

    def doComics(self):
        offset = 0
        limit = 100
        while True:
            print("Checking page %d " % offset)
            comics = self.api_client.comics({
                'orderBy': '-modified',
                'limit': limit,
                'offset': offset,
            })

            self.import_comics(comics)

            if len(comics) < limit:
                break

            offset += 100
        pass

    def doSeries(self):
        offset = 0
        limit = 100
        while True:
            print("Checking page %d " % offset)
            series = self.api_client.series_list({
                'orderBy': 'modified',
                'limit': limit,
                'offset': offset,
            })

            self.import_series(series)

            if len(series) < limit:
                break

            offset += 100
        pass
