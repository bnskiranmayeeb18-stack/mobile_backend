from rest_framework.response import Response

def standard_response(success=True, message="", data=None, error_code=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "error_code": error_code,
        "data": data
    }, status=status_code)