from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # DRF response ni keep chey, just format marchu
        custom_data = {
            "success": False,
            "message": str(response.data.get('detail', 'Error')),
            "error_code": "AUTH_ERROR" if response.status_code==401 else "VALIDATION_ERROR",
            "data": response.data
        }
        response.data = custom_data
        return response
    return None  # Django default ki vadilesey, HttpResponse return cheyaku