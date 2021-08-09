#rest_framework.pagination.PageNumberPagination
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class BookPaginationPN(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 20
   

class BookPaginationLO(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'start'


class BookPaginationCP(CursorPagination):
    page_size = 10
    ordering = '-created'
