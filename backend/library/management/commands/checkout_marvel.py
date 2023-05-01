import json
import time
import datetime

from django.core.management import BaseCommand
from marvelous.exceptions import ApiError

from library.models import BookSeries, Book

from library.utils.marvel_api import get_client


class Command(BaseCommand):
    help = 'checkout marvel api for new data'

    def __init__(self):
        super().__init__()
        self.api_client = get_client()

    def add_arguments(self, parser):
        parser.add_argument('type', choices=['series', 'comics'], type=str)
        parser.add_argument('-p', '--max_pages', dest='max_pages', metavar='N', type=int,
                            help='Stop after checking N pages')
        parser.add_argument('-o', '--older_first', dest='older_first', action='store_true',
                            help='Start with older first (used to check that older issues are still in the catalog)')
        parser.set_defaults(older_first=False)

    def handle(self, *args, **options):
        type = options['type']
        max_pages = options['max_pages']
        older_first = options['older_first']

        if type == "comics":
            self.doComics(max_pages, older_first)
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
            object.pub_date = book.dates.on_sale or datetime.datetime(1900, 1, 1, 12, 0, 0, 0)
            object.availability_date = book.dates.unlimited
            object.type = str(book.format or 'comic').lower()[:64]
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

    def doComics(self, max_pages=None, older_first=False):
        offset = 0
        limit = 100
        done = False
        total = None
        while not done:
            print("Checking page %d " % offset)
            retry = 3
            while retry > 0:
                try:
                    comics = self.api_client.comics({
                        'orderBy': '-modified' if not older_first else 'modified',
                        'limit': limit,
                        'offset': offset,
                    })

                    if total is None:
                        total = comics.response['data']['total']

                    # Retry a page if it got empty results just to be sure
                    if len(comics) == 0:
                        print("Empty results, let's try again")
                        retry = retry - 1
                        continue

                    retry = 0
                    self.import_comics(comics)

                    if (total and offset < total) or max_pages and max_pages >= offset / limit:
                        done = True
                except ApiError as error:
                    print("Error with API:")
                    print(error)
                    time.sleep(1)
                    retry = retry - 1

            offset += 100
            time.sleep(1)
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
