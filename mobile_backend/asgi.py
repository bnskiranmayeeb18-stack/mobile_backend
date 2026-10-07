import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import rides.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mobile_backend.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(rides.routing.websocket_urlpatterns)
        ),
    }
)
