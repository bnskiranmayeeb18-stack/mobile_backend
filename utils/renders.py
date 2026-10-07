"""
renderers.py - Task 6 - Standardize ALL API responses automatically
"""

import json

from rest_framework.renderers import JSONRenderer


class StandardJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        # If already in our standard format, don't wrap again
        if isinstance(data, dict) and "success" in data and "message" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Error case - 4xx, 5xx
        if response and response.status_code >= 400:
            # DRF validation errors are like {"field": ["error"]}
            standardized = {
                "success": False,
                "message": (
                    "Validation failed"
                    if response.status_code == 400
                    else "Error occurred"
                ),
                "errors": data,
                "data": {},
            }
            return super().render(standardized, accepted_media_type, renderer_context)

        # Success case - 2xx
        # Try to get custom message from view, else default
        message = "Success"
        if response and hasattr(response, "status_code"):
            if response.status_code == 201:
                message = "Ride created successfully"
            elif response.status_code == 200:
                message = "Rides fetched successfully"

        standardized = {
            "success": True,
            "message": message,
            "data": data if data is not None else {},
        }
        return super().render(standardized, accepted_media_type, renderer_context)
