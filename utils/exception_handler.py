"""
exception_handler.py - Task 6 - Consistent error structure
"""

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error format
        custom_response = {
            "success": False,
            "message": (
                str(exc.detail)
                if hasattr(exc, "detail") and isinstance(exc.detail, str)
                else (
                    "Validation failed"
                    if response.status_code == 400
                    else "Error occurred"
                )
            ),
            "errors": response.data,
            "data": {},
        }
        # If detail is string, put in message
        if isinstance(response.data, dict) and "detail" in response.data:
            custom_response["message"] = str(response.data["detail"])
            custom_response["errors"] = {}
        elif isinstance(response.data, list):
            custom_response["errors"] = {"non_field_errors": response.data}

        response.data = custom_response

    return response
