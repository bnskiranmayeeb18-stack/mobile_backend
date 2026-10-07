from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and 'data' not in data and 'error' not in data:
            if 'results' in data or 'count' in data:
                return super().render(data, accepted_media_type, renderer_context)
            response_data = {
                'success': True,
                'data': data,
                'message': 'Success'
            }
            return super().render(response_data, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)