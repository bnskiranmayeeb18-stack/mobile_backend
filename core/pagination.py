# core/pagination.py
from rest_framework.pagination import CursorPagination

class RideCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-updated_at'
    cursor_query_param = 'cursor'
