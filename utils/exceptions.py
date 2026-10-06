"""
exceptions.py - Centralized exception handling - Repeated try/except moved here
"""
from rest_framework.exceptions import APIException
from rest_framework import status

class BusinessLogicError(APIException):
    status_code = 400
    default_detail = 'Business logic error'
    default_code = 'business_error'

class ResourceNotFoundError(APIException):
    status_code = 404
    default_detail = 'Resource not found'
    default_code = 'not_found'

class PermissionDeniedError(APIException):
    status_code = 403
    default_detail = 'Permission denied'
    default_code = 'permission_denied'

class DuplicateResourceError(APIException):
    status_code = 409
    default_detail = 'Duplicate resource - idempotency'
    default_code = 'duplicate'