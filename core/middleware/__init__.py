import logging
from.request_id import request_id_ctx
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get() or '-'
        return True