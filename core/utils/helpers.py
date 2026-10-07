def build_success_response(data=None, message="Success"):
    return {
        "success": True,
        "data": data,
        "message": message
    }

def build_error_response(message="Error", errors=None):
    return {
        "success": False,
        "data": None,
        "message": message,
        "errors": errors
    }