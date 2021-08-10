from rest_framework.pagination import PageNumberPagination


class LargeSetPagination(PageNumberPagination):
    page_size = 100
    page_query_param = 'page'
    max_page_size = 1000
