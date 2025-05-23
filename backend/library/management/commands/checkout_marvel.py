import re
import time
import datetime

import requests
from django.core.management import BaseCommand
from django.db.models import Q
from django.utils.datetime_safe import datetime as dj_datetime
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.timezone import make_aware
from marvelous.exceptions import ApiError

from library.models import BookSeries, Book

from library.utils.marvel_api import get_client
from library.utils.marvel_calendar import MarvelCalendar


class Command(BaseCommand):
    help = 'checkout marvel api for new data'

    def __init__(self):
        super().__init__()
        self.api_client = get_client()

    def print(self, text):
        self.stdout.write(str(datetime.datetime.now()) + " - " + self.style.SUCCESS(text))

    def error(self, text):
        self.stderr.write(str(datetime.datetime.now()) + " - " + str(text))

    def add_arguments(self, parser):
        parser.add_argument('type', choices=['series', 'comics', 'availability', 'calendar'], type=str)
        parser.add_argument('-p', '--max_pages', dest='max_pages', metavar='N', type=int,
                            help='Stop after checking N pages')
        parser.add_argument('-o', '--older_first', dest='older_first', action='store_true',
                            help='Start with older first (used to check that older issues are still in the catalog)')
        parser.add_argument('-n', '--page_size', dest='limit', metavar='N', type=int,
                            help='Start with older first (used to check that older issues are still in the catalog)')
        parser.add_argument('-t', '--title', dest='title_starts_with', metavar='title', type=str,
                            help='Filter with title')
        parser.add_argument('-s', '--start-date', dest='start_date', metavar='start_date', type=str, help='YYYY-MM-DD start date for calendar')
        parser.add_argument('-e', '--end-date', dest='end_date', metavar='end_date', type=str, help='YYYY-MM-DD end date for calendar')
        parser.set_defaults(older_first=False, limit=100)

    def handle(self, *args, **options):
        type = options['type']
        max_pages = options['max_pages']
        older_first = options['older_first']
        limit = options['limit']
        title_starts_with = options['title_starts_with']
        start_date = options['start_date']
        end_date = options['end_date']

        if type == "comics":
            self.do_comics(max_pages, older_first, limit, title_starts_with)
        elif type == "series":
            self.do_series()
        elif type == "availability":
            if title_starts_with:
                self.do_check_availability_by_name(title_starts_with)
            else:
                self.do_check_availability()
        elif type == "calendar":
            self.do_comics_from_calendar(start_date or (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
                                         end_date or (datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'))

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
                self.stdout.write(self.style.SUCCESS('No digital id for "%s"' % book.title))
                continue

            if not book.dates.unlimited:
                self.stdout.write(self.style.SUCCESS('No unlimited dates for "%s"' % book.title))
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

    def do_comics_from_calendar(self, start, end):
        calendar = MarvelCalendar()
        books = calendar.check_calendar(start, end)
        self.import_comics_from_calendar(books)

    def import_comics_from_calendar(self, comics):
        for book in comics:
            if book['digital_id'] is None:
                self.stdout.write(self.style.SUCCESS('No digital id for "%s"' % book['title']))
                continue

            query_set = Book.objects.filter(external_id=book['id'])
            if len(query_set) >= 1:
                self.stdout.write(self.style.SUCCESS('Updating comic "%s"' % book['title']))
                object = query_set[0]
            else:
                self.stdout.write(self.style.SUCCESS('Importing comic "%s"' % book['title']))
                object = Book(external_id=book['id'], type='comic')
            object.external_source = 'marvel'
            object.title = book['title']
            # cover_url
            object.cover_url = "https://cdn.marvel.com/u/prod/marvel" + book['image_url'] + "/portrait_uncanny.jpg"
            # read_online_url
            object.read_online_url = "https://read.marvel.com/#/book/%s" % book['digital_id']
            # pub_date
            object.pub_date = make_aware(datetime.datetime.strptime(book['release_date'], '%Y-%m-%d')) or datetime.datetime(1900, 1, 1, 12, 0, 0, 0)
            object.availability_date = make_aware(datetime.datetime.strptime(book['date_added_to_digital_comics'], '%Y-%m-%d'))
            object.type = str(book['metadata']['format'] or 'comic').lower()[:64]
            # series
            if book['metadata']['series']:
                series_id = book['metadata']['series']['id']
                series_query_set = BookSeries.objects.filter(external_id=series_id)
                if len(series_query_set) >= 1:
                    object.series = series_query_set[0]
                else:
                    series = BookSeries(title=book['metadata']['series']['title'], external_id=book['metadata']['series']['id'])
                    series.save()
                    object.series = series
            object.save()

    def do_comics(self, max_pages=None, older_first=False, limit=100, title_starts_with=None):
        offset = 0
        done = False
        total = None
        while not done and offset < 500000:
            self.print("Checking page %d / %d " % (offset, total or 0))
            if title_starts_with:
                self.print("Filtered by title: %s" % title_starts_with)
            retry = 3
            while retry > 0:
                try:
                    params = {
                        'orderBy': '-modified' if not older_first else 'modified',
                        'limit': limit,
                        'offset': offset,
                    }
                    if title_starts_with:
                        params['titleStartsWith'] = title_starts_with

                    comics = self.api_client.comics(params)

                    if total is None:
                        total = comics.response['data']['total']

                    # Retry a page if it got empty results just to be sure
                    if len(comics) == 0:
                        self.error("Empty results, let's try again")
                        retry = retry - 1
                        continue

                    retry = 0
                    self.import_comics(comics)

                    if (total and offset + limit >= total) or (max_pages and max_pages <= offset / limit):
                        done = True
                except ApiError as error:
                    self.error("Error with API:")
                    self.error(error)
                    time.sleep(1)
                    retry = retry - 1
                except Exception as error:
                    self.error("General Error:")
                    self.error(error)
                    time.sleep(1)
                    retry = retry - 1

            offset += limit
            time.sleep(1)
        pass

    def do_series(self):
        offset = 0
        limit = 100
        while True:
            self.print("Checking page %d " % offset)
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

    def do_check_availability(self):
        current_date = timezone.make_aware(dj_datetime.today())
        yesterday = current_date - datetime.timedelta(days=1)
        last_week = current_date - datetime.timedelta(days=7)

        books = Book.objects \
            .filter(available_online=False) \
            .filter(Q(availability_last_check__lt=last_week, pub_date__year__lt=current_date.year) | Q(
            availability_last_check__lt=yesterday, pub_date__year=current_date.year) | Q(availability_last_check=None)) \
            .order_by('-pub_date', '-modified_date')

        self.check_books_availability(books)

    def do_check_availability_by_name(self, search):
        queryset = Book.objects.filter(available_online=False)
        search_terms = search.split(" ")
        for term in search_terms:
            # ignore dashes
            if term == "-":
                continue

            # if starts with a dash then it's an exclude term
            if term.startswith("-"):
                queryset = queryset.exclude(title__icontains=term[1:])
                continue

            queryset = queryset.filter(title__icontains=term)
        self.check_books_availability(queryset)

    def check_books_availability(self, books):
        total_to_check = books.count()
        checked = 0
        for book in books:
            checked = checked + 1
            self.print('%d/%d Check Availability for %s' % (checked, total_to_check, book.title))
            self.check_availability(book)
            time.sleep(1)

    def check_availability(self, book: Book):
        digital_id = re.search(r'/(\d+)$', book.read_online_url).group(1)
        self.print('DigitalID: ' + digital_id)
        if not digital_id or int(digital_id) <= 0:
            return

        bifrost_data = requests.get(
            'https://bifrost.marvel.com/v1/catalog/digital-comics/metadata/' + digital_id).json()
        if bifrost_data['code'] == 200:
            book.available_online = not not bifrost_data['data']['results'][0]['issue_meta']['in_mu']
        book.availability_last_check = Now()
        book.save()
        if book.available_online:
            self.print(book.title + ' is available!')
        else:
            self.print(book.title + ' is not available.')
