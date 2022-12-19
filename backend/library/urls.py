from django.urls import path, include

from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'book',views.BookViewSet)
router.register(r'series', views.BookSeriesViewSet)
router.register(r'reading-list', views.ReadingListViewSet)
router.register(r'reading-history', views.ReadingHistoryViewSet)
router.register(r'book-link', views.BookLinkViewSet)

reading_list_router = routers.NestedSimpleRouter(router, r'reading-list', lookup='reading_list')
reading_list_router.register(r'entries', views.ReadingListEntryViewSet, basename='reading-list-entries')
reading_list_router.register(r'series', views.ReadingListSeriesViewSet, basename='reading-list-series')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reading_list_router.urls)),
    path('reading-statistics/', views.statistics),
    path('completion-statistics/', views.completion),
    path('reading-history-summary/', views.read_history)
]