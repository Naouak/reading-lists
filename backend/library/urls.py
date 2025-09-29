from django.urls import path, include

import library.views.books
import library.views.statistics
import library.views.redirects

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'book', library.views.books.BookViewSet)
router.register(r'series', library.views.books.BookSeriesViewSet)
router.register(r'reading-list', library.views.books.ReadingListViewSet)
router.register(r'reading-history', library.views.books.ReadingHistoryViewSet)
router.register(r'book-link', library.views.books.BookLinkViewSet)

reading_list_router = routers.NestedSimpleRouter(router, r'reading-list', lookup='reading_list')
reading_list_router.register(r'entries', library.views.books.ReadingListEntryViewSet, basename='reading-list-entries')
reading_list_router.register(r'series', library.views.books.ReadingListSeriesViewSet, basename='reading-list-series')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reading_list_router.urls)),
    path('reading-statistics/', library.views.statistics.statistics),
    path('completion-statistics/', library.views.statistics.completion),
    path('completion-series/', library.views.statistics.completion_series),
    path('monthly-completion/', library.views.statistics.monthly_completion),
    path('reading-history-summary/', library.views.books.read_history),
    path('book-link-graph/', library.views.books.book_links_graph),
    path('reading-report/', library.views.statistics.reading_report),
    path('read_online/<int:book_id>', library.views.redirects.read_online),
]