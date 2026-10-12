from rest_framework.response import Response

def standard_response(success=True, message="", data=None, error_code=None, status_code=200):
    body = {
        "success": success,
        "message": message,
        "error_code": error_code,
        "data": data
    }
    return Response(body, status=status_code)

def error_response(message="Error", error_code="ERROR", status_code=400, data=None):
    return standard_response(success=False, message=message, error_code=error_code, data=data, status_code=status_code)
