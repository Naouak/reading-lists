from rest_framework.pagination import PageNumberPagination as Pagination

class PageNumberPagination(Pagination):
    page_size_query_param = 'limit'