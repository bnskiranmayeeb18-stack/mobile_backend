from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # Standard format
        error_code = "VALIDATION_ERROR" if response.status_code == 400 else "API_ERROR"
        if response.status_code == 401:
            error_code = "UNAUTHORIZED"
        if response.status_code == 403:
            error_code = "FORBIDDEN"
        if response.status_code == 404:
            error_code = "NOT_FOUND"

        message = "Error occurred"
        if isinstance(response.data, dict):
            message = response.data.get('detail', str(list(response.data.values())[0][0]) if response.data else message)

        response.data = {
            "success": False,
            "message": message,
            "error_code": error_code,
            "data": None
        }
    return response